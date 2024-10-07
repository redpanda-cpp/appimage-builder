from hashlib import sha256
import logging
from packaging.version import Version
from pathlib import Path
import subprocess
from urllib.error import URLError
from urllib.request import urlopen

from module.checksum import CHECKSUMS
from module.path import ProjectPaths
from module.profile import BranchVersions, ProfileInfo


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

def _appimage_runtime(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/AppImage/type2-runtime/archive/{ver}.tar.gz'
  _validate_and_download(paths.appimage_runtime_arx, url)
  if _check_and_extract(paths.appimage_runtime, paths.appimage_runtime_arx):
    _patch(paths.appimage_runtime, paths.patch / 'appimage-runtime-trunk-squashfs.patch')
    _patch_done(paths.appimage_runtime)

def _binutils(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://ftpmirror.gnu.org/gnu/binutils/{paths.binutils_arx.name}'
  _validate_and_download(paths.binutils_arx, url)
  _check_and_extract(paths.binutils, paths.binutils_arx)
  _patch_done(paths.binutils)

def _dbus(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://dbus.freedesktop.org/releases/dbus/{paths.dbus_arx.name}'
  _validate_and_download(paths.dbus_arx, url)
  _check_and_extract(paths.dbus, paths.dbus_arx)
  _patch_done(paths.dbus)

def _expat(ver: str, info: ProfileInfo, paths: ProjectPaths):
  tag = 'R_' + ver.replace('.', '_')
  url = f'https://github.com/libexpat/libexpat/releases/download/{tag}/{paths.expat_arx.name}'
  _validate_and_download(paths.expat_arx, url)
  _check_and_extract(paths.expat, paths.expat_arx)
  _patch_done(paths.expat)

def _fcitx_qt(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/fcitx/fcitx5-qt/archive/refs/tags/{ver}.tar.gz'
  _validate_and_download(paths.fcitx_qt_arx, url)
  _check_and_extract(paths.fcitx_qt, paths.fcitx_qt_arx)
  _patch_done(paths.fcitx_qt)

def _ffi(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/libffi/libffi/releases/download/v{ver}/{paths.ffi_arx.name}'
  _validate_and_download(paths.ffi_arx, url)
  _check_and_extract(paths.ffi, paths.ffi_arx)
  _patch_done(paths.ffi)

def _fontconfig(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://www.freedesktop.org/software/fontconfig/release/{paths.fontconfig_arx.name}'
  _validate_and_download(paths.fontconfig_arx, url)
  _check_and_extract(paths.fontconfig, paths.fontconfig_arx)
  _patch_done(paths.fontconfig)

def _freetype(ver: str, info: ProfileInfo, paths: ProjectPaths):
  # download.savannah.gnu.org limits concurrent connections
  url = f'https://downloads.sourceforge.net/project/freetype/freetype2/{ver}/{paths.freetype_arx.name}'
  _validate_and_download(paths.freetype_arx, url)
  _check_and_extract(paths.freetype, paths.freetype_arx)
  _patch_done(paths.freetype)

def _fuse(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/libfuse/libfuse/releases/download/fuse-{ver}/{paths.fuse_arx.name}'
  _validate_and_download(paths.fuse_arx, url)
  if _check_and_extract(paths.fuse, paths.fuse_arx):
    _patch(paths.fuse, paths.patch / 'libfuse-try-extra-fusermount.patch')
    _patch_done(paths.fuse)

def _gcc(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://ftpmirror.gnu.org/gcc/gcc-{ver}/{paths.gcc_arx.name}'
  _validate_and_download(paths.gcc_arx, url)
  if _check_and_extract(paths.gcc, paths.gcc_arx):
    _sed(paths.gcc / 'gcc/config/i386/t-linux64', '/m64=/s/lib64/lib/')
    _patch_done(paths.gcc)

def _gmp(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://ftpmirror.gnu.org/gmp/{paths.gmp_arx.name}'
  _validate_and_download(paths.gmp_arx, url)
  _check_and_extract(paths.gmp, paths.gmp_arx)
  _patch_done(paths.gmp)

def _harfbuzz(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/harfbuzz/harfbuzz/releases/download/{ver}/{paths.harfbuzz_arx.name}'
  _validate_and_download(paths.harfbuzz_arx, url)
  _check_and_extract(paths.harfbuzz, paths.harfbuzz_arx)
  _patch_done(paths.harfbuzz)

def _linux_headers(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/sabotage-linux/kernel-headers/releases/download/v{ver}/{paths.linux_headers_arx.name}'
  _validate_and_download(paths.linux_headers_arx, url)
  _check_and_extract(paths.linux_headers, paths.linux_headers_arx)
  _patch_done(paths.linux_headers)

def _mpc(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://ftpmirror.gnu.org/mpc/{paths.mpc_arx.name}'
  _validate_and_download(paths.mpc_arx, url)
  _check_and_extract(paths.mpc, paths.mpc_arx)
  _patch_done(paths.mpc)

def _mpfr(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://ftpmirror.gnu.org/mpfr/{paths.mpfr_arx.name}'
  _validate_and_download(paths.mpfr_arx, url)
  _check_and_extract(paths.mpfr, paths.mpfr_arx)
  _patch_done(paths.mpfr)

def _musl(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://www.musl-libc.org/releases/{paths.musl_arx.name}'
  _validate_and_download(paths.musl_arx, url)
  _check_and_extract(paths.musl, paths.musl_arx)
  _patch_done(paths.musl)

def _png(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://download.sourceforge.net/libpng/{paths.png_arx.name}'
  _validate_and_download(paths.png_arx, url)
  _check_and_extract(paths.png, paths.png_arx)
  _patch_done(paths.png)

def _qtbase(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver}/submodules/{paths.qtbase_arx.name}'
  _validate_and_download(paths.qtbase_arx, url)
  _check_and_extract(paths.qtbase, paths.qtbase_arx)
  _patch_done(paths.qtbase)

def _qtsvg(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver}/submodules/{paths.qtsvg_arx.name}'
  _validate_and_download(paths.qtsvg_arx, url)
  _check_and_extract(paths.qtsvg, paths.qtsvg_arx)
  _patch_done(paths.qtsvg)

def _qttools(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver}/submodules/{paths.qttools_arx.name}'
  _validate_and_download(paths.qttools_arx, url)
  _check_and_extract(paths.qttools, paths.qttools_arx)
  _patch_done(paths.qttools)

def _qttranslations(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver}/submodules/{paths.qttranslations_arx.name}'
  _validate_and_download(paths.qttranslations_arx, url)
  _check_and_extract(paths.qttranslations, paths.qttranslations_arx)
  _patch_done(paths.qttranslations)

def _qtwayland(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.qt.io/archive/qt/{branch}/{ver}/submodules/{paths.qtwayland_arx.name}'
  _validate_and_download(paths.qtwayland_arx, url)
  _check_and_extract(paths.qtwayland, paths.qtwayland_arx)
  _patch_done(paths.qtwayland)

def _squashfuse(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/vasi/squashfuse/archive/{ver}.tar.gz'
  _validate_and_download(paths.squashfuse_arx, url)
  if _check_and_extract(paths.squashfuse, paths.squashfuse_arx):
    _autoreconf(paths.squashfuse)
    _patch_done(paths.squashfuse)

def _wayland(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://gitlab.freedesktop.org/wayland/wayland/-/releases/{ver}/downloads/{paths.wayland_arx.name}'
  _validate_and_download(paths.wayland_arx, url)
  _check_and_extract(paths.wayland, paths.wayland_arx)
  _patch_done(paths.wayland)

def _x(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.x_arx.name}'
  _validate_and_download(paths.x_arx, url)
  _check_and_extract(paths.x, paths.x_arx)
  _patch_done(paths.x)

def _xau(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.xau_arx.name}'
  _validate_and_download(paths.xau_arx, url)
  _check_and_extract(paths.xau, paths.xau_arx)
  _patch_done(paths.xau)

def _xcb(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_arx.name}'
  _validate_and_download(paths.xcb_arx, url)
  _check_and_extract(paths.xcb, paths.xcb_arx)
  _patch_done(paths.xcb)

def _xcb_proto(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_proto_arx.name}'
  _validate_and_download(paths.xcb_proto_arx, url)
  _check_and_extract(paths.xcb_proto, paths.xcb_proto_arx)
  _patch_done(paths.xcb_proto)

def _xcb_util(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_arx.name}'
  _validate_and_download(paths.xcb_util_arx, url)
  _check_and_extract(paths.xcb_util, paths.xcb_util_arx)
  _patch_done(paths.xcb_util)

def _xcb_util_cursor(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_cursor_arx.name}'
  _validate_and_download(paths.xcb_util_cursor_arx, url)
  _check_and_extract(paths.xcb_util_cursor, paths.xcb_util_cursor_arx)
  _patch_done(paths.xcb_util_cursor)

def _xcb_util_image(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_image_arx.name}'
  _validate_and_download(paths.xcb_util_image_arx, url)
  _check_and_extract(paths.xcb_util_image, paths.xcb_util_image_arx)
  _patch_done(paths.xcb_util_image)

def _xcb_util_keysyms(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_keysyms_arx.name}'
  _validate_and_download(paths.xcb_util_keysyms_arx, url)
  _check_and_extract(paths.xcb_util_keysyms, paths.xcb_util_keysyms_arx)
  _patch_done(paths.xcb_util_keysyms)

def _xcb_util_renderutil(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_renderutil_arx.name}'
  _validate_and_download(paths.xcb_util_renderutil_arx, url)
  _check_and_extract(paths.xcb_util_renderutil, paths.xcb_util_renderutil_arx)
  _patch_done(paths.xcb_util_renderutil)

def _xcb_util_wm(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xcb.freedesktop.org/dist/{paths.xcb_util_wm_arx.name}'
  _validate_and_download(paths.xcb_util_wm_arx, url)
  _check_and_extract(paths.xcb_util_wm, paths.xcb_util_wm_arx)
  _patch_done(paths.xcb_util_wm)

def _xkbcommon(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xkbcommon.org/download/{paths.xkbcommon_arx.name}'
  _validate_and_download(paths.xkbcommon_arx, url)
  _check_and_extract(paths.xkbcommon, paths.xkbcommon_arx)
  _patch_done(paths.xkbcommon)

def _xml(ver: str, info: ProfileInfo, paths: ProjectPaths):
  v = Version(ver)
  branch = f'{v.major}.{v.minor}'
  url = f'https://download.gnome.org/sources/libxml2/{branch}/{paths.xml_arx.name}'
  _validate_and_download(paths.xml_arx, url)
  _check_and_extract(paths.xml, paths.xml_arx)
  _patch_done(paths.xml)

def _xorg_proto(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xorg.freedesktop.org/releases/individual/proto/{paths.xorg_proto_arx.name}'
  _validate_and_download(paths.xorg_proto_arx, url)
  _check_and_extract(paths.xorg_proto, paths.xorg_proto_arx)
  _patch_done(paths.xorg_proto)

def _xtrans(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://xorg.freedesktop.org/releases/individual/lib/{paths.xtrans_arx.name}'
  _validate_and_download(paths.xtrans_arx, url)
  _check_and_extract(paths.xtrans, paths.xtrans_arx)
  _patch_done(paths.xtrans)

def _z(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://zlib.net/fossils/{paths.z_arx.name}'
  _validate_and_download(paths.z_arx, url)
  _check_and_extract(paths.z, paths.z_arx)
  _patch_done(paths.z)

def _zstd(ver: str, info: ProfileInfo, paths: ProjectPaths):
  url = f'https://github.com/facebook/zstd/releases/download/v{ver}/{paths.zstd_arx.name}'
  _validate_and_download(paths.zstd_arx, url)
  _check_and_extract(paths.zstd, paths.zstd_arx)
  _patch_done(paths.zstd)

def download_and_patch(ver: BranchVersions, paths: ProjectPaths, info: ProfileInfo):
  _appimage_runtime(ver.appimage_runtime, info, paths)
  _binutils(ver.binutils, info, paths)
  _dbus(ver.dbus, info, paths)
  _expat(ver.expat, info, paths)
  _ffi(ver.ffi, info, paths)
  _fcitx_qt(ver.fcitx_qt, info, paths)
  _fontconfig(ver.fontconfig, info, paths)
  _freetype(ver.freetype, info, paths)
  _fuse(ver.fuse, info, paths)
  _gcc(ver.gcc, info, paths)
  _gmp(ver.gmp, info, paths)
  _harfbuzz(ver.harfbuzz, info, paths)
  _linux_headers(ver.linux_headers, info, paths)
  _mpc(ver.mpc, info, paths)
  _mpfr(ver.mpfr, info, paths)
  _musl(ver.musl, info, paths)
  _png(ver.png, info, paths)
  _qtbase(ver.qt, info, paths)
  _qtsvg(ver.qt, info, paths)
  _qttools(ver.qt, info, paths)
  _qttranslations(ver.qt, info, paths)
  _qtwayland(ver.qt, info, paths)
  _squashfuse(ver.squashfuse, info, paths)
  _wayland(ver.wayland, info, paths)
  _x(ver.x, info, paths)
  _xau(ver.xau, info, paths)
  _xcb(ver.xcb, info, paths)
  _xcb_proto(ver.xcb_proto, info, paths)
  _xcb_util(ver.xcb_util, info, paths)
  _xcb_util_cursor(ver.xcb_util_cursor, info, paths)
  _xcb_util_image(ver.xcb_util_image, info, paths)
  _xcb_util_keysyms(ver.xcb_util_keysyms, info, paths)
  _xcb_util_renderutil(ver.xcb_util_renderutil, info, paths)
  _xcb_util_wm(ver.xcb_util_wm, info, paths)
  _xkbcommon(ver.xkbcommon, info, paths)
  _xml(ver.xml, info, paths)
  _xorg_proto(ver.xorg_proto, info, paths)
  _xtrans(ver.xtrans, info, paths)
  _z(ver.z, info, paths)
  _zstd(ver.zstd, info, paths)
