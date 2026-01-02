# Red Panda C++ AppImage Build Environment

## Use (Build Red Panda C++)

Please refer to [Red Panda C++’s document](https://github.com/royqh1979/RedPanda-CPP/blob/master/BUILD.md).

## Build (Build This Project)

### Build the Tools and Libraries

1. Launch container:
   ```bash
   podman run -it --rm \
     --cap-add=sys_admin \
     -v $PWD:/mnt -w /mnt \
     docker.io/amd64/ubuntu:24.04
   ```
   To expose build directories for debugging:
   ```bash
   podman run -it --rm \
     --cap-add=sys_admin \
     -v $PWD:/mnt -w /mnt \
     -v $PWD/build:/tmp/build \
     -v $PWD/layer:/tmp/layer \
     docker.io/amd64/ubuntu:24.04
   ```
2. Install dependencies:
   ```bash
   ./support/dep.sh
   ```
3. Build the project:
   ```bash
   ./main.sh -a <arch> -b <branch>
   ```

### Build the Container Image

```
podman build -t redpanda-cpp/appimage-builder-<arch> container/<arch>
```
