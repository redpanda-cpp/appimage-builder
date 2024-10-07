import argparse
from pathlib import Path

from module.profile import BranchVersions, ProfileInfo

class ProjectPaths:
  root: Path

  assets: Path
  dist: Path
  patch: Path

  build: Path
  container: Path
  h_prefix: Path
  prefix: Path

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
  linux_headers: Path
  mpc: Path
  mpfr: Path
  musl: Path
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

  appimage_runtime_arx: Path
  binutils_arx: Path
  dbus_arx: Path
  expat_arx: Path
  fcitx_qt_arx: Path
  ffi_arx: Path
  fontconfig_arx: Path
  freetype_arx: Path
  fuse_arx: Path
  gcc_arx: Path
  gmp_arx: Path
  harfbuzz_arx: Path
  linux_headers_arx: Path
  mpc_arx: Path
  mpfr_arx: Path
  musl_arx: Path
  png_arx: Path
  qtbase_arx: Path
  qtsvg_arx: Path
  qttools_arx: Path
  qttranslations_arx: Path
  qtwayland_arx: Path
  squashfuse_arx: Path
  wayland_arx: Path
  x_arx: Path
  xau_arx: Path
  xcb_arx: Path
  xcb_proto_arx: Path
  xcb_util_arx: Path
  xcb_util_cursor_arx: Path
  xcb_util_image_arx: Path
  xcb_util_keysyms_arx: Path
  xcb_util_renderutil_arx: Path
  xcb_util_wm_arx: Path
  xkbcommon_arx: Path
  xml_arx: Path
  xorg_proto_arx: Path
  xtrans_arx: Path
  z_arx: Path
  zstd_arx: Path

  def __init__(
    self,
    config: argparse.Namespace,
    ver: BranchVersions,
    info: ProfileInfo,
  ):
    self.root = Path.cwd()

    self.assets = self.root / 'assets'
    self.dist = self.root / 'dist'
    self.patch = self.root / 'patch'

    self.build = Path(f'/tmp/build/{info.arch}')
    self.container = self.root / 'container' / info.arch
    self.h_prefix = Path(f'/opt/qt-{info.arch}')
    self.prefix = Path(f'/opt/qt-{info.arch}/{info.target}')

    appimage_runtime = f'type2-runtime-{ver.appimage_runtime}'
    self.appimage_runtime = self.build / appimage_runtime
    self.appimage_runtime_arx = self.assets / f'{appimage_runtime}.tar.gz'

    binutils = f'binutils-{ver.binutils}'
    self.binutils = self.build / binutils
    self.binutils_arx = self.assets / f'{binutils}.tar.zst'

    dbus = f'dbus-{ver.dbus}'
    self.dbus = self.build / dbus
    self.dbus_arx = self.assets / f'{dbus}.tar.xz'

    expat = f'expat-{ver.expat}'
    self.expat = self.build / expat
    self.expat_arx = self.assets / f'{expat}.tar.xz'

    fcitx_qt = f'fcitx5-qt-{ver.fcitx_qt}'
    self.fcitx_qt = self.build / fcitx_qt
    self.fcitx_qt_arx = self.assets / f'{fcitx_qt}.tar.gz'

    ffi = f'libffi-{ver.ffi}'
    self.ffi = self.build / ffi
    self.ffi_arx = self.assets / f'{ffi}.tar.gz'

    fontconfig = f'fontconfig-{ver.fontconfig}'
    self.fontconfig = self.build / fontconfig
    self.fontconfig_arx = self.assets / f'{fontconfig}.tar.gz'

    freetype = f'freetype-{ver.freetype}'
    self.freetype = self.build / freetype
    self.freetype_arx = self.assets / f'{freetype}.tar.xz'

    fuse = f'fuse-{ver.fuse}'
    self.fuse = self.build / fuse
    self.fuse_arx = self.assets / f'{fuse}.tar.gz'

    gcc = f'gcc-{ver.gcc}'
    self.gcc = self.build / gcc
    self.gcc_arx = self.assets / f'{gcc}.tar.xz'

    gmp = f'gmp-{ver.gmp}'
    self.gmp = self.build / gmp
    self.gmp_arx = self.assets / f'{gmp}.tar.zst'

    harfbuzz = f'harfbuzz-{ver.harfbuzz}'
    self.harfbuzz = self.build / harfbuzz
    self.harfbuzz_arx = self.assets / f'{harfbuzz}.tar.xz'

    linux_headers = f'linux-headers-{ver.linux_headers}'
    self.linux_headers = self.build / linux_headers
    self.linux_headers_arx = self.assets / f'{linux_headers}.tar.xz'

    mpc = f'mpc-{ver.mpc}'
    self.mpc = self.build / mpc
    self.mpc_arx = self.assets / f'{mpc}.tar.gz'

    mpfr = f'mpfr-{ver.mpfr}'
    self.mpfr = self.build / mpfr
    self.mpfr_arx = self.assets / f'{mpfr}.tar.xz'

    musl = f'musl-{ver.musl}'
    self.musl = self.build / musl
    self.musl_arx = self.assets / f'{musl}.tar.gz'

    png = f'libpng-{ver.png}'
    self.png = self.build / png
    self.png_arx = self.assets / f'{png}.tar.xz'

    qtbase = f'qtbase-everywhere-src-{ver.qt}'
    self.qtbase = self.build / qtbase
    self.qtbase_arx = self.assets / f'{qtbase}.tar.xz'

    qtsvg = f'qtsvg-everywhere-src-{ver.qt}'
    self.qtsvg = self.build / qtsvg
    self.qtsvg_arx = self.assets / f'{qtsvg}.tar.xz'

    qttools = f'qttools-everywhere-src-{ver.qt}'
    self.qttools = self.build / qttools
    self.qttools_arx = self.assets / f'{qttools}.tar.xz'

    qttranslations = f'qttranslations-everywhere-src-{ver.qt}'
    self.qttranslations = self.build / qttranslations
    self.qttranslations_arx = self.assets / f'{qttranslations}.tar.xz'

    qtwayland = f'qtwayland-everywhere-src-{ver.qt}'
    self.qtwayland = self.build / qtwayland
    self.qtwayland_arx = self.assets / f'{qtwayland}.tar.xz'

    squashfuse = f'squashfuse-{ver.squashfuse}'
    self.squashfuse = self.build / squashfuse
    self.squashfuse_arx = self.assets / f'{squashfuse}.tar.gz'

    wayland = f'wayland-{ver.wayland}'
    self.wayland = self.build / wayland
    self.wayland_arx = self.assets / f'{wayland}.tar.xz'

    x = f'libX11-{ver.x}'
    self.x = self.build / x
    self.x_arx = self.assets / f'{x}.tar.xz'

    xau = f'libXau-{ver.xau}'
    self.xau = self.build / xau
    self.xau_arx = self.assets / f'{xau}.tar.xz'

    xcb = f'libxcb-{ver.xcb}'
    self.xcb = self.build / xcb
    self.xcb_arx = self.assets / f'{xcb}.tar.xz'

    xcb_proto = f'xcb-proto-{ver.xcb_proto}'
    self.xcb_proto = self.build / xcb_proto
    self.xcb_proto_arx = self.assets / f'{xcb_proto}.tar.xz'

    xcb_util = f'xcb-util-{ver.xcb_util}'
    self.xcb_util = self.build / xcb_util
    self.xcb_util_arx = self.assets / f'{xcb_util}.tar.xz'

    xcb_util_cursor = f'xcb-util-cursor-{ver.xcb_util_cursor}'
    self.xcb_util_cursor = self.build / xcb_util_cursor
    self.xcb_util_cursor_arx = self.assets / f'{xcb_util_cursor}.tar.xz'

    xcb_util_image = f'xcb-util-image-{ver.xcb_util_image}'
    self.xcb_util_image = self.build / xcb_util_image
    self.xcb_util_image_arx = self.assets / f'{xcb_util_image}.tar.xz'

    xcb_util_keysyms = f'xcb-util-keysyms-{ver.xcb_util_keysyms}'
    self.xcb_util_keysyms = self.build / xcb_util_keysyms
    self.xcb_util_keysyms_arx = self.assets / f'{xcb_util_keysyms}.tar.xz'

    xcb_util_renderutil = f'xcb-util-renderutil-{ver.xcb_util_renderutil}'
    self.xcb_util_renderutil = self.build / xcb_util_renderutil
    self.xcb_util_renderutil_arx = self.assets / f'{xcb_util_renderutil}.tar.xz'

    xcb_util_wm = f'xcb-util-wm-{ver.xcb_util_wm}'
    self.xcb_util_wm = self.build / xcb_util_wm
    self.xcb_util_wm_arx = self.assets / f'{xcb_util_wm}.tar.xz'

    xkbcommon = f'libxkbcommon-{ver.xkbcommon}'
    self.xkbcommon = self.build / xkbcommon
    self.xkbcommon_arx = self.assets / f'{xkbcommon}.tar.xz'

    xml = f'libxml2-{ver.xml}'
    self.xml = self.build / xml
    self.xml_arx = self.assets / f'{xml}.tar.xz'

    xorg_proto = f'xorgproto-{ver.xorg_proto}'
    self.xorg_proto = self.build / xorg_proto
    self.xorg_proto_arx = self.assets / f'{xorg_proto}.tar.xz'

    xtrans = f'xtrans-{ver.xtrans}'
    self.xtrans = self.build / xtrans
    self.xtrans_arx = self.assets / f'{xtrans}.tar.xz'

    z = f'zlib-{ver.z}'
    self.z = self.build / z
    self.z_arx = self.assets / f'{z}.tar.gz'

    zstd = f'zstd-{ver.zstd}'
    self.zstd = self.build / zstd
    self.zstd_arx = self.assets / f'{zstd}.tar.zst'
