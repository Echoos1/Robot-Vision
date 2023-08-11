<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Echoos1/Robot-Vision">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">RaspiVision</h3>

  <p align="center">
    Using a Raspberry Pi camera to give an industrial robot 3D spacial tracking
    <br />
    <a href="https://github.com/Echoos1/Robot-Vision"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Echoos1/Robot-Vision">View Demo</a>
    ·
    <a href="https://github.com/Echoos1/Robot-Vision/issues">Report Bug</a>
    ·
    <a href="https://github.com/Echoos1/Robot-Vision/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

Created through a fellowship with [Ballard International](https://ballardintl.com/)

Industrial robots typically are not aware of 3D space, and all positions must be hard-coded in by an operator. The robot vision solutions that currently exist are usually for conveyor tracking in 2D or rough 3D, and full 3D tracking is often quite expensive and application specific.

By using a Raspberry Pi and open source software, this project aims to be a cheap, low-tech, accessible, general purpose solution to 3D robot vision.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![RaspberryPi][RaspberryPi]][RaspberryPi-url]
* [![Python][Python]][Python-url]
* [![OpenCV][OpenCV]][OpenCV-url]
* [![RAPID][RAPID]][RAPID-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Before you begin, you will need:
* Access to an industrial robot
  * ABB Preferred. (You will have to translate your own code for any other brand)
* A Raspberry Pi with python 3
* A Raspberry Pi Camera
* A 3D printer
  * Some kind of 3D modeling software would be helpful

### Prerequisites

On the raspberry pi, you will need an assortment of packages.
You will also need a specific fork and version of OpenCV, numpy, and tqdm
* First, update the pi to the newest set of packages:
  ```sh
  sudo apt update
  sudo apt full-upgrade
  ```
* Then install the dependencies
  ```sh
  sudo apt install libwayland-cursor0 libxfixes3 libva2 libdav1d4 libavutil56 libxcb-render0 libwavpack1 libvorbis0a libx264-160 libx265-192 libaec0 libxinerama1 libva-x11-2 libpixman-1-0 libwayland-egl1 libzvbi0 libxkbcommon0 libnorm1 libatk-bridge2.0-0 libmp3lame0 libxcb-shm0 libspeex1 libwebpmux3 libatlas3-base libpangoft2-1.0-0 libogg0 libgraphite2-3 libsoxr0 libatspi2.0-0 libdatrie1 libswscale5 librabbitmq4 libhdf5-103-1 libharfbuzz0b libbluray2 libwayland-client0 libaom0 ocl-icd-libopencl1 libsrt1.4-gnutls libopus0 libxvidcore4 libzmq5 libgsm1 libsodium23 libxcursor1 libvpx6 libavformat58 libswresample3 libgdk-pixbuf-2.0-0 libilmbase25 libssh-gcrypt-4 libopenexr25 libxdamage1 libsnappy1v5 libsz2 libdrm2 libxcomposite1 libgtk-3-0 libepoxy0 libgfortran5 libvorbisenc2 libopenmpt0 libvdpau1 libchromaprint1 libpgm-5.3-0 libcairo-gobject2 libavcodec58 libxrender1 libgme0 libpango-1.0-0 libtwolame0 libcairo2 libatk1.0-0 libxrandr2 librsvg2-2 libopenjp2-7 libpangocairo-1.0-0 libshine3 libxi6 libvorbisfile3 libcodec2-0.9 libmpg123-0 libthai0 libudfread0 libva-drm2 libtheora0
  sudo pip3 install opencv-contrib-python==4.5.5.62
  sudo pip3 install numpy
  sudo pip3 install tqdm
  ```

* 3D print your monting plate for the gripper.
  * My STL files are included for the ABB IRB 4600-45/2.05 Type A with an unknown gripper module. It is likely you will have to create your own mount for the gripper/camera.
  * If you use a different mount, you will also need to modify the tooldata parameters in `Robot Code\BASE.mod`
  
* Print both ArUCo Tag Boards in `Boards` on 8.5"x11" paper at 100% scale. The size is very important. The size of each tag should be 30x30mm and each space between tags to be 10mm.
  * Mount the boards to a flat surface, or otherwise ensure the boards are flat whenever they are viewed by the camera
### Installation

1. Download all files from the repository
2. Move the "Robot Code" folder onto a USB and then onto the robot.
   * Open the *.pgf file to load the program on the robot.
3. When your camera is attached to the Pi, take around 40 pictures of the first `ArUCo Tags 0 - 29; Pickup Location` tag board and put the photos in `Pi Code\calib_imgs`. Then run `Pi Code\Calibrate_Camera.py`.

### Camera Wiring

The camera will need to be wired properly to the I/O connections of the robot.

> PLEASE NOTE: This wiring is for the R2.CS plug on the ABB IRB 4600. Other models may have similar plugs, or not at all. The wires in the diagram are also labeled with their respective I/O signal, so if you are using a different robot, use that as a guide for proper communication wiring.

![WiringDiagram][WiringDiagram]

Because the robot I/O is 24v, and the Pi is 3.3v, all signals between the two will need to be converted.

24v to 3.3v: [Amazon](https://www.amazon.com/DZS-Elec-Converter-Adjustable-Regulator/dp/B07JWGN1F6/ref=sr_1_5?crid=2RQXZ117LP9O3&keywords=24v+to+3.3v+dc+converter&qid=1686676501&sprefix=24v+to+3.3v+dc+converter%2Caps%2C152&sr=8-5)

3.3v to 24v: [Amazon](https://www.amazon.com/Converter-Adjustable-Voltage-Regulator-Compatible/dp/B09S8ZDVBN/ref=sr_1_6?crid=2ST5BG6NCYT7B&keywords=3.3v%2Bto%2B24v%2Bboost%2Bconverter&qid=1686677500&sprefix=3.3v%2Bto%2B24v%2Bboost%2Bconverter%2Caps%2C112&sr=8-6&th=1)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Standard Use

1. Load and run the program on the robot
2. Load and run `Pi Code\RapsiVision.py` on the pi
3. Wait for the camera and the robot to synchronize
   * The robot pendant and the camera console will print status information
3. Press play on the robot to locate a visible board to move to

### Debug and Testing Features

* `Pi Code\GPIO_debug.py` will give you control over the I/O signals from the Pi to test the connections to the robot
* `Pi Code\Vision_Test.py` will run the camera and locating script locally
  * This is designed to be run on a PC with a webcam, rather than the pi

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add movement options for both Tag Boards on the robot
- [ ] Add a scanning procedure to find boards anywhere around the robot
- [ ] Improve accuracy
- [ ] Improve photo analysis speed
- [ ] Improve Cam-Robot communication speed

See the [open issues](https://github.com/Echoos1/Robot-Vision/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Matthew DiMaggio - matthew@grandfinaletech.com

Project Link: [https://github.com/Echoos1/Robot-Vision](https://github.com/Echoos1/Robot-Vision)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Ballard International](https://ballardintl.com/)
* [Lawrence Technological University](https://ltu.edu/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Echoos1/Robot-Vision.svg?style=for-the-badge
[contributors-url]: https://github.com/Echoos1/Robot-Vision/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Echoos1/Robot-Vision.svg?style=for-the-badge
[forks-url]: https://github.com/Echoos1/Robot-Vision/network/members
[stars-shield]: https://img.shields.io/github/stars/Echoos1/Robot-Vision.svg?style=for-the-badge
[stars-url]: https://github.com/Echoos1/Robot-Vision/stargazers
[issues-shield]: https://img.shields.io/github/issues/Echoos1/Robot-Vision.svg?style=for-the-badge
[issues-url]: https://github.com/Echoos1/Robot-Vision/issues
[license-shield]: https://img.shields.io/github/license/Echoos1/Robot-Vision.svg?style=for-the-badge
[license-url]: https://github.com/Echoos1/Robot-Vision/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/matthew-dimaggio-372039235
[product-screenshot]: images/screenshot.jpg
[WiringDiagram]: images/wiring_diagram.png

[Python]: https://img.shields.io/badge/Python-306998?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[RAPID]: https://img.shields.io/badge/RAPID-FF000E?style=for-the-badge&logo=abbrobotstudio&logoColor=white
[RAPID-url]: https://search.abb.com/library/Download.aspx?DocumentID=3HAC050917-001&LanguageCode=en&DocumentPartId=&Action=Launch

[OpenCV]: https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/

[RaspberryPi]: https://img.shields.io/badge/Raspberry_Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white
[RaspberryPi-url]: https://www.raspberrypi.com/