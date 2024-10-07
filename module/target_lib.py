import argparse
import logging
import os
from packaging.version import Version
from shutil import copyfile
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchVersions, ProfileInfo
from module.util import cflags_target, cmake_build, cmake_config, cmake_install, configure, ensure, make_default, make_install, meson_compile, meson_install, meson_setup, qt_configure_module

def _expat(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.expat / 'build-target'
  ensure(build_dir)
  configure('expat', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('expat', build_dir, jobs)
  make_install('expat', build_dir)

def _ffi(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.ffi / 'build-target'
  ensure(build_dir)
  configure('ffi', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    '--disable-multi-os-directory',
    *cflags_target(),
  ])
  make_default('ffi', build_dir, jobs)
  make_install('ffi', build_dir)

def _fuse(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.fuse / 'build-target'
  meson_setup('fuse', paths.fuse, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dudevrulesdir=/lib/udev/rules.d',
    '-Dutils=false',
    '-Dexamples=false',
    '-Dtests=false',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('fuse', build_dir, jobs)
  meson_install('fuse', build_dir)

def _xml(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xml / 'build-target'
  ensure(build_dir)
  configure('xml', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    '--without-python',
    *cflags_target(),
  ])
  make_default('xml', build_dir, jobs)
  make_install('xml', build_dir)

def _z(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.z / 'build-target'
  ensure(build_dir)
  os.environ['CHOST'] = info.target
  configure('z', build_dir, [
    f'--prefix={paths.prefix}',
    '--static',
  ])
  del os.environ['CHOST']
  make_default('z', build_dir, jobs)
  make_install('z', build_dir)

def _zstd(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  src_dir = paths.zstd / 'build/meson'
  build_dir = paths.zstd / 'build-target'
  meson_setup('zstd', src_dir, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dbin_programs=false',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('zstd', build_dir, jobs)
  meson_install('zstd', build_dir)

def _squashfuse(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.squashfuse / 'build-target'
  ensure(build_dir)
  configure('squashfuse', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    '--disable-demo',
    '--without-zlib',
    '--without-xcz',
    '--without-lzo',
    '--without-lz4',
    *cflags_target(),
  ])
  make_default('squashfuse', build_dir, jobs)
  make_install('squashfuse', build_dir)

  # required by appimage-runtime
  copyfile(paths.squashfuse / 'fuseprivate.h', paths.prefix / 'include/squashfuse/fuseprivate.h')

def _appimage_runtime(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.appimage_runtime / 'build-target'
  ensure(build_dir)
  ret = subprocess.run([
    f'{info.target}-gcc',
    '-std=gnu99',
    '-Os',
    '-I', paths.prefix / 'include/fuse3',
    '-D_FILE_OFFSET_BITS=64',
    '-DGIT_COMMIT="{ver}"',
    '-T', paths.appimage_runtime / 'src/runtime/data_sections.ld',
    '-static',
    '-s',
    paths.appimage_runtime / 'src/runtime/runtime.c',
    '-lsquashfuse',
    '-lsquashfuse_ll',
    '-lzstd',
    '-lfuse3',
    '-o', f'{build_dir}/appimage-runtime',
  ], check = False)
  if ret.returncode != 0:
    raise Exception(f'Build fail: appimage-runtime gcc returned {ret.returncode}')

  # magic bytes
  ret = subprocess.run([
    'dd',
    f'of={build_dir}/appimage-runtime',
    'bs=1',
    'count=3',
    'seek=8',
    'conv=notrunc',
  ], input = b'AI\x02', check = False)
  if ret.returncode != 0:
    raise Exception(f'Build fail: appimage-runtime dd returned {ret.returncode}')

  copyfile(build_dir / 'appimage-runtime', paths.prefix / 'bin' / 'appimage-runtime')

def _dbus(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.dbus / 'build-target'
  ensure(build_dir)
  configure('dbus', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('dbus', build_dir, jobs)
  make_install('dbus', build_dir)

def _wayland(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.wayland / 'build-target'
  meson_setup('wayland', paths.wayland, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dscanner=false',
    '-Dtests=false',
    '-Ddocumentation=false',
    '-Ddtd_validation=false',
    '-Dicon_directory=/usr/share/icons',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('wayland', build_dir, jobs)
  meson_install('wayland', build_dir)

  # merge libs -- workaround for Qt missing static library
  res = subprocess.run(['ar', '-M'], cwd = build_dir, input = (
    f'create {paths.prefix}/lib/libwayland-client.a\n'
    f'addlib {build_dir}/src/libwayland-client.a\n'
    f'addlib {paths.prefix}/lib/libffi.a\n'
    'save\n'
    'end\n'
  ).encode())
  if res.returncode != 0:
    raise Exception(f'Build fail: wayland merge libs returned {res.returncode}')

def _xorg_proto(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xorg_proto / 'build-target'
  ensure(build_dir)
  configure('xorgproto', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xorgproto', build_dir, jobs)
  make_install('xorgproto', build_dir)

def _xau(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xau / 'build-target'
  ensure(build_dir)
  configure('xau', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xau', build_dir, jobs)
  make_install('xau', build_dir)

def _xcb_proto(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_proto / 'build-target'
  ensure(build_dir)
  configure('xcb', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb', build_dir, jobs)
  make_install('xcb', build_dir)

def _xcb(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb / 'build-target'
  ensure(build_dir)
  configure('xcb', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb', build_dir, jobs)
  make_install('xcb', build_dir)

  # merge libs -- workaround for Qt feature test
  res = subprocess.run(['ar', '-M'], cwd = build_dir, input = (
    f'create {paths.prefix}/lib/libxcb.a\n'
    f'addlib {build_dir}/src/.libs/libxcb.a\n'
    f'addlib {paths.prefix}/lib/libXau.a\n'
    'save\n'
    'end\n'
  ).encode())
  if res.returncode != 0:
    raise Exception(f'Build fail: xcb merge libs returned {res.returncode}')

def _xtrans(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xtrans / 'build-target'
  ensure(build_dir)
  configure('xtrans', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xtrans', build_dir, jobs)
  make_install('xtrans', build_dir)

def _x(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.x / 'build-target'
  ensure(build_dir)
  configure('x', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    '--disable-malloc0returnsnull',  # workaround for cross build
    *cflags_target(),
  ])
  make_default('x', build_dir, jobs)
  make_install('x', build_dir)

def _xcb_util(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util / 'build-target'
  ensure(build_dir)
  configure('xcb_util', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util', build_dir, jobs)
  make_install('xcb_util', build_dir)

def _xcb_util_image(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util_image / 'build-target'
  ensure(build_dir)
  configure('xcb_util_image', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util_image', build_dir, jobs)
  make_install('xcb_util_image', build_dir)

  # merge libs -- workaround for Qt missing static library
  res = subprocess.run(['ar', '-M'], cwd = build_dir, input = (
    f'create {paths.prefix}/lib/libxcb-image.a\n'
    f'addlib {build_dir}/image/.libs/libxcb-image.a\n'
    f'addlib {paths.prefix}/lib/libxcb-util.a\n'
    'save\n'
    'end\n'
  ).encode())
  if res.returncode != 0:
    raise Exception(f'Build fail: xcb_util_image merge libs returned {res.returncode}')

def _xcb_util_keysyms(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util_keysyms / 'build-target'
  ensure(build_dir)
  configure('xcb_util_keysyms', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util_keysyms', build_dir, jobs)
  make_install('xcb_util_keysyms', build_dir)

def _xcb_util_renderutil(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util_renderutil / 'build-target'
  ensure(build_dir)
  configure('xcb_util_renderutil', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util_renderutil', build_dir, jobs)
  make_install('xcb_util_renderutil', build_dir)

def _xcb_util_wm(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util_wm / 'build-target'
  ensure(build_dir)
  configure('xcb_util_wm', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util_wm', build_dir, jobs)
  make_install('xcb_util_wm', build_dir)

def _xcb_util_cursor(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xcb_util_cursor / 'build-target'
  ensure(build_dir)
  configure('xcb_util_cursor', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('xcb_util_cursor', build_dir, jobs)
  make_install('xcb_util_cursor', build_dir)

def _xkbcommon(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.xkbcommon / 'build-target'
  meson_setup('xkbcommon', paths.xkbcommon, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dxkb-config-root=/usr/share/X11/xkb',
    '-Dxkb-config-extra-path=/etc/xkb',
    '-Dx-locale-root=/usr/share/X11/locale',
    '-Denable-wayland=false',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('xkbcommon', build_dir, jobs)
  meson_install('xkbcommon', build_dir)

def _png(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.png / 'build-target'
  ensure(build_dir)
  configure('png', build_dir, [
    f'--prefix={paths.prefix}',
    f'--host={info.target}',
    '--disable-shared',
    '--enable-static',
    *cflags_target(),
  ])
  make_default('png', build_dir, jobs)
  make_install('png', build_dir)

def _freetype_decycle(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.freetype / 'build-target-decycle'
  meson_setup('freetype (decycle)', paths.freetype, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dharfbuzz=disabled',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('freetype (decycle)', build_dir, jobs)
  meson_install('freetype (decycle)', build_dir)

def _harfbuzz(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.harfbuzz / 'build-target'
  meson_setup('harfbuzz', paths.harfbuzz, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dfreetype=enabled',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('harfbuzz', build_dir, jobs)
  meson_install('harfbuzz', build_dir)

def _freetype(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.freetype / 'build-target'
  meson_setup('freetype', paths.freetype, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dharfbuzz=enabled',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('freetype', build_dir, jobs)
  meson_install('freetype', build_dir)

def _fontconfig(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.fontconfig / 'build-target'
  meson_setup('fontconfig', paths.fontconfig, build_dir, [
    '--cross-file', f'{paths.root}/meson/{info.target}.txt',
    '--prefix', paths.prefix,
    '--default-library', 'static',
    '--prefer-static',
    '-Dcache-dir=/var/cache/fontconfig',
    '-Dtemplate-dir=/usr/share/fontconfig/conf.avail',
    '-Dbaseconfig-dir=/etc/fonts',
    '--buildtype', 'minsize', '--strip',
  ])
  meson_compile('fontconfig', build_dir, jobs)
  meson_install('fontconfig', build_dir)

  # merge libs -- workaround for Qt missing static library
  res = subprocess.run(['ar', '-M'], cwd = build_dir, input = (
    f'create {paths.prefix}/lib/libfontconfig.a\n'
    f'addlib {build_dir}/src/libfontconfig.a\n'
    f'addlib {paths.prefix}/lib/libexpat.a\n'
    f'addlib {paths.prefix}/lib/libfreetype.a\n'
    'save\n'
    'end\n'
  ).encode())
  if res.returncode != 0:
    raise Exception(f'Build fail: fontconfig merge libs returned {res.returncode}')

def _qtbase(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  linker_arg = 'gold'
  if info.arch in ('riscv64', 'loong64'):
    linker_arg = 'bfd'

  build_dir = paths.qtbase / 'build-target'
  ensure(build_dir)
  configure('qtbase', build_dir, [
    '-prefix', paths.prefix / 'qt',
    # configure meta
    # build options
    '-cmake-generator', 'Ninja',
    '-release',
    '-optimize-size',
    '-gc-binaries',
    '-static',
    '-platform', 'linux-g++',
    '-xplatform', 'devices/linux-generic-g++',
    '-device', 'linux-generic-g++',
    '-device-option', f'CROSS_COMPILE={info.target}-',
    '-qt-host-path', f'{paths.h_prefix}/qt',
    '-pch',
    '-no-ltcg',
    '-linker', linker_arg,
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
    f'CMAKE_TOOLCHAIN_FILE={paths.root}/cmake/{info.target}.cmake',
    f'CMAKE_PREFIX_PATH={paths.prefix}',
  ])
  cmake_build('qtbase', build_dir, jobs)
  cmake_install('qtbase', build_dir)

def _qtsvg(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qtsvg / 'build-target'
  ensure(build_dir)
  qt_configure_module('qtsvg', paths.qtsvg, build_dir, [
    f'CMAKE_PREFIX_PATH={paths.prefix}',
  ])
  cmake_build('qtsvg', build_dir, jobs)
  cmake_install('qtsvg', build_dir)

def _qttools(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qttools / 'build-target'
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
    f'CMAKE_PREFIX_PATH={paths.prefix}',
  ])
  cmake_build('qttools', build_dir, jobs)
  cmake_install('qttools', build_dir)

def _qttranslations(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qttranslations / 'build-target'
  ensure(build_dir)
  qt_configure_module('qttranslations', paths.qttranslations, build_dir, [
    f'CMAKE_PREFIX_PATH={paths.prefix}',
  ])
  cmake_build('qttranslations', build_dir, jobs)
  cmake_install('qttranslations', build_dir)

def _qtwayland(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.qtwayland / 'build-target'
  ensure(build_dir)
  qt_configure_module('qtwayland', paths.qtwayland, build_dir, [
    '-no-feature-wayland-server',
    f'CMAKE_PREFIX_PATH={paths.prefix}',
  ])
  cmake_build('qtwayland', build_dir, jobs)
  cmake_install('qtwayland', build_dir)

def _fcitx_qt(ver: str, paths: ProjectPaths, info: ProfileInfo, jobs: int):
  build_dir = paths.fcitx_qt / 'build-target'
  cmake_config('fcitx-qt', paths.fcitx_qt, build_dir, [
    f'-DCMAKE_TOOLCHAIN_FILE={paths.root}/cmake/{info.target}.cmake',
    '-DENABLE_QT5=Off',
    '-DENABLE_QT6=On',
    '-DBUILD_ONLY_PLUGIN=On',
    '-DBUILD_STATIC_PLUGIN=On',
    '-DCMAKE_BUILD_TYPE=MinSizeRel',
    f'-DCMAKE_PREFIX_PATH={paths.prefix}/qt;{paths.prefix}',
  ])
  cmake_build('fcitx-qt', build_dir, jobs)

  # fcitx-qt installs to host qt dir, even if specified `CMAKE_INSTALL_PREFIX`
  # here we do manual copy
  ime_dir = paths.prefix / 'qt/plugins/platforminputcontexts'
  ensure(ime_dir)
  copyfile(build_dir / 'qt6/platforminputcontext/libfcitx5platforminputcontextplugin.a', ime_dir / 'libfcitx5platforminputcontextplugin.a')

  # and generate missing plugin mkspec file
  mkspec_dir = paths.prefix / 'qt/mkspecs/modules'
  ibus_mkspec = open(mkspec_dir / 'qt_plugin_ibusplatforminputcontextplugin.pri', 'r').read()
  fcitx_mkspec = ibus_mkspec.replace('ibus', 'fcitx5').replace('Ibus', 'Fcitx5')
  with open(mkspec_dir / 'qt_plugin_fcitx5platforminputcontextplugin.pri', 'w') as f:
    f.write(fcitx_mkspec)

def build_target_lib(ver: BranchVersions, paths: ProjectPaths, info: ProfileInfo, config: argparse.Namespace):
  _expat(ver.expat, paths, info, config.jobs)
  _ffi(ver.ffi, paths, info, config.jobs)
  _fuse(ver.fuse, paths, info, config.jobs)
  _xml(ver.xml, paths, info, config.jobs)
  _z(ver.z, paths, info, config.jobs)
  _zstd(ver.zstd, paths, info, config.jobs)

  _squashfuse(ver.squashfuse, paths, info, config.jobs)
  _appimage_runtime(ver.appimage_runtime, paths, info, config.jobs)

  _dbus(ver.dbus, paths, info, config.jobs)
  old_pkg_config_libdir = os.environ['PKG_CONFIG_LIBDIR']
  os.environ['PKG_CONFIG_LIBDIR'] = f'{old_pkg_config_libdir}:{paths.h_prefix}/lib/pkgconfig'
  _wayland(ver.wayland, paths, info, config.jobs)
  os.environ['PKG_CONFIG_LIBDIR'] = old_pkg_config_libdir

  _xorg_proto(ver.xorg_proto, paths, info, config.jobs)
  _xau(ver.xau, paths, info, config.jobs)

  _xcb_proto(ver.xcb_proto, paths, info, config.jobs)
  _xcb(ver.xcb, paths, info, config.jobs)

  _xtrans(ver.xtrans, paths, info, config.jobs)
  _x(ver.x, paths, info, config.jobs)

  _xcb_util(ver.xcb_util, paths, info, config.jobs)
  _xcb_util_image(ver.xcb_util_image, paths, info, config.jobs)
  _xcb_util_keysyms(ver.xcb_util_keysyms, paths, info, config.jobs)
  _xcb_util_renderutil(ver.xcb_util_renderutil, paths, info, config.jobs)
  _xcb_util_wm(ver.xcb_util_wm, paths, info, config.jobs)
  _xcb_util_cursor(ver.xcb_util_cursor, paths, info, config.jobs)

  _xkbcommon(ver.xkbcommon, paths, info, config.jobs)

  _png(ver.png, paths, info, config.jobs)
  _freetype_decycle(ver.freetype, paths, info, config.jobs)
  _harfbuzz(ver.harfbuzz, paths, info, config.jobs)
  _freetype(ver.freetype, paths, info, config.jobs)
  _fontconfig(ver.fontconfig, paths, info, config.jobs)

  _qtbase(ver.qt, paths, info, config.jobs)
  old_path = os.environ['PATH']
  os.environ['PATH'] = f'{paths.prefix}/qt/bin:{old_path}'
  _qtsvg(ver.qt, paths, info, config.jobs)
  _qttools(ver.qt, paths, info, config.jobs)
  _qttranslations(ver.qt, paths, info, config.jobs)
  _qtwayland(ver.qt, paths, info, config.jobs)
  os.environ['PATH'] = old_path
  _fcitx_qt(ver.qt, paths, info, config.jobs)
