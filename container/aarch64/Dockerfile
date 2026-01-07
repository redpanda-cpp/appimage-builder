FROM localhost/redpanda-cpp/basic-appimage-builder:latest

ADD qt.tar /usr/local

ENV ARCH=aarch64
ENV DEB_ARCH=arm64
ENV APPIMAGE_RUNTIME=/usr/local/aarch64-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/aarch64-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/aarch64-linux-musl
ENV CMAKE_CROSSCOMPILING_EMULATOR=qemu-aarch64
