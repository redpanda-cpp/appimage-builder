FROM localhost/redpanda-cpp/basic-appimage-builder:latest

ADD qt.tar /usr/local

ENV ARCH=i686
ENV DEB_ARCH=i386
ENV APPIMAGE_RUNTIME=/usr/local/i686-linux-musl/bin/appimage-runtime

ENV CMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/i686-linux-musl.cmake
ENV CMAKE_PREFIX_PATH=/usr/local/i686-linux-musl
