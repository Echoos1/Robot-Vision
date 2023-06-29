# Robot Vision
> Custom implementation of Robot Vision

Uses OpenCV and a Raspberry Pi + Pi Cameras to create a Robot Vision system for Industrial Robotics utilizing ArUCo Fudicial Markers for 3D Spacial Tracking

## Installing / Getting started

On the Raspberry Pi, python 3 is required

```shell
sudo apt install libwayland-cursor0 libxfixes3 libva2 libdav1d4 libavutil56 libxcb-render0 libwavpack1 libvorbis0a libx264-160 libx265-192 libaec0 libxinerama1 libva-x11-2 libpixman-1-0 libwayland-egl1 libzvbi0 libxkbcommon0 libnorm1 libatk-bridge2.0-0 libmp3lame0 libxcb-shm0 libspeex1 libwebpmux3 libatlas3-base libpangoft2-1.0-0 libogg0 libgraphite2-3 libsoxr0 libatspi2.0-0 libdatrie1 libswscale5 librabbitmq4 libhdf5-103-1 libharfbuzz0b libbluray2 libwayland-client0 libaom0 ocl-icd-libopencl1 libsrt1.4-gnutls libopus0 libxvidcore4 libzmq5 libgsm1 libsodium23 libxcursor1 libvpx6 libavformat58 libswresample3 libgdk-pixbuf-2.0-0 libilmbase25 libssh-gcrypt-4 libopenexr25 libxdamage1 libsnappy1v5 libsz2 libdrm2 libxcomposite1 libgtk-3-0 libepoxy0 libgfortran5 libvorbisenc2 libopenmpt0 libvdpau1 libchromaprint1 libpgm-5.3-0 libcairo-gobject2 libavcodec58 libxrender1 libgme0 libpango-1.0-0 libtwolame0 libcairo2 libatk1.0-0 libxrandr2 librsvg2-2 libopenjp2-7 libpangocairo-1.0-0 libshine3 libxi6 libvorbisfile3 libcodec2-0.9 libmpg123-0 libthai0 libudfread0 libva-drm2 libtheora0
sudo pip3 install opencv-contrib-python
sudo pip3 install numpy
sudo pip3 install tqdm
```

This will install all the required dependencies

## Features

The program will
* Communicate with an industrial robot with simple I/O handshakes
* Analyze camera when prompted
* Locate ArUCo boards in 3D rotational space
* Send pose to the robot with simple I/O binary signals

## Contributing

This project was created by an untrained, self-taught deveoper still learning the
standard practices of software development and deployment.

Any and all contributions are very welcome!

## Links

- Project homepage: https://github.com/Echoos1/Robot-Vision
- Repository: https://github.com/Echoos1/Robot-Vision
- Issue tracker: https://github.com/Echoos1/Robot-Vision/issues

## Licensing

The code in this project is licensed under MIT license.