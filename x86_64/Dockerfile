# RHEL devtoolset, which provides new version of GCC targetting old libgcc_s and libstdc++, is the key to compatibility.
# EL 7 is modern enough for apps and libs.
FROM docker.io/amd64/centos:7

# System
RUN yum install -y centos-release-scl-rh epel-release && \
    yum upgrade -y && \
    yum install -y \
        # general devtools
        devtoolset-7-gcc devtoolset-7-gcc-c++ make \
        # squashfs-tools libs
        libzstd-devel \
        # Qt build tools
        file which \
        # Qt libs
        at-spi2-core-devel dbus-devel fontconfig-devel freetype-devel mesa-libGL-devel wayland-devel \
        libXrender-devel libxcb-devel libxkbcommon-devel libxkbcommon-x11-devel xcb-util-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel xcb-util-wm-devel \
        # Red Panda C++
        git && \
    yum clean all

ARG DEVTOOLSET_ROOTPATH=/opt/rh/devtoolset-7/root
ENV PATH=/opt/qt/bin:${DEVTOOLSET_ROOTPATH}/usr/bin:${PATH}
ENV LD_LIBRARY_PATH=${DEVTOOLSET_ROOTPATH}/usr/lib64

ARG SQUASHFS_TOOLS_VERSION=4.4
ARG QT_MAJOR_MINOR=5.15
ARG QT_PATCH=12
ARG QT_VERSION=${QT_MAJOR_MINOR}.${QT_PATCH}
ARG FCITX5_QT_VERSION=5.0.17

# AppImage runtime
RUN curl -L -o /opt/appimage-runtime 'https://github.com/AppImage/type2-runtime/releases/download/continuous/runtime-x86_64'

# squashfs-tools
RUN mkdir -p /build/squashfs-tools && \
    cd /build/squashfs-tools && \
    curl -L -o squashfs-tools-${SQUASHFS_TOOLS_VERSION}.tar.gz "https://github.com/plougher/squashfs-tools/archive/refs/tags/${SQUASHFS_TOOLS_VERSION}.tar.gz" && \
    tar xf squashfs-tools-${SQUASHFS_TOOLS_VERSION}.tar.gz && \
    cd squashfs-tools-${SQUASHFS_TOOLS_VERSION}/squashfs-tools && \
    make ZSTD_SUPPORT=1 -j$(nproc) && \
    make install && \
    # cleanup
    cd / && \
    rm -r /build/squashfs-tools

# Qt 5
RUN mkdir -p /build/qt5 && \
    cd /build/qt5 && \
    curl -L -O "https://download.qt.io/archive/qt/${QT_MAJOR_MINOR}/${QT_VERSION}/submodules/qt{base,svg,tools,wayland}-everywhere-opensource-src-${QT_VERSION}.tar.xz" && \
    tar xf qtbase-everywhere-opensource-src-${QT_VERSION}.tar.xz && \
    cd qtbase-everywhere-src-${QT_VERSION} && \
    ./configure \
        -prefix /opt/qt \
        -opensource -confirm-license \
        -optimize-size -static -platform linux-g++ -linker bfd \
        -nomake examples -nomake tests -nomake tools -dbus-linked \
        -qt-doubleconversion -no-glib -eventfd -inotify -iconv -no-icu -no-mimetype-database -qt-pcre -qt-zlib \
        -no-openssl \
        -no-cups -fontconfig -system-freetype -qt-harfbuzz -no-gtk -no-opengl -xcb-xlib \
        -xcb \
        -bundled-xcb-xinput \
        -qt-libjpeg -qt-libpng \
        -sql-sqlite -qt-sqlite && \
    make -j$(nproc) && \
    make install && \
    # svg package
    cd /build/qt5 && \
    tar xf qtsvg-everywhere-opensource-src-${QT_VERSION}.tar.xz && \
    cd qtsvg-everywhere-src-${QT_VERSION} && \
    qmake . && \
    make -j$(nproc) && \
    make install && \
    # tools package
    cd /build/qt5 && \
    tar xf qttools-everywhere-opensource-src-${QT_VERSION}.tar.xz && \
    cd qttools-everywhere-src-${QT_VERSION} && \
    qmake . && \
    make -j$(nproc) && \
    make install && \
    # wayland package
    cd /build/qt5 && \
    tar xf qtwayland-everywhere-opensource-src-${QT_VERSION}.tar.xz && \
    cd qtwayland-everywhere-src-${QT_VERSION} && \
    qmake . && \
    make -j$(nproc) && \
    make install && \
    # cleanup
    cd / && \
    rm -r /build/qt5

# fcitx5-qt
RUN yum install -y \
        cmake3 extra-cmake-modules && \
    mkdir -p /build/qt5 && \
    cd /build/qt5 && \
    curl -L -o fcitx5-qt-${FCITX5_QT_VERSION}.tar.gz "https://github.com/fcitx/fcitx5-qt/archive/refs/tags/${FCITX5_QT_VERSION}.tar.gz" && \
    tar xf fcitx5-qt-${FCITX5_QT_VERSION}.tar.gz && \
    cd fcitx5-qt-${FCITX5_QT_VERSION} && \
    cmake3 . -Bbuild -DCMAKE_MODULE_PATH=/opt/qt/lib/cmake -DCMAKE_PREFIX_PATH=/opt/qt -DCMAKE_BUILD_TYPE=Release -DENABLE_QT4=Off -DENABLE_QT5=On -DENABLE_QT6=Off -DBUILD_ONLY_PLUGIN=On -DBUILD_STATIC_PLUGIN=On && \
    cmake3 --build build --parallel && \
    cmake3 --install build && \
    # cleanup
    yum autoremove -y \
        cmake3 extra-cmake-modules && \
    yum clean all && \
    cd / && \
    rm -r /build/qt5
