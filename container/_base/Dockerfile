FROM docker.io/amd64/ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update && \
    apt install --no-install-recommends -y \
        # Red Panda C++
        cmake git make qemu-user \
        fonts-noto fonts-noto-cjk fonts-noto-color-emoji \
        # appimage tools
        squashfs-tools && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
