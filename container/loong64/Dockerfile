FROM localhost/redpanda-cpp/basic-appimage-builder:latest

ADD qt.tar /usr/local

ENV ARCH=loong64
ENV DEB_ARCH=loong64
ENV APPIMAGE_RUNTIME=/usr/local/loongarch64-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/loongarch64-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/loongarch64-linux-musl
ENV CMAKE_CROSSCOMPILING_EMULATOR=qemu-loongarch64
