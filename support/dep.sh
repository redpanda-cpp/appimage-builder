#!/bin/bash

apt update
env DEBIAN_FRONTEND=noninteractive \
  apt install -y --no-install-recommends \
    autoconf automake bison cmake extra-cmake-modules g++ gawk gcc gperf libtool m4 make ninja-build patch pkgconf rsync texinfo \
    ca-certificates libarchive-tools python3 python3-packaging python3-pip
