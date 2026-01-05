#!/usr/bin/python3

import argparse
import logging
import os
from pathlib import Path
import shutil
import subprocess
from subprocess import PIPE
from typing import Dict, List

from module.path import ProjectPaths
from module.prepare_source import prepare_source
from module.profile import resolve_profile
from module.util import ensure, overlayfs_ro

from module.host_lib import build_host_lib
from module.cross_toolchain import build_cross_toolchain
from module.target_lib import build_target_lib

def get_gcc_triplet():
  result = subprocess.run(['gcc', '-dumpmachine'], stdout = PIPE, stderr = PIPE, check = True)
  return result.stdout.decode('utf-8').strip()

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

  gcc_triplet = get_gcc_triplet()
  parser.add_argument(
    '--host',
    type = str,
    default = gcc_triplet,
    help = 'Host system triplet',
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
    '--download-only',
    action = 'store_true',
    help = 'Download sources only',
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
  if paths.build_dir.exists():
    shutil.rmtree(paths.build_dir)
  if paths.layer_dir.exists():
    shutil.rmtree(paths.layer_dir)

def prepare_dirs(paths: ProjectPaths):
  ensure(paths.assets_dir)
  ensure(paths.build_dir)
  ensure(paths.dist_dir)

def check_file_collision(layers: list[Path]):
  file_to_package_map: Dict[str, List[str]] = {}
  for layer in layers:
    for file in layer.glob('**/*'):
      if not file.is_dir():
        file_path = str(file.relative_to(layer))
        if file_path in file_to_package_map:
          file_to_package_map[file_path].append(str(layer))
        else:
          file_to_package_map[file_path] = [str(layer)]

  ok = True
  for file, packages in file_to_package_map.items():
    if len(packages) > 1:
      ok = False
      print(f'file collision: {file} in {packages}')

  if not ok:
    raise Exception('file collision')

def package(paths: ProjectPaths):
  layers = []
  for layer_group in (paths.layer_host, paths.layer_x, paths.layer_target):
    for k, v in layer_group._asdict().items():
      if k in ('prefix', 'freetype_decycle'):
        continue
      layers.append(v)

  check_file_collision(layers)

  with overlayfs_ro('/usr/local', [
    *map(lambda layer: layer / 'usr/local', layers),
  ]):
    subprocess.run([
      'tar',
      '-C', '/usr/local',
      '-c', '.',
      '-f', paths.container_dir / 'qt.tar',
    ], check = True)

def main():
  config = parse_args()

  if config.verbose >= 2:
    logging.basicConfig(level = logging.DEBUG)
  elif config.verbose >= 1:
    logging.basicConfig(level = logging.INFO)
  else:
    logging.basicConfig(level = logging.ERROR)

  ver = resolve_profile(config)
  paths = ProjectPaths(config, ver)

  if config.clean:
    clean(config, paths)

  prepare_dirs(paths)

  prepare_source(ver, paths, config.download_only)

  if config.download_only:
    return

  build_host_lib(ver, paths, config)

  build_cross_toolchain(ver, paths, config)

  build_target_lib(ver, paths, config)

  package(paths)

if __name__ == "__main__":
  main()
