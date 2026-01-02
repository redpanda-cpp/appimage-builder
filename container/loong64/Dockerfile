FROM docker.io/amd64/ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update && \
    apt install --no-install-recommends -y \
        # Red Panda C++
        git make \
        # appimage tools
        squashfs-tools && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ADD qt.tar /usr/local

ENV ARCH=loong64
ENV QMAKE=/usr/local/loongarch64-linux-musl/bin/qmake
ENV APPIMAGE_RUNTIME=/usr/local/loongarch64-linux-musl/bin/appimage-runtime
