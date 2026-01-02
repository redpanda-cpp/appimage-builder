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
from module.util import cflags_host, configure, make_default, make_destdir_install
from module.util import cmake_build, cmake_destdir_install, qt_configure_module
from module.util import meson_build, meson_config, meson_destdir_install

def _gmp(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.gmp / 'build-host'
  ensure(build_dir)

  configure(build_dir, [
    '--prefix=/usr/local',
    '--disable-assembly',
    '--enable-static',
    '--disable-shared',
    *cflags_host(),
  ])
  make_default(build_dir, config.jobs)
  make_destdir_install(build_dir, paths.layer_host.gmp)

def _mpfr(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.mpfr / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.gmp / 'usr/local',
  ]):
    configure(build_dir, [
      '--prefix=/usr/local',
      '--enable-static',
      '--disable-shared',
      *cflags_host(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_host.mpfr)

def _mpc(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.mpc / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.gmp / 'usr/local',
    paths.layer_host.mpfr / 'usr/local',
  ]):
    configure(build_dir, [
      '--prefix=/usr/local',
      '--enable-static',
      '--disable-shared',
      *cflags_host(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_host.mpc)

def _expat(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.expat / 'build-host'
  ensure(build_dir)

  configure(build_dir, [
    '--prefix=/usr/local',
    '--disable-shared',
    '--enable-static',
    *cflags_host(),
  ])
  make_default(build_dir, config.jobs)
  make_destdir_install(build_dir, paths.layer_host.expat)

def _ffi(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.ffi / 'build-host'
  ensure(build_dir)

  configure(build_dir, [
    '--prefix=/usr/local',
    '--disable-shared',
    '--enable-static',
    '--disable-multi-os-directory',
    *cflags_host(),
  ])
  make_default(build_dir, config.jobs)
  make_destdir_install(build_dir, paths.layer_host.ffi)

def _dbus(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.dbus / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.expat / 'usr/local',
  ]):
    configure(build_dir, [
      '--prefix=/usr/local',
      '--disable-shared',
      '--enable-static',
      *cflags_host(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_host.dbus)

def _wayland(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.wayland / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.expat / 'usr/local',
    paths.layer_host.ffi / 'usr/local',
  ]):
    meson_config(paths.src_dir.wayland, build_dir, [
      '--prefix', '/usr/local',
      '--libdir', '/usr/local/lib',
      '-Dscanner=true',
      '-Dtests=false',
      '-Ddocumentation=false',
      '-Ddtd_validation=false',
      '-Dicon_directory=/usr/share/icons',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, destdir = paths.layer_host.wayland)

def _qtbase(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qtbase / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.dbus / 'usr/local',
    paths.layer_host.wayland / 'usr/local',
  ]):
    configure(build_dir, [
      '-prefix', '/usr/local',
      # configure meta
      # build options
      '-cmake-generator', 'Ninja',
      '-release',
      '-gc-binaries',
      '-static',
      '-platform', 'linux-g++',
      '-no-pch',
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
    ])
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_host.qtbase)

def _qttools(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qttools / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.qtbase / 'usr/local',
  ]):
    qt_configure_module(paths.src_dir.qttools, build_dir, [
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
    ])
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_host.qttools)

def _qtwayland(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qtwayland / 'build-host'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.layer_host.qtbase / 'usr/local',
    paths.layer_host.wayland / 'usr/local',
  ]):
    qt_configure_module(paths.src_dir.qtwayland, build_dir, [
      '-no-feature-wayland-server',
    ])
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_host.qtwayland)

def build_host_lib(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  os.environ['PKG_CONFIG_PATH'] = '/usr/local/lib/pkgconfig'

  # toolchain
  _gmp(ver, paths, config)
  _mpfr(ver, paths, config)
  _mpc(ver, paths, config)

  # misc. round 1
  _expat(ver, paths, config)
  _ffi(ver, paths, config)

  # misc. round 2
  _dbus(ver, paths, config)
  _wayland(ver, paths, config)

  # host Qt
  _qtbase(ver, paths, config)
  _qttools(ver, paths, config)
  _qtwayland(ver, paths, config)

  del os.environ['PKG_CONFIG_PATH']
