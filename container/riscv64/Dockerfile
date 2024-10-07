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

ENV ARCH=riscv64
ENV PATH=/opt/qt-riscv64/riscv64-linux-musl/qt/bin:/opt/qt-riscv64/bin:${PATH}
ENV APPIMAGE_RUNTIME=/opt/qt-riscv64/riscv64-linux-musl/bin/appimage-runtime
