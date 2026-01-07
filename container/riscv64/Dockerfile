FROM localhost/redpanda-cpp/basic-appimage-builder:latest

ADD qt.tar /usr/local

ENV ARCH=riscv64
ENV DEB_ARCH=riscv64
ENV APPIMAGE_RUNTIME=/usr/local/riscv64-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/riscv64-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/riscv64-linux-musl
ENV CMAKE_CROSSCOMPILING_EMULATOR=qemu-riscv64
