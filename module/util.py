from contextlib import contextmanager
import logging
import os
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Union

from module.path import ProjectPaths
from module.profile import ProfileInfo

def cflags_host(
  suffix: str = '',
  cpp_extra: List[str] = [],
  common_extra: List[str] = [],
  ld_extra: List[str] = [],
  c_extra: List[str] = [],
  cxx_extra: List[str] = [],
) -> List[str]:
  return cflags_target(
    suffix = suffix,
    cpp_extra = cpp_extra,
    common_extra = common_extra,
    ld_extra = ld_extra,
    c_extra = c_extra,
    cxx_extra = cxx_extra,
  )

def cflags_target(
  suffix: str = '',
  cpp_extra: List[str] = [],
  common_extra: List[str] = [],
  ld_extra: List[str] = [],
  c_extra: List[str] = [],
  cxx_extra: List[str] = [],
) -> List[str]:
  cpp = ['-DNDEBUG']
  common = ['-O2', '-pipe']
  ld = ['-s']
  return [
    f'CPPFLAGS{suffix}=' + ' '.join(cpp + cpp_extra),
    f'CFLAGS{suffix}=' + ' '.join(common + common_extra + c_extra),
    f'CXXFLAGS{suffix}=' + ' '.join(common + common_extra + cxx_extra),
    f'LDFLAGS{suffix}=' + ' '.join(ld + ld_extra),
  ]

def cmake_build(build_dir: Path, jobs: int):
  cmake_custom(['--build', build_dir, '--parallel', str(jobs)])

def cmake_config(source_dir: Path, build_dir: Path, args: List[str]):
  cmake_custom([
    '-S', source_dir,
    '-B', build_dir,
    '-DCMAKE_BUILD_TYPE=Release',
    *args,
  ])

def cmake_custom(args: List[str], env: Dict[str, str] = {}):
  subprocess.run(
    ['cmake', *args],
    env = {**os.environ, **env},
    check = True,
  )

def cmake_destdir_install(build_dir: Path, destdir: Path):
  cmake_custom(['--install', build_dir, '--strip'], env = {'DESTDIR': destdir})

def cmake_install(build_dir: Path):
  cmake_custom(['--install', build_dir, '--strip'])

def configure(cwd: Path, args: List[str]):
  subprocess.run(
    ['../configure', *args],
    cwd = cwd,
    check = True,
  )

def ensure(path: Path):
  path.mkdir(parents = True, exist_ok = True)

def make_custom(cwd: Path, extra_args: List[str], jobs: int):
  subprocess.run(
    ['make', *extra_args, f'-j{jobs}'],
    cwd = cwd,
    check = True,
  )

def make_default(cwd: Path, jobs: int):
  make_custom(cwd, [], jobs)

def make_destdir_install(cwd: Path, destdir: Path):
  make_custom(cwd, [f'DESTDIR={destdir}', 'install'], jobs = 1)

def make_install(cwd: Path):
  make_custom(cwd, ['install'], jobs = 1)

def merge_libs(triplet: str, merged: Path, libs: List[Union[Path, str]]):
  """
  workaround for Qt missing static library
  """

  input = f'create {merged}\n'
  for lib in libs:
    input += f'addlib {lib}\n'
  input += 'save\nend\n'

  subprocess.run(
    [f'{triplet}-gcc-ar', '-M'],
    input = input.encode(),
    check = True,
  )

def meson_build(
  build_dir: str,
  jobs: int,
  targets: List[str] = [],
):
  subprocess.run(
    ['meson', 'compile', '-C', build_dir, f'-j{jobs}', *targets],
    check = True,
  )

def meson_config(
  source_dir: Path,
  build_dir: str,
  extra_args: List[str],
):
  subprocess.run(
    [
      'meson',
      'setup',
      '--default-library', 'static',
      '--prefer-static',
      '--buildtype', 'minsize',
      '--strip',
      *extra_args,
      build_dir
    ],
    cwd = source_dir,
    check = True,
  )

def meson_destdir_install(
  build_dir: str,
  destdir: Path,
):
  subprocess.run(
    ['meson', 'install', '-C', build_dir, '--destdir', destdir],
    check = True,
  )

@contextmanager
def overlayfs_ro(merged: Union[Path, str], lower: list[Path]):
  try:
    if len(lower) == 1:
      subprocess.run([
        'mount',
        '--bind',
        lower[0],
        merged,
        '-o', 'ro',
      ], check = True)
    else:
      lowerdir = ':'.join(map(str, lower))
      subprocess.run([
        'mount',
        '-t', 'overlay',
        'none',
        merged,
        '-o', f'lowerdir={lowerdir}',
      ], check = True)
    yield
  finally:
    subprocess.run(['umount', merged], check = False)

def qt_configure_module(source_dir: Path, build_dir: Path, args: List[str], triplet: Optional[str] = None):
  qt_configure_module = 'qt-configure-module'
  if triplet:
    qt_configure_module = f'/usr/local/{triplet}/bin/qt-configure-module'

  subprocess.run(
    [qt_configure_module, source_dir, *args],
    cwd = build_dir,
    check = True,
  )

def qt_dependent_layers(paths: ProjectPaths):
  return [
    paths.layer_host.qtbase / f'usr/local',
    paths.layer_host.qttools / 'usr/local',
    paths.layer_host.qtwayland / 'usr/local',
    paths.layer_host.wayland / 'usr/local',

    paths.layer_target.dbus / 'usr/local',
    paths.layer_target.expat / 'usr/local',
    paths.layer_target.ffi / 'usr/local',
    paths.layer_target.fontconfig / 'usr/local',
    paths.layer_target.freetype / 'usr/local',
    paths.layer_target.harfbuzz / 'usr/local',
    paths.layer_target.png / 'usr/local',
    paths.layer_target.wayland / 'usr/local',
    paths.layer_target.x / 'usr/local',
    paths.layer_target.xau / 'usr/local',
    paths.layer_target.xcb / 'usr/local',
    paths.layer_target.xcb_util / 'usr/local',
    paths.layer_target.xcb_util_cursor / 'usr/local',
    paths.layer_target.xcb_util_image / 'usr/local',
    paths.layer_target.xcb_util_keysyms / 'usr/local',
    paths.layer_target.xcb_util_renderutil / 'usr/local',
    paths.layer_target.xcb_util_wm / 'usr/local',
    paths.layer_target.xkbcommon / 'usr/local',
    paths.layer_target.xml / 'usr/local',
    paths.layer_target.xorg_proto / 'usr/local',
    paths.layer_target.z / 'usr/local',
  ]

def toolchain_layers(paths: ProjectPaths):
  return [
    paths.layer_x.binutils / 'usr/local',
    paths.layer_x.gcc / 'usr/local',
    paths.layer_x.linux / 'usr/local',
    paths.layer_x.musl / 'usr/local',
    paths.layer_x.pkgconf / 'usr/local',
  ]
