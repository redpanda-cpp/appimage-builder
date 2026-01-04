import argparse
import logging
import os
from packaging.version import Version
from pathlib import Path
from shutil import copyfile
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import ensure, merge_libs, overlayfs_ro, toolchain_layers, qt_dependent_layers
from module.util import cflags_target, configure, make_default, make_destdir_install
from module.util import cmake_build, cmake_config, cmake_destdir_install, qt_configure_module
from module.util import meson_build, meson_config, meson_destdir_install

def _expat(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.expat / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.expat)

def _ffi(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.ffi / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      '--disable-multi-os-directory',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.ffi)

def _fuse(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.fuse / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    meson_config(paths.src_dir.fuse, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dudevrulesdir=/lib/udev/rules.d',
      '-Dutils=false',
      '-Dexamples=false',
      '-Dtests=false',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.fuse)

def _xml(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xml / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      '--without-python',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xml)

def _xcb_proto(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_proto / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_proto)

def _xorg_proto(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xorg_proto / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xorg_proto)

def _xtrans(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xtrans / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xtrans)

def _z(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.z / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    os.environ['CHOST'] = ver.target
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      '--static',
    ])
    del os.environ['CHOST']
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.z)

def _zstd(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  src_dir = paths.src_dir.zstd / 'build/meson'
  build_dir = paths.src_dir.zstd / 'build-target'

  with overlayfs_ro('/usr/local', toolchain_layers(paths)):
    meson_config(src_dir, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dbin_programs=false',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.zstd)

def _dbus(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.dbus / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.expat / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.dbus)

def _png(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.png / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.z / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.png)

def _squashfuse(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.squashfuse / 'build-target'
  ensure(build_dir)
  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.fuse / 'usr/local',
    paths.layer_target.z / 'usr/local',
    paths.layer_target.zstd / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      '--disable-demo',
      '--without-zlib',
      '--without-xcz',
      '--without-lzo',
      '--without-lz4',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.squashfuse)

  # required by appimage-runtime
  include_dir = paths.layer_target.squashfuse / f'usr/local/{ver.target}/include/squashfuse'
  copyfile(paths.src_dir.squashfuse / 'fuseprivate.h', include_dir / 'fuseprivate.h')

def _wayland(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.wayland / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_host.wayland / 'usr/local',
    paths.layer_target.ffi / 'usr/local',
    paths.layer_target.xml / 'usr/local',
  ]):
    meson_config(paths.src_dir.wayland, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dscanner=false',
      '-Dtests=false',
      '-Ddocumentation=false',
      '-Ddtd_validation=false',
      '-Dicon_directory=/usr/share/icons',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.wayland)

    merge_libs(
      ver.target,
      paths.layer_target.wayland / f'usr/local/{ver.target}/lib/libwayland-client.a',
      [
        build_dir / 'src/libwayland-client.a',
        paths.layer_target.ffi / f'usr/local/{ver.target}/lib/libffi.a',
      ],
    )

def _xau(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xau / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xau)

def _freetype_decycle(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.freetype / 'build-target-decycle'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.png / 'usr/local',
    paths.layer_target.z / 'usr/local',
  ]):
    meson_config(paths.src_dir.freetype, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dharfbuzz=disabled',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.freetype_decycle)

def _xcb(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb_proto / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb)

    merge_libs(
      ver.target,
      paths.layer_target.xcb / f'usr/local/{ver.target}/lib/libxcb.a',
      [
        build_dir / 'src/.libs/libxcb.a',
        paths.layer_target.xau / f'usr/local/{ver.target}/lib/libXau.a',
      ],
    )

def _harfbuzz(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.harfbuzz / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.freetype_decycle / 'usr/local',
    paths.layer_target.png / 'usr/local',
    paths.layer_target.z / 'usr/local',
  ]):
    meson_config(paths.src_dir.harfbuzz, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dfreetype=enabled',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.harfbuzz)

def _x(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.x / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
    paths.layer_target.xtrans / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      '--disable-malloc0returnsnull',  # workaround for cross build
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.x)

def _xcb_util(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util)

def _xcb_util_keysyms(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util_keysyms / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util_keysyms)

def _xcb_util_renderutil(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util_renderutil / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util_renderutil)

def _xcb_util_wm(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util_wm / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util_wm)

def _xkbcommon(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xkbcommon / 'build-target'

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xml / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    meson_config(paths.src_dir.xkbcommon, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '--default-library', 'static',
      '--prefer-static',
      '-Dxkb-config-root=/usr/share/X11/xkb',
      '-Dxkb-config-extra-path=/etc/xkb',
      '-Dx-locale-root=/usr/share/X11/locale',
      '-Denable-wayland=false',
      '--buildtype', 'minsize', '--strip',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.xkbcommon)

def _freetype(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.freetype / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.freetype_decycle / 'usr/local',
    paths.layer_target.harfbuzz / 'usr/local',
    paths.layer_target.png / 'usr/local',
    paths.layer_target.z / 'usr/local',
  ]):
    meson_config(paths.src_dir.freetype, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dharfbuzz=enabled',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.freetype)

def _xcb_util_image(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util_image / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xcb_util / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util_image)

    merge_libs(
      ver.target,
      paths.layer_target.xcb_util_image / f'usr/local/{ver.target}/lib/libxcb-image.a',
      [
        build_dir / 'image/.libs/libxcb-image.a',
        paths.layer_target.xcb_util / f'usr/local/{ver.target}/lib/libxcb-util.a',
      ],
    )

def _fontconfig(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.fontconfig / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.expat / 'usr/local',
    paths.layer_target.freetype / 'usr/local',
    paths.layer_target.harfbuzz / 'usr/local',
    paths.layer_target.png / 'usr/local',
    paths.layer_target.z / 'usr/local',
  ]):
    meson_config(paths.src_dir.fontconfig, build_dir, [
      '--cross-file', paths.meson_cross_file,
      '--prefix', f'/usr/local/{ver.target}',
      '-Dcache-dir=/var/cache/fontconfig',
      '-Dtemplate-dir=/usr/share/fontconfig/conf.avail',
      '-Dbaseconfig-dir=/etc/fonts',
    ])
    meson_build(build_dir, config.jobs)
    meson_destdir_install(build_dir, paths.layer_target.fontconfig)

    merge_libs(
      ver.target,
      paths.layer_target.fontconfig / f'usr/local/{ver.target}/lib/libfontconfig.a',
      [
        build_dir / 'src/libfontconfig.a',
        paths.layer_target.expat / f'usr/local/{ver.target}/lib/libexpat.a',
        paths.layer_target.freetype / f'usr/local/{ver.target}/lib/libfreetype.a',
      ],
    )

def _xcb_util_cursor(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.xcb_util_cursor / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xcb_util / 'usr/local',
    paths.layer_target.xcb_util_image / 'usr/local',
    paths.layer_target.xcb_util_renderutil / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
  ]):
    configure(build_dir, [
      f'--prefix=/usr/local/{ver.target}',
      f'--host={ver.target}',
      '--disable-shared',
      '--enable-static',
      *cflags_target(),
    ])
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer_target.xcb_util_cursor)

def _qtbase(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qtbase / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
  ]):
    configure(build_dir, [
      '-prefix', f'/usr/local/{ver.target}',
      # build options
      '-cmake-generator', 'Ninja',
      '-release',
      '-optimize-size',
      '-gc-binaries',
      '-static',
      '-platform', 'linux-g++',
      '-xplatform', 'devices/linux-generic-g++',
      '-device', 'linux-generic-g++',
      '-device-option', f'CROSS_COMPILE={ver.target}-',
      '-qt-host-path', '/usr/local',
      '-no-pch',
      '-ltcg',
      '-no-unity-build',
      # build environment
      '-pkg-config',
      # component selection
      '-nomake', 'examples',
      '-gui',
      '-widgets',
      '-dbus-linked',
      # core options
      '-qt-doubleconversion',
      '-no-glib',
      '-no-icu',
      '-qt-pcre',
      '-system-zlib',
      # network options
      '-no-ssl',
      # gui, printing, widget options
      '-no-cups',
      '-fontconfig',
      '-system-freetype',
      '-system-harfbuzz',
      '-no-opengl',
      '-qpa', 'xcb;wayland',
      '-xcb',
      '-xkbcommon',
      '-system-libpng',
      '-qt-libjpeg',
      # database options
      '-sql-sqlite',
      '-qt-sqlite',
      # cmake variables
      f'CMAKE_TOOLCHAIN_FILE={paths.cmake_cross_file}',
      f'CMAKE_PREFIX_PATH=/usr/local/{ver.target}',
    ])
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_target.qtbase)

def _qtsvg(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qtsvg / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
    paths.layer_target.qtbase / 'usr/local',
  ]):
    qt_configure_module(paths.src_dir.qtsvg, build_dir, [
      f'CMAKE_PREFIX_PATH=/usr/local/{ver.target}',
    ], triplet = ver.target)
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_target.qtsvg)

def _qttools(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qttools / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
    paths.layer_target.qtbase / 'usr/local',
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
      f'CMAKE_PREFIX_PATH=/usr/local/{ver.target}',
    ], triplet = ver.target)
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_target.qttools)

def _qttranslations(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qttranslations / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
    paths.layer_target.qtbase / 'usr/local',
    paths.layer_target.qttools / 'usr/local',
  ]):
    qt_configure_module(paths.src_dir.qttranslations, build_dir, [
      f'CMAKE_PREFIX_PATH=/usr/local/{ver.target}',
    ], triplet = ver.target)
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_target.qttranslations)

def _qtwayland(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.qtwayland / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
    paths.layer_target.qtbase / 'usr/local',
  ]):
    qt_configure_module(paths.src_dir.qtwayland, build_dir, [
      '-no-feature-wayland-server',
      f'CMAKE_PREFIX_PATH=/usr/local/{ver.target}',
    ], triplet = ver.target)
    cmake_build(build_dir, config.jobs)
    cmake_destdir_install(build_dir, paths.layer_target.qtwayland)

def _fcitx_qt(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.fcitx_qt / 'build-target'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    *qt_dependent_layers(paths),
    paths.layer_target.qtbase / 'usr/local',
    paths.layer_target.qtwayland / 'usr/local',
  ]):
    cmake_config(paths.src_dir.fcitx_qt, build_dir, [
      f'-DCMAKE_TOOLCHAIN_FILE={paths.cmake_cross_file}',
      f'-DCMAKE_PREFIX_PATH=/usr/local/{ver.target}',
      f'-DCMAKE_INSTALL_PREFIX=/usr/local/{ver.target}',
      '-DENABLE_QT5=Off',
      '-DENABLE_QT6=On',
      '-DBUILD_ONLY_PLUGIN=On',
      '-DBUILD_STATIC_PLUGIN=On',
    ])
    cmake_build(build_dir, config.jobs)

    # fcitx-qt installs to host qt dir, even if specified `CMAKE_INSTALL_PREFIX`
    # here we do manual copy
    ime_dir = paths.layer_target.fcitx_qt / f'usr/local/{ver.target}/plugins/platforminputcontexts'
    ensure(ime_dir)
    copyfile(build_dir / 'qt6/platforminputcontext/libfcitx5platforminputcontextplugin.a', ime_dir / 'libfcitx5platforminputcontextplugin.a')

    # and generate missing cmake files
    cmake_dir = f'usr/local/{ver.target}/lib/cmake/Qt6Gui'
    ibus_cmake_dir = Path('/') / cmake_dir
    fcitx_cmake_dir = paths.layer_target.fcitx_qt / cmake_dir
    ensure(fcitx_cmake_dir)

    for ibus_file in ibus_cmake_dir.glob('Qt6QIbusPlatformInputContextPlugin*.cmake'):
      ibus_content = open(ibus_file, 'r').read()
      fcitx_file = fcitx_cmake_dir / ibus_file.name.replace('Ibus', 'Fcitx5')
      with open(fcitx_file, 'w') as f:
        f.write(ibus_content.replace('ibus', 'fcitx5').replace('Ibus', 'Fcitx5'))

    import_object = paths.layer_target.fcitx_qt / f'usr/local/{ver.target}/plugins/platforminputcontexts/objects-Release/QFcitx5PlatformInputContextPlugin_init/QFcitx5PlatformInputContextPlugin_init.cpp.o'
    ensure(import_object.parent)
    subprocess.run([
      f'{ver.target}-g++',
      '-std=c++17', '-O3',
      '-I', f'/usr/local/{ver.target}/include/QtCore',
      '-c', paths.root_dir / 'support/fcitx/import.cc',
      '-o', import_object,
    ], check = True)

def _appimage_runtime(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.appimage_runtime / 'build-target'
  src_dir = paths.src_dir.appimage_runtime / 'src/runtime'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    *toolchain_layers(paths),
    paths.layer_target.fuse / 'usr/local',
    paths.layer_target.squashfuse / 'usr/local',
    paths.layer_target.z / 'usr/local',
    paths.layer_target.zstd / 'usr/local',
  ]):
    subprocess.run([
      f'{ver.target}-gcc',
      '-std=gnu99',
      '-O2',
      '-I', f'/usr/local/{ver.target}/include/fuse3',
      '-D_FILE_OFFSET_BITS=64',
      '-DGIT_COMMIT="{ver}"',
      '-T', src_dir / 'data_sections.ld',
      '-static-pie',
      '-s',
      src_dir / 'runtime.c',
      '-lsquashfuse',
      '-lsquashfuse_ll',
      '-lzstd',
      '-lfuse3',
      '-o', build_dir / 'appimage-runtime',
    ], check = True)

    # magic bytes
    subprocess.run([
      'dd',
      f'of={build_dir}/appimage-runtime',
      'bs=1',
      'count=3',
      'seek=8',
      'conv=notrunc',
    ], input = b'AI\x02', check = True)

    bin_dir = paths.layer_target.appimage_runtime / f'usr/local/{ver.target}/bin'
    ensure(bin_dir)
    copyfile(build_dir / 'appimage-runtime', bin_dir / 'appimage-runtime')

def build_target_lib(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  # misc: round 1
  _expat(ver, paths, config)
  _ffi(ver, paths, config)
  _fuse(ver, paths, config)
  _xml(ver, paths, config)
  _xcb_proto(ver, paths, config)
  _xorg_proto(ver, paths, config)
  _xtrans(ver, paths, config)
  _z(ver, paths, config)
  _zstd(ver, paths, config)

  # misc: round 2
  _dbus(ver, paths, config)
  _png(ver, paths, config)
  _squashfuse(ver, paths, config)
  _wayland(ver, paths, config)
  _xau(ver, paths, config)

  # misc: round 3
  _freetype_decycle(ver, paths, config)
  _xcb(ver, paths, config)

  # misc: round 4
  _harfbuzz(ver, paths, config)
  _x(ver, paths, config)
  _xcb_util(ver, paths, config)
  _xcb_util_keysyms(ver, paths, config)
  _xcb_util_renderutil(ver, paths, config)
  _xcb_util_wm(ver, paths, config)
  _xkbcommon(ver, paths, config)

  # misc: round 5
  _freetype(ver, paths, config)
  _xcb_util_image(ver, paths, config)

  # misc: round 6
  _fontconfig(ver, paths, config)
  _xcb_util_cursor(ver, paths, config)

  # target Qt
  _qtbase(ver, paths, config)
  _qtsvg(ver, paths, config)
  _qttools(ver, paths, config)
  _qttranslations(ver, paths, config)
  _qtwayland(ver, paths, config)
  _fcitx_qt(ver, paths, config)

  # appimage
  _appimage_runtime(ver, paths, config)
