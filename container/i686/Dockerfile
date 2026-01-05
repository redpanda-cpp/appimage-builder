FROM docker.io/amd64/ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update && \
    apt install --no-install-recommends -y \
        # Red Panda C++
        cmake git make \
        fonts-noto fonts-noto-cjk fonts-noto-color-emoji \
        # appimage tools
        squashfs-tools && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ADD qt.tar /usr/local

ENV ARCH=i686
ENV DEB_ARCH=i386
ENV APPIMAGE_RUNTIME=/usr/local/i686-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/i686-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/i686-linux-musl
