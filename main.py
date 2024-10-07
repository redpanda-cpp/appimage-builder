#!/usr/bin/python3

import argparse
import logging
import os
import shutil
import subprocess

from module.cross_toolchain import build_cross_toolchain
from module.host_lib import build_host_lib
from module.path import ProjectPaths
from module.prepare_source import download_and_patch
from module.profile import get_full_profile
from module.target_lib import build_target_lib

def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-a', '--arch', '--architecture',
    type = str,
    choices = [
      'x86_64', 'aarch64', 'riscv64', 'loong64',
      'i686',
    ],
    required = True,
  )
  parser.add_argument(
    '-b', '--branch',
    type = str,
    choices = ['main', 'time32'],
    default = 'main',
    help = 'Qt branch to build',
  )

  parser.add_argument(
    '-c', '--clean',
    action = 'store_true',
    help = 'Clean build directories',
  )
  parser.add_argument(
    '-j', '--jobs',
    type = int,
    default = os.cpu_count(),
  )
  parser.add_argument(
    '-v', '--verbose',
    action = 'count',
    default = 0,
    help = 'Increase verbosity (up to 2)',
  )

  result = parser.parse_args()
  return result

def clean(config: argparse.Namespace, paths: ProjectPaths):
  if paths.build.exists():
    shutil.rmtree(paths.build)
  if paths.prefix.exists():
    shutil.rmtree(paths.prefix)

def prepare_dirs(paths: ProjectPaths):
  paths.assets.mkdir(parents = True, exist_ok = True)
  paths.build.mkdir(parents = True, exist_ok = True)
  paths.dist.mkdir(parents = True, exist_ok = True)

def package(paths: ProjectPaths):
  ret = subprocess.run([
    'tar',
    '-cf',
    paths.container / 'qt.tar',
    paths.h_prefix,
  ])
  if ret.returncode != 0:
    raise Exception('Failed to package')

def main():
  config = parse_args()

  if config.verbose >= 2:
    logging.basicConfig(level = logging.DEBUG)
  elif config.verbose >= 1:
    logging.basicConfig(level = logging.INFO)
  else:
    logging.basicConfig(level = logging.ERROR)

  profile = get_full_profile(config)
  paths = ProjectPaths(config, profile.ver, profile.info)

  if config.clean:
    clean(config, paths)

  prepare_dirs(paths)

  download_and_patch(profile.ver, paths, profile.info)

  os.environ['PATH'] = f'{paths.h_prefix}/bin:{os.environ['PATH']}'

  os.environ['PKG_CONFIG_LIBDIR'] = f'{paths.h_prefix}/lib/pkgconfig:{paths.h_prefix}/share/pkgconfig'
  build_host_lib(profile.ver, paths, profile.info, config)
  del os.environ['PKG_CONFIG_LIBDIR']

  build_cross_toolchain(profile.ver, paths, profile.info, config)

  os.environ['PKG_CONFIG_LIBDIR'] = f'{paths.prefix}/lib/pkgconfig:{paths.prefix}/share/pkgconfig'
  build_target_lib(profile.ver, paths, profile.info, config)
  del os.environ['PKG_CONFIG_LIBDIR']

  package(paths)

if __name__ == "__main__":
  main()
