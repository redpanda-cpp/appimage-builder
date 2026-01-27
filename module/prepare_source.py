from hashlib import sha256
import logging
from packaging.version import Version
from pathlib import Path
import subprocess
from urllib.error import URLError
from urllib.request import urlopen

from module.checksum import CHECKSUMS
from module.path import ProjectPaths
from module.profile import BranchProfile


def _validate_and_download(path: Path, url: str):
  MAX_RETRY = 3
  checksum = CHECKSUMS[path.name]
  if path.exists():
    with open(path, 'rb') as f:
      body = f.read()
      if checksum != sha256(body).hexdigest():
        message = 'Validate fail: %s exists but checksum mismatch' % path.name
        logging.critical(message)
        logging.info('Please delete %s and try again' % path.name)
        raise Exception(message)
  else:
    logging.info('Downloading %s' % path.name)
    retry_count = 0
    while True:
      retry_count += 1
      try:
        response = urlopen(url)
        body = response.read()
        if checksum != sha256(body).hexdigest():
          message = 'Download fail: checksum mismatch for %s' % path.name
          logging.critical(message)
          raise Exception(message)
        with open(path, "wb") as f:
          f.write(body)
          return
      except URLError as e:
        message = 'Download fail: %s for %s (retry %d/3)' % (e.reason, path.name, retry_count)
        if retry_count < MAX_RETRY:
          logging.warning(message)
          logging.warning('Retrying...')
        else:
          logging.critical(message)
          raise e

def _check_and_extract(path: Path, arx: Path):
  # check if already extracted
  if path.exists():
    mark = path / '.patched'
    if mark.exists():
      return False
    else:
      message = 'Extract fail: %s exists but not marked as fully patched' % path.name
      logging.critical(message)
      logging.info('Please delete %s and try again' % path.name)
      raise Exception(message)

  # extract
  res = subprocess.run([
    'bsdtar',
    '-xf',
    arx,
    '--no-same-owner',
  ], cwd = path.parent)
  if res.returncode != 0:
    message = 'Extract fail: bsdtar returned %d extracting %s' % (res.returncode, arx.name)
    logging.critical(message)
    raise Exception(message)

  return True

def _patch(path: Path, patch: Path):
  res = subprocess.run([
    'patch',
    '-Np1',
    '-i', patch,
  ], cwd = path)
  if res.returncode != 0:
    message = 'Patch fail: applying %s to %s' % (patch.name, path.name)
    logging.critical(message)
    raise Exception(message)

def _sed(path: Path, command: str):
  res = subprocess.run([
    'sed',
    '-i',
    command,
    path,
  ])
  if res.returncode != 0:
    message = 'Sed fail: %s' % path.name
    logging.critical(message)
    raise Exception(message)

def _autoreconf(path: Path):
  res = subprocess.run([
    'autoreconf',
    '-fi',
  ], cwd = path)
  if res.returncode != 0:
    message = 'Autoreconf fail: %s' % path.name
    logging.critical(message)
    raise Exception(message)

def _automake(path: Path):
  res = subprocess.run([
    'automake',
  ], cwd = path)
  if res.returncode != 0:
    message = 'Automake fail: %s' % path.name
    logging.critical(message)
    raise Exception(message)

def _patch_done(path: Path):
  mark = path / '.patched'
  mark.touch()

def _appimage_runtime(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/AppImage/type2-runtime/archive/{ver.appimage_runtime}.tar.gz'
  _validate_and_download(paths.src_arx.appimage_runtime, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.appimage_runtime, paths.src_arx.appimage_runtime)
  _patch_done(paths.src_dir.appimage_runtime)

def _binutils(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://ftpmirror.gnu.org/gnu/binutils/{paths.src_arx.binutils.name}'
  _validate_and_download(paths.src_arx.binutils, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.binutils, paths.src_arx.binutils)
  _patch_done(paths.src_dir.binutils)

def _dbus(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://dbus.freedesktop.org/releases/dbus/{paths.src_arx.dbus.name}'
  _validate_and_download(paths.src_arx.dbus, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.dbus, paths.src_arx.dbus)
  _patch_done(paths.src_dir.dbus)

def _expat(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  tag = 'R_' + ver.expat.replace('.', '_')
  url = f'https://github.com/libexpat/libexpat/releases/download/{tag}/{paths.src_arx.expat.name}'
  _validate_and_download(paths.src_arx.expat, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.expat, paths.src_arx.expat)
  _patch_done(paths.src_dir.expat)

def _fcitx_qt(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/fcitx/fcitx5-qt/archive/refs/tags/{ver.fcitx_qt}.tar.gz'
  _validate_and_download(paths.src_arx.fcitx_qt, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.fcitx_qt, paths.src_arx.fcitx_qt)
  _patch_done(paths.src_dir.fcitx_qt)

def _ffi(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/libffi/libffi/releases/download/v{ver.ffi}/{paths.src_arx.ffi.name}'
  _validate_and_download(paths.src_arx.ffi, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.ffi, paths.src_arx.ffi)
  _patch_done(paths.src_dir.ffi)

def _fontconfig(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://gitlab.freedesktop.org/api/v4/projects/890/packages/generic/fontconfig/{ver.fontconfig}/{paths.src_arx.fontconfig.name}'
  _validate_and_download(paths.src_arx.fontconfig, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.fontconfig, paths.src_arx.fontconfig)
  _patch_done(paths.src_dir.fontconfig)

def _freetype(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  # download.savannah.gnu.org limits concurrent connections
  url = f'https://downloads.sourceforge.net/project/freetype/freetype2/{ver.freetype}/{paths.src_arx.freetype.name}'
  _validate_and_download(paths.src_arx.freetype, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.freetype, paths.src_arx.freetype)
  _patch_done(paths.src_dir.freetype)

def _fuse(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/libfuse/libfuse/releases/download/fuse-{ver.fuse}/{paths.src_arx.fuse.name}'
  _validate_and_download(paths.src_arx.fuse, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.fuse, paths.src_arx.fuse):
    _patch(paths.src_dir.fuse, paths.patch_dir / 'libfuse-try-extra-fusermount.patch')
    _patch_done(paths.src_dir.fuse)

def _gcc(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://ftpmirror.gnu.org/gcc/gcc-{ver.gcc}/{paths.src_arx.gcc.name}'
  _validate_and_download(paths.src_arx.gcc, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.gcc, paths.src_arx.gcc):
    v_musl = Version(ver.musl)
    if v_musl < Version('1.2'):
      _patch(paths.src_dir.gcc, paths.patch_dir / 'gcc-revert-sanitizer-musl-time64.patch')
    _sed(paths.src_dir.gcc / 'gcc/config/i386/t-linux64', '/m64=/s/lib64/lib/')
    _patch_done(paths.src_dir.gcc)

def _gmp(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://ftpmirror.gnu.org/gmp/{paths.src_arx.gmp.name}'
  _validate_and_download(paths.src_arx.gmp, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.gmp, paths.src_arx.gmp)
  _patch_done(paths.src_dir.gmp)

def _harfbuzz(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/harfbuzz/harfbuzz/releases/download/{ver.harfbuzz}/{paths.src_arx.harfbuzz.name}'
  _validate_and_download(paths.src_arx.harfbuzz, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.harfbuzz, paths.src_arx.harfbuzz)
  _patch_done(paths.src_dir.harfbuzz)

def _linux(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.linux)
  url = f'https://cdn.kernel.org/pub/linux/kernel/v{v.major}.x/linux-{ver.linux}.tar.xz'
  _validate_and_download(paths.src_arx.linux, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.linux, paths.src_arx.linux)
  _patch_done(paths.src_dir.linux)

def _mimalloc(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/microsoft/mimalloc/archive/refs/tags/v{ver.mimalloc}.tar.gz'
  _validate_and_download(paths.src_arx.mimalloc, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.mimalloc, paths.src_arx.mimalloc)
  _patch_done(paths.src_dir.mimalloc)

def _mpc(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://ftpmirror.gnu.org/mpc/{paths.src_arx.mpc.name}'
  _validate_and_download(paths.src_arx.mpc, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.mpc, paths.src_arx.mpc)
  _patch_done(paths.src_dir.mpc)

def _mpfr(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://ftpmirror.gnu.org/mpfr/{paths.src_arx.mpfr.name}'
  _validate_and_download(paths.src_arx.mpfr, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.mpfr, paths.src_arx.mpfr)
  _patch_done(paths.src_dir.mpfr)

def _musl(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://www.musl-libc.org/releases/{paths.src_arx.musl.name}'
  _validate_and_download(paths.src_arx.musl, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.musl, paths.src_arx.musl):
    v = Version(ver.musl)
    if v < Version('1.2'):
      _patch(paths.src_dir.musl, paths.patch_dir / 'musl-remove-non-proto-decl.patch')
    _patch_done(paths.src_dir.musl)

def _pkgconf(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/pkgconf/pkgconf/archive/refs/tags/pkgconf-{ver.pkgconf}.tar.gz'
  _validate_and_download(paths.src_arx.pkgconf, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.pkgconf, paths.src_arx.pkgconf)
  _patch_done(paths.src_dir.pkgconf)

def _png(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://download.sourceforge.net/libpng/{paths.src_arx.png.name}'
  _validate_and_download(paths.src_arx.png, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.png, paths.src_arx.png)
  _patch_done(paths.src_dir.png)

def _qtbase(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.qt)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver.qt}/submodules/{paths.src_arx.qtbase.name}'
  _validate_and_download(paths.src_arx.qtbase, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.qtbase, paths.src_arx.qtbase):
    if v >= Version('6.9.0'):
      _patch(paths.src_dir.qtbase, paths.patch_dir / 'qtbase-define-loong-hwcap-flags.patch')
    _patch_done(paths.src_dir.qtbase)

def _qtsvg(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.qt)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver.qt}/submodules/{paths.src_arx.qtsvg.name}'
  _validate_and_download(paths.src_arx.qtsvg, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.qtsvg, paths.src_arx.qtsvg)
  _patch_done(paths.src_dir.qtsvg)

def _qttools(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.qt)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver.qt}/submodules/{paths.src_arx.qttools.name}'
  _validate_and_download(paths.src_arx.qttools, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.qttools, paths.src_arx.qttools)
  _patch_done(paths.src_dir.qttools)

def _qttranslations(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.qt)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver.qt}/submodules/{paths.src_arx.qttranslations.name}'
  _validate_and_download(paths.src_arx.qttranslations, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.qttranslations, paths.src_arx.qttranslations)
  _patch_done(paths.src_dir.qttranslations)

def _qtwayland(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.qt)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver.qt}/submodules/{paths.src_arx.qtwayland.name}'
  _validate_and_download(paths.src_arx.qtwayland, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.qtwayland, paths.src_arx.qtwayland)
  _patch_done(paths.src_dir.qtwayland)

def _squashfuse(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/vasi/squashfuse/releases/download/{ver.squashfuse}/{paths.src_arx.squashfuse.name}'
  _validate_and_download(paths.src_arx.squashfuse, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.squashfuse, paths.src_arx.squashfuse):
    _autoreconf(paths.src_dir.squashfuse)
    _patch_done(paths.src_dir.squashfuse)

def _wayland(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://gitlab.freedesktop.org/wayland/wayland/-/releases/{ver.wayland}/downloads/{paths.src_arx.wayland.name}'
  _validate_and_download(paths.src_arx.wayland, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.wayland, paths.src_arx.wayland)
  _patch_done(paths.src_dir.wayland)

def _x(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.src_arx.x.name}'
  _validate_and_download(paths.src_arx.x, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.x, paths.src_arx.x)
  _patch_done(paths.src_dir.x)

def _xau(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.src_arx.xau.name}'
  _validate_and_download(paths.src_arx.xau, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xau, paths.src_arx.xau)
  _patch_done(paths.src_dir.xau)

def _xcb(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb.name}'
  _validate_and_download(paths.src_arx.xcb, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb, paths.src_arx.xcb)
  _patch_done(paths.src_dir.xcb)

def _xcb_proto(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_proto.name}'
  _validate_and_download(paths.src_arx.xcb_proto, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_proto, paths.src_arx.xcb_proto)
  _patch_done(paths.src_dir.xcb_proto)

def _xcb_util(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util.name}'
  _validate_and_download(paths.src_arx.xcb_util, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util, paths.src_arx.xcb_util)
  _patch_done(paths.src_dir.xcb_util)

def _xcb_util_cursor(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util_cursor.name}'
  _validate_and_download(paths.src_arx.xcb_util_cursor, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util_cursor, paths.src_arx.xcb_util_cursor)
  _patch_done(paths.src_dir.xcb_util_cursor)

def _xcb_util_image(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util_image.name}'
  _validate_and_download(paths.src_arx.xcb_util_image, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util_image, paths.src_arx.xcb_util_image)
  _patch_done(paths.src_dir.xcb_util_image)

def _xcb_util_keysyms(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util_keysyms.name}'
  _validate_and_download(paths.src_arx.xcb_util_keysyms, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util_keysyms, paths.src_arx.xcb_util_keysyms)
  _patch_done(paths.src_dir.xcb_util_keysyms)

def _xcb_util_renderutil(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util_renderutil.name}'
  _validate_and_download(paths.src_arx.xcb_util_renderutil, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util_renderutil, paths.src_arx.xcb_util_renderutil)
  _patch_done(paths.src_dir.xcb_util_renderutil)

def _xcb_util_wm(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xcb.freedesktop.org/dist/{paths.src_arx.xcb_util_wm.name}'
  _validate_and_download(paths.src_arx.xcb_util_wm, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xcb_util_wm, paths.src_arx.xcb_util_wm)
  _patch_done(paths.src_dir.xcb_util_wm)

def _xkbcommon(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/xkbcommon/libxkbcommon/archive/refs/tags/xkbcommon-{ver.xkbcommon}.tar.gz'
  _validate_and_download(paths.src_arx.xkbcommon, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xkbcommon, paths.src_arx.xkbcommon)
  _patch_done(paths.src_dir.xkbcommon)

def _xml(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.xml)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.gnome.org/sources/libxml2/{branch}/{paths.src_arx.xml.name}'
  _validate_and_download(paths.src_arx.xml, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xml, paths.src_arx.xml)
  _patch_done(paths.src_dir.xml)

def _xorg_proto(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xorg.freedesktop.org/releases/individual/proto/{paths.src_arx.xorg_proto.name}'
  _validate_and_download(paths.src_arx.xorg_proto, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xorg_proto, paths.src_arx.xorg_proto)
  _patch_done(paths.src_dir.xorg_proto)

def _xtrans(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.src_arx.xtrans.name}'
  _validate_and_download(paths.src_arx.xtrans, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.xtrans, paths.src_arx.xtrans)
  _patch_done(paths.src_dir.xtrans)

def _z(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://zlib.net/fossils/{paths.src_arx.z.name}'
  _validate_and_download(paths.src_arx.z, url)
  if download_only:
    return

  _check_and_extract(paths.src_dir.z, paths.src_arx.z)
  _patch_done(paths.src_dir.z)

def _zstd(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/facebook/zstd/releases/download/v{ver.zstd}/{paths.src_arx.zstd.name}'
  _validate_and_download(paths.src_arx.zstd, url)
  if download_only:
    return

  if _check_and_extract(paths.src_dir.zstd, paths.src_arx.zstd):
    _patch(paths.src_dir.zstd, paths.patch_dir / 'zstd-add-switch-for-qsort.patch')
    _patch_done(paths.src_dir.zstd)

def prepare_source(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v_qt = Version(ver.qt)

  _appimage_runtime(ver, paths, download_only)
  _binutils(ver, paths, download_only)
  _dbus(ver, paths, download_only)
  _expat(ver, paths, download_only)
  _ffi(ver, paths, download_only)
  _fcitx_qt(ver, paths, download_only)
  _fontconfig(ver, paths, download_only)
  _freetype(ver, paths, download_only)
  _fuse(ver, paths, download_only)
  _gcc(ver, paths, download_only)
  _gmp(ver, paths, download_only)
  _harfbuzz(ver, paths, download_only)
  _linux(ver, paths, download_only)
  _mimalloc(ver, paths, download_only)
  _mpc(ver, paths, download_only)
  _mpfr(ver, paths, download_only)
  _musl(ver, paths, download_only)
  _pkgconf(ver, paths, download_only)
  _png(ver, paths, download_only)
  _qtbase(ver, paths, download_only)
  _qtsvg(ver, paths, download_only)
  _qttools(ver, paths, download_only)
  _qttranslations(ver, paths, download_only)
  if v_qt < Version('6.10'):
    _qtwayland(ver, paths, download_only)
  _squashfuse(ver, paths, download_only)
  _wayland(ver, paths, download_only)
  _x(ver, paths, download_only)
  _xau(ver, paths, download_only)
  _xcb(ver, paths, download_only)
  _xcb_proto(ver, paths, download_only)
  _xcb_util(ver, paths, download_only)
  _xcb_util_cursor(ver, paths, download_only)
  _xcb_util_image(ver, paths, download_only)
  _xcb_util_keysyms(ver, paths, download_only)
  _xcb_util_renderutil(ver, paths, download_only)
  _xcb_util_wm(ver, paths, download_only)
  _xkbcommon(ver, paths, download_only)
  _xml(ver, paths, download_only)
  _xorg_proto(ver, paths, download_only)
  _xtrans(ver, paths, download_only)
  _z(ver, paths, download_only)
  _zstd(ver, paths, download_only)
