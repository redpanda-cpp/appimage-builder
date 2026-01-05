import argparse
from pathlib import Path
from typing import NamedTuple

from module.profile import BranchProfile

class SourcePaths(NamedTuple):
  appimage_runtime: Path
  binutils: Path
  dbus: Path
  expat: Path
  fcitx_qt: Path
  ffi: Path
  fontconfig: Path
  freetype: Path
  fuse: Path
  gcc: Path
  gmp: Path
  harfbuzz: Path
  linux: Path
  mimalloc: Path
  mpc: Path
  mpfr: Path
  musl: Path
  pkgconf: Path
  png: Path
  qtbase: Path
  qtsvg: Path
  qttools: Path
  qttranslations: Path
  qtwayland: Path
  squashfuse: Path
  wayland: Path
  x: Path
  xau: Path
  xcb: Path
  xcb_proto: Path
  xcb_util: Path
  xcb_util_cursor: Path
  xcb_util_image: Path
  xcb_util_keysyms: Path
  xcb_util_renderutil: Path
  xcb_util_wm: Path
  xkbcommon: Path
  xml: Path
  xorg_proto: Path
  xtrans: Path
  z: Path
  zstd: Path

class LayerPathsHost(NamedTuple):
  prefix: Path

  dbus: Path
  expat: Path
  ffi: Path
  gmp: Path
  meson: Path
  mpc: Path
  mpfr: Path
  qtbase: Path
  qttools: Path
  qtwayland: Path
  wayland: Path

class LayerPathsX(NamedTuple):
  prefix: Path

  binutils: Path
  cmake: Path
  gcc: Path
  linux: Path
  mimalloc: Path
  musl: Path
  pkgconf: Path

class LayerPathsTarget(NamedTuple):
  prefix: Path

  appimage_runtime: Path
  dbus: Path
  expat: Path
  fcitx_qt: Path
  ffi: Path
  fontconfig: Path
  freetype: Path
  freetype_decycle: Path
  fuse: Path
  harfbuzz: Path
  png: Path
  qtbase: Path
  qtsvg: Path
  qttools: Path
  qttranslations: Path
  qtwayland: Path
  squashfuse: Path
  wayland: Path
  x: Path
  xau: Path
  xcb: Path
  xcb_proto: Path
  xcb_util: Path
  xcb_util_cursor: Path
  xcb_util_image: Path
  xcb_util_keysyms: Path
  xcb_util_renderutil: Path
  xcb_util_wm: Path
  xkbcommon: Path
  xml: Path
  xorg_proto: Path
  xtrans: Path
  z: Path
  zstd: Path

class ProjectPaths:
  root_dir: Path

  assets_dir: Path
  dist_dir: Path
  patch_dir: Path

  build_dir: Path
  container_dir: Path
  layer_dir: Path

  cmake_cross_file: Path
  meson_cross_file: Path

  src_dir: SourcePaths
  src_arx: SourcePaths

  layer_host: LayerPathsHost
  layer_x: LayerPathsX
  layer_target: LayerPathsTarget

  def __init__(
    self,
    config: argparse.Namespace,
    ver: BranchProfile,
  ):
    self.root_dir = Path.cwd()

    self.assets_dir = self.root_dir / 'assets'
    self.dist_dir = self.root_dir / 'dist'
    self.patch_dir = self.root_dir / 'patch'

    self.build_dir = Path(f'/tmp/build/{ver.arch}')
    self.container_dir = self.root_dir / 'container' / ver.arch
    self.layer_dir = self.root_dir / 'layer' / ver.arch

    self.cmake_cross_file = self.root_dir / f'support/cmake/{ver.target}.cmake'
    self.meson_cross_file = self.root_dir / f'support/meson/{ver.target}.txt'

    self.src_dir = SourcePaths(
      appimage_runtime = self.build_dir / f'type2-runtime-{ver.appimage_runtime}',
      binutils = self.build_dir / f'binutils-{ver.binutils}',
      dbus = self.build_dir / f'dbus-{ver.dbus}',
      expat = self.build_dir / f'expat-{ver.expat}',
      fcitx_qt = self.build_dir / f'fcitx5-qt-{ver.fcitx_qt}',
      ffi = self.build_dir / f'libffi-{ver.ffi}',
      fontconfig = self.build_dir / f'fontconfig-{ver.fontconfig}',
      freetype = self.build_dir / f'freetype-{ver.freetype}',
      fuse = self.build_dir / f'fuse-{ver.fuse}',
      gcc = self.build_dir / f'gcc-{ver.gcc}',
      gmp = self.build_dir / f'gmp-{ver.gmp}',
      harfbuzz = self.build_dir / f'harfbuzz-{ver.harfbuzz}',
      linux = self.build_dir / f'linux-{ver.linux}',
      mimalloc = self.build_dir / f'mimalloc-{ver.mimalloc}',
      mpc = self.build_dir / f'mpc-{ver.mpc}',
      mpfr = self.build_dir / f'mpfr-{ver.mpfr}',
      musl = self.build_dir / f'musl-{ver.musl}',
      pkgconf = self.build_dir / f'pkgconf-pkgconf-{ver.pkgconf}',
      png = self.build_dir / f'libpng-{ver.png}',
      qtbase = self.build_dir / f'qtbase-everywhere-src-{ver.qt}',
      qtsvg = self.build_dir / f'qtsvg-everywhere-src-{ver.qt}',
      qttools = self.build_dir / f'qttools-everywhere-src-{ver.qt}',
      qttranslations = self.build_dir / f'qttranslations-everywhere-src-{ver.qt}',
      qtwayland = self.build_dir / f'qtwayland-everywhere-src-{ver.qt}',
      squashfuse = self.build_dir / f'squashfuse-{ver.squashfuse}',
      wayland = self.build_dir / f'wayland-{ver.wayland}',
      x = self.build_dir / f'libX11-{ver.x}',
      xau = self.build_dir / f'libXau-{ver.xau}',
      xcb = self.build_dir / f'libxcb-{ver.xcb}',
      xcb_proto = self.build_dir / f'xcb-proto-{ver.xcb_proto}',
      xcb_util = self.build_dir / f'xcb-util-{ver.xcb_util}',
      xcb_util_cursor = self.build_dir / f'xcb-util-cursor-{ver.xcb_util_cursor}',
      xcb_util_image = self.build_dir / f'xcb-util-image-{ver.xcb_util_image}',
      xcb_util_keysyms = self.build_dir / f'xcb-util-keysyms-{ver.xcb_util_keysyms}',
      xcb_util_renderutil = self.build_dir / f'xcb-util-renderutil-{ver.xcb_util_renderutil}',
      xcb_util_wm = self.build_dir / f'xcb-util-wm-{ver.xcb_util_wm}',
      xkbcommon = self.build_dir / f'libxkbcommon-xkbcommon-{ver.xkbcommon}',
      xml = self.build_dir / f'libxml2-{ver.xml}',
      xorg_proto = self.build_dir / f'xorgproto-{ver.xorg_proto}',
      xtrans = self.build_dir / f'xtrans-{ver.xtrans}',
      z = self.build_dir / f'zlib-{ver.z}',
      zstd = self.build_dir / f'zstd-{ver.zstd}',
    )

    self.src_arx = SourcePaths(
      appimage_runtime = self.assets_dir / f'type2-runtime-{ver.appimage_runtime}.tar.gz',
      binutils = self.assets_dir / f'binutils-{ver.binutils}.tar.zst',
      dbus = self.assets_dir / f'dbus-{ver.dbus}.tar.xz',
      expat = self.assets_dir / f'expat-{ver.expat}.tar.xz',
      fcitx_qt = self.assets_dir / f'fcitx5-qt-{ver.fcitx_qt}.tar.gz',
      ffi = self.assets_dir / f'libffi-{ver.ffi}.tar.gz',
      fontconfig = self.assets_dir / f'fontconfig-{ver.fontconfig}.tar.xz',
      freetype = self.assets_dir / f'freetype-{ver.freetype}.tar.xz',
      fuse = self.assets_dir / f'fuse-{ver.fuse}.tar.gz',
      gcc = self.assets_dir / f'gcc-{ver.gcc}.tar.xz',
      gmp = self.assets_dir / f'gmp-{ver.gmp}.tar.zst',
      harfbuzz = self.assets_dir / f'harfbuzz-{ver.harfbuzz}.tar.xz',
      linux = self.assets_dir / f'linux-{ver.linux}.tar.xz',
      mimalloc = self.assets_dir / f'mimalloc-{ver.mimalloc}.tar.gz',
      mpc = self.assets_dir / f'mpc-{ver.mpc}.tar.gz',
      mpfr = self.assets_dir / f'mpfr-{ver.mpfr}.tar.xz',
      musl = self.assets_dir / f'musl-{ver.musl}.tar.gz',
      pkgconf = self.assets_dir / f'pkgconf-pkgconf-{ver.pkgconf}.tar.gz',
      png = self.assets_dir / f'libpng-{ver.png}.tar.xz',
      qtbase = self.assets_dir / f'qtbase-everywhere-src-{ver.qt}.tar.xz',
      qtsvg = self.assets_dir / f'qtsvg-everywhere-src-{ver.qt}.tar.xz',
      qttools = self.assets_dir / f'qttools-everywhere-src-{ver.qt}.tar.xz',
      qttranslations = self.assets_dir / f'qttranslations-everywhere-src-{ver.qt}.tar.xz',
      qtwayland = self.assets_dir / f'qtwayland-everywhere-src-{ver.qt}.tar.xz',
      squashfuse = self.assets_dir / f'squashfuse-{ver.squashfuse}.tar.gz',
      wayland = self.assets_dir / f'wayland-{ver.wayland}.tar.xz',
      x = self.assets_dir / f'libX11-{ver.x}.tar.xz',
      xau = self.assets_dir / f'libXau-{ver.xau}.tar.xz',
      xcb = self.assets_dir / f'libxcb-{ver.xcb}.tar.xz',
      xcb_proto = self.assets_dir / f'xcb-proto-{ver.xcb_proto}.tar.xz',
      xcb_util = self.assets_dir / f'xcb-util-{ver.xcb_util}.tar.xz',
      xcb_util_cursor = self.assets_dir / f'xcb-util-cursor-{ver.xcb_util_cursor}.tar.xz',
      xcb_util_image = self.assets_dir / f'xcb-util-image-{ver.xcb_util_image}.tar.xz',
      xcb_util_keysyms = self.assets_dir / f'xcb-util-keysyms-{ver.xcb_util_keysyms}.tar.xz',
      xcb_util_renderutil = self.assets_dir / f'xcb-util-renderutil-{ver.xcb_util_renderutil}.tar.xz',
      xcb_util_wm = self.assets_dir / f'xcb-util-wm-{ver.xcb_util_wm}.tar.xz',
      xkbcommon = self.assets_dir / f'libxkbcommon-xkbcommon-{ver.xkbcommon}.tar.gz',
      xml = self.assets_dir / f'libxml2-{ver.xml}.tar.xz',
      xorg_proto = self.assets_dir / f'xorgproto-{ver.xorg_proto}.tar.xz',
      xtrans = self.assets_dir / f'xtrans-{ver.xtrans}.tar.xz',
      z = self.assets_dir / f'zlib-{ver.z}.tar.gz',
      zstd = self.assets_dir / f'zstd-{ver.zstd}.tar.zst',
    )

    layer_host_prefix = self.layer_dir / 'host'
    self.layer_host = LayerPathsHost(
      prefix = layer_host_prefix,

      dbus = layer_host_prefix / 'dbus',
      expat = layer_host_prefix / 'expat',
      ffi = layer_host_prefix / 'libffi',
      gmp = layer_host_prefix / 'gmp',
      meson = layer_host_prefix / 'meson',
      mpc = layer_host_prefix / 'mpc',
      mpfr = layer_host_prefix / 'mpfr',
      qtbase = layer_host_prefix / 'qtbase',
      qttools = layer_host_prefix / 'qttools',
      qtwayland = layer_host_prefix / 'qtwayland',
      wayland = layer_host_prefix / 'wayland',
    )

    layer_x_prefix = self.layer_dir / 'x'
    self.layer_x = LayerPathsX(
      prefix = layer_x_prefix,

      binutils = layer_x_prefix / 'binutils',
      cmake = layer_x_prefix / 'cmake',
      gcc = layer_x_prefix / 'gcc',
      linux = layer_x_prefix / 'linux',
      mimalloc = layer_x_prefix / 'mimalloc',
      musl = layer_x_prefix / 'musl',
      pkgconf = layer_x_prefix / 'pkgconf',
    )

    layer_target_prefix = self.layer_dir / 'target'
    self.layer_target = LayerPathsTarget(
      prefix = layer_target_prefix,

      appimage_runtime = layer_target_prefix / 'type2-runtime',
      dbus = layer_target_prefix / 'dbus',
      expat = layer_target_prefix / 'expat',
      fcitx_qt = layer_target_prefix / 'fcitx5-qt',
      ffi = layer_target_prefix / 'libffi',
      fontconfig = layer_target_prefix / 'fontconfig',
      freetype = layer_target_prefix / 'freetype',
      freetype_decycle = layer_target_prefix / 'freetype-decycle',
      fuse = layer_target_prefix / 'fuse',
      harfbuzz = layer_target_prefix / 'harfbuzz',
      png = layer_target_prefix / 'libpng',
      qtbase = layer_target_prefix / 'qtbase',
      qtsvg = layer_target_prefix / 'qtsvg',
      qttools = layer_target_prefix / 'qttools',
      qttranslations = layer_target_prefix / 'qttranslations',
      qtwayland = layer_target_prefix / 'qtwayland',
      squashfuse = layer_target_prefix / 'squashfuse',
      wayland = layer_target_prefix / 'wayland',
      x = layer_target_prefix / 'libX11',
      xau = layer_target_prefix / 'libXau',
      xcb = layer_target_prefix / 'libxcb',
      xcb_proto = layer_target_prefix / 'xcb-proto',
      xcb_util = layer_target_prefix / 'xcb-util',
      xcb_util_cursor = layer_target_prefix / 'xcb-util-cursor',
      xcb_util_image = layer_target_prefix / 'xcb-util-image',
      xcb_util_keysyms = layer_target_prefix / 'xcb-util-keysyms',
      xcb_util_renderutil = layer_target_prefix / 'xcb-util-renderutil',
      xcb_util_wm = layer_target_prefix / 'xcb-util-wm',
      xkbcommon = layer_target_prefix / 'libxkbcommon',
      xml = layer_target_prefix / 'libxml2',
      xorg_proto = layer_target_prefix / 'xorgproto',
      xtrans = layer_target_prefix / 'xtrans',
      z = layer_target_prefix / 'zlib',
      zstd = layer_target_prefix / 'zstd',
    )
