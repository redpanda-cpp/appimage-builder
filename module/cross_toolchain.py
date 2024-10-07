import argparse
import logging
from packaging.version import Version
from shutil import copyfile
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchVersions, ProfileInfo
from module.util import cflags_host, cflags_target, configure, ensure, make_custom, make_default, make_install

def _linux_headers(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  make_custom('linux-headers', paths.linux_headers, [
    f'ARCH={info.kernel_arch}',
    f'prefix={paths.prefix}',
    'install',
  ], jobs = 1)

def _binutils(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  gold_arg = '--enable-gold'
  if info.arch in ('riscv64', 'loong64'):
    gold_arg = '--disable-gold'

  build_dir = paths.binutils / 'build-x'
  ensure(build_dir)
  configure('binutils', build_dir, [
    f'--prefix={paths.h_prefix}',
    f'--target={info.target}',
    # static build
    '--disable-shared',
    '--enable-static',
    # features
    gold_arg,
    '--disable-install-libbfd',
    '--disable-multilib',
    '--disable-nls',
    *cflags_host(),
  ])
  make_default('binutils', build_dir, jobs)
  make_install('binutils', build_dir)

def _gcc(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.gcc / 'build-x'
  ensure(build_dir)
  configure('gcc', build_dir, [
    f'--prefix={paths.h_prefix}',
    f'--with-gcc-major-version-only',
    f'--target={info.target}',
    # static build
    '--disable-plugin',
    '--disable-shared',
    '--enable-static',
    # features
    '--enable-checking=release',
    '--enable-default-pie',
    '--disable-dependency-tracking',
    '--enable-host-pie',
    '--enable-languages=c,c++',
    '--disable-libgomp',
    '--disable-libsanitizer',
    '--enable-lto',
    '--disable-multilib',
    '--disable-nls',
    # packages
    f'--with-gmp={paths.h_prefix}',
    '--without-libcc1',
    '--without-libiconv',
    '--without-libintl',
    f'--with-mpc={paths.h_prefix}',
    f'--with-mpfr={paths.h_prefix}',
    *cflags_host(),
    *cflags_target('_FOR_TARGET'),
  ])
  make_custom('gcc (all-gcc)', build_dir, ['all-gcc'], jobs)
  make_custom('gcc (install-gcc)', build_dir, ['install-gcc'], jobs = 1)
  yield

  make_custom('gcc (all-target-libgcc)', build_dir, ['all-target-libgcc'], jobs)
  make_custom('gcc (install-target-libgcc)', build_dir, ['install-target-libgcc'], jobs = 1)
  yield

  make_default('gcc', build_dir, jobs)
  make_install('gcc', build_dir)
  yield

def _musl(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.musl / 'build-x'
  ensure(build_dir)
  configure('musl', build_dir, [
    f'--prefix={paths.prefix}',
    f'--target={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_custom('musl (install-headers)', build_dir, ['install-headers'], jobs = 1)
  yield

  make_default('musl', build_dir, jobs)
  make_install('musl', build_dir)
  yield

def build_cross_toolchain(ver: BranchVersions, paths: ProjectPaths, info: ProfileInfo, config: argparse.Namespace):
  _linux_headers(ver.linux_headers, paths, info, config.jobs)

  _binutils(ver.binutils, paths, info, config.jobs)

  gcc = _gcc(ver.gcc, paths, info, config.jobs)
  gcc.__next__()

  musl = _musl(ver.musl, paths, info, config.jobs)
  musl.__next__()

  gcc.__next__()

  musl.__next__()

  gcc.__next__()
