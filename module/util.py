import logging
from pathlib import Path
import subprocess
from typing import List

from module.profile import ProfileInfo

def cflags_host(
  suffix: str = '',
  common_extra: List[str] = [],
  ld_extra: List[str] = [],
  c_extra: List[str] = [],
  cxx_extra: List[str] = [],
) -> List[str]:
  common = ['-Os']
  ld = ['-s']
  return [
    f'CFLAGS{suffix}=' + ' '.join(common + common_extra + c_extra),
    f'CXXFLAGS{suffix}=' + ' '.join(common + common_extra + cxx_extra),
    f'LDFLAGS{suffix}=' + ' '.join(ld + ld_extra),
  ]

def cflags_target(
  suffix: str = '',
  common_extra: List[str] = [],
  ld_extra: List[str] = [],
  c_extra: List[str] = [],
  cxx_extra: List[str] = [],
) -> List[str]:
  common = ['-Os']
  ld = ['-s']
  return [
    f'CFLAGS{suffix}=' + ' '.join(common + common_extra + c_extra),
    f'CXXFLAGS{suffix}=' + ' '.join(common + common_extra + cxx_extra),
    f'LDFLAGS{suffix}=' + ' '.join(ld + ld_extra),
  ]

def cmake_build(component: str, build_dir: Path, jobs: int):
  cmake_custom(component + ' (build)', ['--build', build_dir, '--parallel', str(jobs)])

def cmake_config(component: str, source_dir: Path, build_dir: Path, args: List[str]):
  cmake_custom(component + ' (config)', ['-S', source_dir, '-B', build_dir, *args])

def cmake_custom(component: str, args: List[str]):
  res = subprocess.run(
    ['cmake', *args],
  )
  if res.returncode != 0:
    message = f'Build fail: {component} cmake returned {res.returncode}'
    logging.critical(message)
    raise Exception(message)

def cmake_install(component: str, build_dir: Path):
  cmake_custom(component + ' (install)', ['--install', build_dir])

def configure(component: str, cwd: Path, args: List[str]):
  res = subprocess.run(
    ['../configure', *args],
    cwd = cwd,
  )
  if res.returncode != 0:
    message = f'Build fail: {component} configure returned {res.returncode}'
    logging.critical(message)
    raise Exception(message)

def ensure(path: Path):
  path.mkdir(parents = True, exist_ok = True)

def make_custom(component: str, cwd: Path, extra_args: List[str], jobs: int):
  res = subprocess.run(
    ['make', *extra_args, f'-j{jobs}'],
    cwd = cwd,
  )
  if res.returncode != 0:
    message = f'Build fail: {component} make returned {res.returncode}'
    logging.critical(message)
    raise Exception(message)

def make_default(component: str, cwd: Path, jobs: int):
  make_custom(component + ' (default)', cwd, [], jobs)

def make_install(component: str, cwd: Path):
  make_custom(component + ' (install)', cwd, ['install'], jobs = 1)

def meson_compile(component: str, build_dir: Path, jobs: int):
  meson_custom(component + ' (compile)', ['compile', '-C', build_dir, '--jobs', str(jobs)])

def meson_custom(component: str, args: List[str]):
  res = subprocess.run(
    ['meson', *args],
  )
  if res.returncode != 0:
    message = f'Build fail: {component} meson returned {res.returncode}'
    logging.critical(message)
    raise Exception(message)

def meson_install(component: str, build_dir: Path):
  meson_custom(component + ' (install)', ['install', '-C', build_dir])

def meson_setup(component: str, source_dir: Path, build_dir: Path, args: List[str]):
  meson_custom(component + ' (setup)', ['setup', *args, build_dir, source_dir])

def qt_configure_module(component: str, source_dir: Path, build_dir: Path, args: List[str]):
  res = subprocess.run([
    'qt-configure-module',
    source_dir,
    *args,
  ], cwd = build_dir)
  if res.returncode != 0:
    raise Exception(f'{component} qt-configure-module returned {res.returncode}')
