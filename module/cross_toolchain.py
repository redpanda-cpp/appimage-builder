import argparse
import logging
import os
from packaging.version import Version
from shutil import copyfile
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import ensure, overlayfs_ro
from module.util import cflags_host, cflags_target, configure, make_custom, make_default, make_destdir_install, overlayfs_ro
from module.util import meson_build, meson_config, meson_destdir_install

def _linux_headers(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  make_custom(paths.src_dir.linux_headers, [
    f'ARCH={ver.kernel_arch}',
    f'prefix={paths.layer_x.linux}/usr/local/{ver.target}',
    'install',
  ], jobs = 1)

def _binutils(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  gold_arg = '--enable-gold'
  if info.arch in ('riscv64', 'loong64'):
    gold_arg = '--disable-gold'

  build_dir = paths.src_dir.binutils / 'build-x'
  ensure(build_dir)

  configure(build_dir, [
    '--prefix=/usr/local',
    f'--target={ver.target}',
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
  make_default(build_dir, config.jobs)
  make_destdir_install(build_dir, paths.layer_x.binutils)

def _gcc(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.gcc / 'build-x'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.gmp / 'usr/local',
    paths.layer_host.mpfr / 'usr/local',
    paths.layer_host.mpc / 'usr/local',

    paths.layer_x.binutils / 'usr/local',
  ]):
    configure(build_dir, [
      '--prefix=/usr/local',
      f'--with-gcc-major-version-only',
      f'--target={ver.target}',
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
      '--with-gmp=/usr/local',
      '--without-libcc1',
      '--without-libiconv',
      '--without-libintl',
      '--with-mpc=/usr/local',
      '--with-mpfr=/usr/local',
      *cflags_host(),
      *cflags_target('_FOR_TARGET'),
    ])
    make_custom(build_dir, ['all-gcc'], config.jobs)
    make_custom(build_dir, ['install-gcc', f'DESTDIR={paths.layer_x.gcc}'], jobs = 1)
  yield

  with overlayfs_ro('/usr/local', [
    paths.layer_host.gmp / 'usr/local',
    paths.layer_host.mpfr / 'usr/local',
    paths.layer_host.mpc / 'usr/local',

    paths.layer_x.binutils / 'usr/local',
    paths.layer_x.gcc / 'usr/local',
    paths.layer_x.linux / 'usr/local',
    paths.layer_x.musl / 'usr/local',
  ]):
    make_custom(build_dir, ['all-target-libgcc'], config.jobs)
    make_custom(build_dir, ['install-target-libgcc', f'DESTDIR={paths.layer_x.gcc}'], jobs = 1)
  yield

  with overlayfs_ro('/usr/local', [
    paths.layer_host.gmp / 'usr/local',
    paths.layer_host.mpfr / 'usr/local',
    paths.layer_host.mpc / 'usr/local',

    paths.layer_x.binutils / 'usr/local',
    paths.layer_x.gcc / 'usr/local',
    paths.layer_x.linux / 'usr/local',
    paths.layer_x.musl / 'usr/local',
  ]):
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_x.gcc)
  yield

def _musl(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.musl / 'build-x'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_x.binutils / 'usr/local',
    paths.layer_x.gcc / 'usr/local',
    paths.layer_x.linux / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--target={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_custom(build_dir, ['install-headers', f'DESTDIR={paths.layer_x.musl}'], jobs = 1)
  yield

  with overlayfs_ro('/usr/local', [
    paths.layer_x.binutils / 'usr/local',
    paths.layer_x.gcc / 'usr/local',
    paths.layer_x.linux / 'usr/local',
    paths.layer_x.musl / 'usr/local',
  ]):
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_x.musl)
  yield

def _pkgconf(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.pkgconf / 'build-x'
  ensure(build_dir)

  meson_config(paths.src_dir.pkgconf, build_dir, [
    '--prefix', f'/usr/local/{ver.target}',
    '--libdir', f'/usr/local/{ver.target}/lib',
    '-Dtests=disabled',
  ])
  meson_build(build_dir, config.jobs)
  meson_destdir_install(build_dir, paths.layer_x.pkgconf)

  bin_dir = paths.layer_x.pkgconf / f'usr/local/bin'
  alias = bin_dir / f'{ver.target}-pkg-config'
  ensure(bin_dir)
  if alias.exists():
    os.remove(alias)
  os.symlink(f'../{ver.target}/bin/pkgconf', bin_dir / f'{ver.target}-pkg-config')

def build_cross_toolchain(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):

  _linux_headers(ver, paths, config)

  _binutils(ver, paths, config)

  gcc = _gcc(ver, paths, config)
  gcc.__next__()

  musl = _musl(ver, paths, config)
  musl.__next__()

  gcc.__next__()

  musl.__next__()

  gcc.__next__()

  _pkgconf(ver, paths, config)
