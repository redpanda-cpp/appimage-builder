import argparse

class BranchVersions:
  musl: str
  qt: str

  appimage_runtime: str = 'caf24f9f712084686bfc24a70b75e50df0aefb9c'
  binutils: str = '2.45.1'
  dbus: str = '1.16.2'
  expat: str = '2.7.3'
  fcitx_qt: str = '5.1.12'
  ffi: str = '3.5.2'
  fontconfig: str = '2.17.1'
  freetype: str = '2.14.1'
  fuse: str = '3.18.1'
  gcc: str = '15.2.0'
  gmp: str = '6.3.0'
  harfbuzz: str = '12.3.0'
  linux: str = '6.18.3'
  meson: str = '1.10.0'
  mimalloc: str = '3.0.11'
  mpc: str = '1.3.1'
  mpfr: str = '4.2.2'
  pkgconf: str = '2.5.1'
  png: str = '1.6.53'
  squashfuse: str = '0.6.1'
  wayland: str = '1.24.0'
  x: str = '1.8.12'
  xau: str = '1.0.12'
  xcb: str = '1.17.0'
  xcb_proto: str = '1.17.0'
  xcb_util: str = '0.4.1'
  xcb_util_cursor: str = '0.1.6'
  xcb_util_image: str = '0.4.1'
  xcb_util_keysyms: str = '0.4.1'
  xcb_util_renderutil: str = '0.3.10'
  xcb_util_wm: str = '0.4.2'
  xkbcommon: str = '1.13.1'
  xml: str = '2.15.1'
  xorg_proto: str = '2025.1'
  xtrans: str = '1.6.0'
  z: str = '1.3.1'
  zstd: str = '1.5.7'

  def __init__(
    self,

    musl: str,
    qt: str,
  ):
    self.musl = musl
    self.qt = qt

class ProfileInfo:
  arch: str
  kernel_arch: str
  target: str

  def __init__(
    self,
    arch: str,
    triplet_arch: str,
    kernel_arch: str,
  ):
    self.arch = arch
    self.kernel_arch = kernel_arch
    self.target = f'{triplet_arch}-linux-musl'

class BranchProfile(BranchVersions):
  arch: str
  kernel_arch: str
  target: str

  def __init__(
    self,
    ver: BranchVersions,
    info: ProfileInfo,
  ):
    BranchVersions.__init__(self, **ver.__dict__)

    self.arch = info.arch
    self.kernel_arch = info.kernel_arch
    self.target = info.target

BRANCHES = {
  'main': BranchVersions(
    musl = '1.2.5',
    qt = '6.10.1',
  ),
  'time32': BranchVersions(
    musl = '1.1.24',
    qt = '6.8.3',
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
    kernel_arch = 'loongarch',
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

def resolve_profile(config: argparse.Namespace) -> BranchProfile:
  return BranchProfile(
    ver = BRANCHES[config.branch],
    info = PROFILES[config.arch],
  )
