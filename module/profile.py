class BranchVersions:
  appimage_runtime: str
  binutils: str
  dbus: str
  expat: str
  fcitx_qt: str
  ffi: str
  fontconfig: str
  freetype: str
  fuse: str
  gcc: str
  gmp: str
  harfbuzz: str
  linux_headers: str
  mpc: str
  mpfr: str
  musl: str
  png: str
  qt: str
  squashfuse: str
  wayland: str
  x: str
  xau: str
  xcb: str
  xcb_proto: str
  xcb_util: str
  xcb_util_cursor: str
  xcb_util_image: str
  xcb_util_keysyms: str
  xcb_util_renderutil: str
  xcb_util_wm: str
  xkbcommon: str
  xml: str
  xorg_proto: str
  xtrans: str
  z: str
  zstd: str

  def __init__(
    self,
    appimage_runtime: str,
    binutils: str,
    dbus: str,
    expat: str,
    fcitx_qt: str,
    ffi: str,
    fontconfig: str,
    freetype: str,
    fuse: str,
    gcc: str,
    gmp: str,
    harfbuzz: str,
    linux_headers: str,
    mpc: str,
    mpfr: str,
    musl: str,
    png: str,
    qt: str,
    squashfuse: str,
    wayland: str,
    x: str,
    xau: str,
    xcb: str,
    xcb_proto: str,
    xcb_util: str,
    xcb_util_cursor: str,
    xcb_util_image: str,
    xcb_util_keysyms: str,
    xcb_util_renderutil: str,
    xcb_util_wm: str,
    xkbcommon: str,
    xml: str,
    xorg_proto: str,
    xtrans: str,
    z: str,
    zstd: str,
  ):
    self.appimage_runtime = appimage_runtime
    self.binutils = binutils
    self.dbus = dbus
    self.expat = expat
    self.fcitx_qt = fcitx_qt
    self.ffi = ffi
    self.fontconfig = fontconfig
    self.freetype = freetype
    self.fuse = fuse
    self.gcc = gcc
    self.gmp = gmp
    self.harfbuzz = harfbuzz
    self.linux_headers = linux_headers
    self.mpc = mpc
    self.mpfr = mpfr
    self.musl = musl
    self.png = png
    self.qt = qt
    self.squashfuse = squashfuse
    self.wayland = wayland
    self.x = x
    self.xau = xau
    self.xcb = xcb
    self.xcb_proto = xcb_proto
    self.xcb_util = xcb_util
    self.xcb_util_cursor = xcb_util_cursor
    self.xcb_util_image = xcb_util_image
    self.xcb_util_keysyms = xcb_util_keysyms
    self.xcb_util_renderutil = xcb_util_renderutil
    self.xcb_util_wm = xcb_util_wm
    self.xkbcommon = xkbcommon
    self.xml = xml
    self.xorg_proto = xorg_proto
    self.xtrans = xtrans
    self.z = z
    self.zstd = zstd

class ProfileInfo:
  arch: str
  host: str
  kernel_arch: str
  target: str

  def __init__(
    self,
    arch: str,
    triplet_arch: str,
    kernel_arch: str,
  ):
    self.arch = arch
    self.host = 'x86_64-linux-gnu'
    self.kernel_arch = kernel_arch
    self.target = f'{triplet_arch}-linux-musl'

class FullProfile:
  ver: BranchVersions
  info: ProfileInfo

  def __init__(
    self,
    ver: BranchVersions,
    info: ProfileInfo
  ):
    self.ver = ver
    self.info = info

BRANCHES = {
  'main': BranchVersions(
    appimage_runtime = '01164bfcbc8dd2bd0d7e3706f97035108d6b91ba',
    binutils = '2.43.1',
    dbus = '1.14.10',
    expat = '2.6.4',
    fcitx_qt = '5.1.8',
    ffi = '3.4.6',
    fontconfig = '2.15.0',
    freetype = '2.13.3',
    fuse = '3.16.2',
    gcc = '14.2.0',
    gmp = '6.3.0',
    harfbuzz = '10.1.0',
    linux_headers = '4.19.88-2',
    mpc = '1.3.1',
    mpfr = '4.2.1',
    musl = '1.2.5',
    png = '1.6.44',
    qt = '6.8.1',
    squashfuse = '0.5.2',
    wayland = '1.23.1',
    x = '1.8.10',
    xau = '1.0.11',
    xcb = '1.17.0',
    xcb_proto = '1.17.0',
    xcb_util = '0.4.1',
    xcb_util_cursor = '0.1.5',
    xcb_util_image = '0.4.1',
    xcb_util_keysyms = '0.4.1',
    xcb_util_renderutil = '0.3.10',
    xcb_util_wm = '0.4.2',
    xkbcommon = '1.7.0',
    xml = '2.13.5',
    xorg_proto = '2024.1',
    xtrans = '1.5.2',
    z = '1.3.1',
    zstd = '1.5.6',
  ),
  'time32': BranchVersions(
    appimage_runtime = '01164bfcbc8dd2bd0d7e3706f97035108d6b91ba',
    binutils = '2.43.1',
    dbus = '1.14.10',
    expat = '2.6.4',
    fcitx_qt = '5.1.8',
    ffi = '3.4.6',
    fontconfig = '2.15.0',
    freetype = '2.13.3',
    fuse = '3.16.2',
    gcc = '14.2.0',
    gmp = '6.3.0',
    harfbuzz = '10.1.0',
    linux_headers = '4.19.88-2',
    mpc = '1.3.1',
    mpfr = '4.2.1',
    musl = '1.1.24',
    png = '1.6.44',
    qt = '6.8.1',
    squashfuse = '0.5.2',
    wayland = '1.23.1',
    x = '1.8.10',
    xau = '1.0.11',
    xcb = '1.17.0',
    xcb_proto = '1.17.0',
    xcb_util = '0.4.1',
    xcb_util_cursor = '0.1.5',
    xcb_util_image = '0.4.1',
    xcb_util_keysyms = '0.4.1',
    xcb_util_renderutil = '0.3.10',
    xcb_util_wm = '0.4.2',
    xkbcommon = '1.7.0',
    xml = '2.13.5',
    xorg_proto = '2024.1',
    xtrans = '1.5.2',
    z = '1.3.1',
    zstd = '1.5.6',
  ),
}

PROFILES = {
  'x86_64': ProfileInfo(
    arch = 'x86_64',
    triplet_arch = 'x86_64',
    kernel_arch = 'x86',
  ),
  'aarch64': ProfileInfo(
    arch = 'aarch64',
    triplet_arch = 'aarch64',
    kernel_arch = 'arm64',
  ),
  'riscv64': ProfileInfo(
    arch = 'riscv64',
    triplet_arch = 'riscv64',
    kernel_arch = 'riscv',
  ),
  'loong64': ProfileInfo(
    arch = 'loong64',
    triplet_arch = 'loongarch64',
    kernel_arch = 'riscv',
  ),
  'i686': ProfileInfo(
    arch = 'i686',
    triplet_arch = 'i686',
    kernel_arch = 'x86',
  ),
  'armv7l': ProfileInfo(
    arch = 'armv7l',
    triplet_arch = 'armv7l',
    kernel_arch = 'arm',
  ),
}

def get_full_profile(config) -> FullProfile:
  return FullProfile(
    ver = BRANCHES[config.branch],
    info = PROFILES[config.arch],
  )
