import argparse
import logging
import os
from packaging.version import Version
from shutil import copyfile
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchVersions, ProfileInfo
from module.util import cflags_host, cmake_build, cmake_install, configure, ensure, make_default, make_install, meson_compile, meson_install, meson_setup, qt_configure_module

def _gmp(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.gmp / 'build-host'
  ensure(build_dir)
  configure('gmp', build_dir, [
    f'--prefix={paths.h_prefix}',
    '--disable-assembly',
    '--enable-static',
    '--disable-shared',
    *cflags_host(),
  ])
  make_default('gmp', build_dir, jobs)
  make_install('gmp', build_dir)

def _mpfr(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.mpfr / 'build-host'
  ensure(build_dir)
  configure('mpfr', build_dir, [
    f'--prefix={paths.h_prefix}',
    f'--with-gmp={paths.h_prefix}',
    '--enable-static',
    '--disable-shared',
    *cflags_host(),
  ])
  make_default('mpfr', build_dir, jobs)
  make_install('mpfr', build_dir)

def _mpc(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.mpc / 'build-host'
  ensure(build_dir)
  configure('mpc', build_dir, [
    f'--prefix={paths.h_prefix}',
    f'--with-gmp={paths.h_prefix}',
    f'--with-mpfr={paths.h_prefix}',
    '--enable-static',
    '--disable-shared',
    *cflags_host(),
  ])
  make_default('mpc', build_dir, jobs)
  make_install('mpc', build_dir)

def _expat(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.expat / 'build-host'
  ensure(build_dir)
  configure('expat', build_dir, [
    f'--prefix={paths.h_prefix}',
    '--disable-shared',
    '--enable-static',
    *cflags_host(),
  ])
  make_default('expat', build_dir, jobs)
  make_install('expat', build_dir)

def _ffi(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.ffi / 'build-host'
  ensure(build_dir)
  configure('ffi', build_dir, [
    f'--prefix={paths.h_prefix}',
    '--disable-shared',
    '--enable-static',
    '--disable-multi-os-directory',
    *cflags_host(),
  ])
  make_default('ffi', build_dir, jobs)
  make_install('ffi', build_dir)

def _dbus(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.dbus / 'build-host'
  ensure(build_dir)
  configure('dbus', build_dir, [
    f'--prefix={paths.h_prefix}',
    '--disable-shared',
    '--enable-static',
    *cflags_host(),
  ])
  make_default('dbus', build_dir, jobs)
  make_install('dbus', build_dir)

def _wayland(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.wayland / 'build-host'
  meson_setup('wayland', paths.wayland, build_dir, [
    '--prefix', paths.h_prefix,
    '--libdir', paths.h_prefix / 'lib',
    '--default-library', 'static',
    '--prefer-static',
    '-Dscanner=true',
    '-Dtests=false',
    '-Ddocumentation=false',
    '-Ddtd_validation=false',
    '-Dicon_directory=/usr/share/icons',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('wayland', build_dir, jobs)
  meson_install('wayland', build_dir)

def _qtbase(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qtbase / 'build-host'
  ensure(build_dir)
  configure('qtbase', build_dir, [
    '-prefix', paths.h_prefix / 'qt',
    # configure meta
    # build options
    '-cmake-generator', 'Ninja',
    '-release',
    '-optimize-size',
    '-gc-binaries',
    '-static',
    '-platform', 'linux-g++',
    '-pch',
    '-no-ltcg',
    '-linker', 'gold',
    '-no-unity-build',
    # build environment
    '-no-pkg-config',
    # component selection
    '-nomake', 'examples',
    '-gui',
    '-no-widgets',
    '-dbus-linked',
    # core options
    '-qt-doubleconversion',
    '-no-glib',
    '-no-icu',
    '-qt-pcre',
    '-qt-zlib',
    # network options
    '-no-ssl',
    # gui, printing, widget options
    '-no-cups',
    '-no-fontconfig',
    '-no-freetype',
    '-no-harfbuzz',
    '-no-opengl',
    '-no-xcb',
    '-no-libpng',
    '-no-libjpeg',
    # database options
    '-sql-sqlite',
    '-qt-sqlite',
    # cmake variables
    f'CMAKE_PREFIX_PATH={paths.h_prefix}',
  ])
  cmake_build('qtbase', build_dir, jobs)
  cmake_install('qtbase', build_dir)

def _qttools(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qttools / 'build-host'
  ensure(build_dir)
  qt_configure_module('qttools', paths.qttools, build_dir, [
    '-no-feature-assistant',
    '-no-feature-designer',
    '-no-feature-distancefieldgenerator',
    '-no-feature-kmap2qmap',
    '-feature-linguist',
    '-no-feature-pixeltool',
    '-no-feature-qdbus',
    '-no-feature-qdoc',
    '-no-feature-qev',
    '-no-feature-qtattributionsscanner',
    '-no-feature-qtdiag',
    '-no-feature-qtplugininfo',
    f'CMAKE_PREFIX_PATH={paths.h_prefix}',
  ])
  cmake_build('qttools', build_dir, jobs)
  cmake_install('qttools', build_dir)

def _qtwayland(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qtwayland / 'build-host'
  ensure(build_dir)
  qt_configure_module('qtwayland', paths.qtwayland, build_dir, [
    '-no-feature-wayland-server',
    f'CMAKE_PREFIX_PATH={paths.h_prefix}',
  ])
  cmake_build('qtwayland', build_dir, jobs)
  cmake_install('qtwayland', build_dir)

def build_host_lib(ver: BranchVersions, paths: ProjectPaths, info: ProfileInfo, config: argparse.Namespace):
  _gmp(ver.gmp, paths, info, config.jobs)
  _mpfr(ver.mpfr, paths, info, config.jobs)
  _mpc(ver.mpc, paths, info, config.jobs)

  _expat(ver.expat, paths, info, config.jobs)
  _ffi(ver.ffi, paths, info, config.jobs)

  _dbus(ver.dbus, paths, info, config.jobs)
  _wayland(ver.wayland, paths, info, config.jobs)

  _qtbase(ver.qt, paths, info, config.jobs)
  old_path = os.environ['PATH']
  os.environ['PATH'] = f'{paths.h_prefix}/qt/bin:{old_path}'
  _qttools(ver.qt, paths, info, config.jobs)
  _qtwayland(ver.qt, paths, info, config.jobs)
  os.environ['PATH'] = old_path
