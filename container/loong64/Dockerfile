FROM docker.io/amd64/ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update && \
    apt upgrade -y && \
    apt install --no-install-recommends -y \
        # Red Panda C++
        git make \
        # appimage tools
        squashfs-tools && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ADD qt.tar /

ENV ARCH=loong64
ENV PATH=/opt/qt-loong64/loongarch64-linux-musl/qt/bin:/opt/qt-loong64/bin:${PATH}
ENV APPIMAGE_RUNTIME=/opt/qt-loong64/loongarch64-linux-musl/bin/appimage-runtime
