FROM localhost/redpanda-cpp/basic-appimage-builder:latest

ADD qt.tar /usr/local

ENV ARCH=x86_64.v3
ENV DEB_ARCH=amd64v3
ENV APPIMAGE_RUNTIME=/usr/local/x86_64-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/x86_64-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/x86_64-linux-musl
