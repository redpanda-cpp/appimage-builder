import argparse

class BranchVersions:
  appimage_runtime: str = '01164bfcbc8dd2bd0d7e3706f97035108d6b91ba'
  binutils: str = '2.43.1'
  dbus: str = '1.14.10'
  expat: str = '2.6.4'
  fcitx_qt: str = '5.1.8'
  ffi: str = '3.4.6'
  fontconfig: str = '2.15.0'
  freetype: str = '2.13.3'
  fuse: str = '3.16.2'
  gcc: str = '14.2.0'
  gmp: str = '6.3.0'
  harfbuzz: str = '10.1.0'
  linux_headers: str = '4.19.88-2'
  mpc: str = '1.3.1'
  mpfr: str = '4.2.1'
  musl: str = '1.2.5'
  pkgconf: str = '2.5.1'
  png: str = '1.6.44'
  qt: str = '6.8.1'
  squashfuse: str = '0.5.2'
  wayland: str = '1.23.1'
  x: str = '1.8.10'
  xau: str = '1.0.11'
  xcb: str = '1.17.0'
  xcb_proto: str = '1.17.0'
  xcb_util: str = '0.4.1'
  xcb_util_cursor: str = '0.1.5'
  xcb_util_image: str = '0.4.1'
  xcb_util_keysyms: str = '0.4.1'
  xcb_util_renderutil: str = '0.3.10'
  xcb_util_wm: str = '0.4.2'
  xkbcommon: str = '1.7.0'
  xml: str = '2.13.5'
  xorg_proto: str = '2024.1'
  xtrans: str = '1.5.2'
  z: str = '1.3.1'
  zstd: str = '1.5.6'

  def __init__(
    self,

    musl: str,
  ):
    self.musl = musl

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
  ),
  'time32': BranchVersions(
    musl = '1.1.24',
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

def resolve_profile(config: argparse.Namespace) -> BranchProfile:
  return BranchProfile(
    ver = BRANCHES[config.branch],
    info = PROFILES[config.arch],
  )
