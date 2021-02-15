

<h1 align="center">
  <br>
  pyConsoleAnime
  <br>
</h1>

<h4 align="center"></h4>

<p align="center">
  <a>
    <img src="https://img.shields.io/badge/build-not--yet-red">
    <!-- <img src="https://img.shields.io/badge/build-passing-brightgreen"> -->
  </a>
  <a href="https://github.com/nakashimas/pyConsoleAnime/releases">
    <img src="https://img.shields.io/badge/releace-None-58839b.svg?style=flat">
  </a>
  <a href="./LICENSE">
    <img src="http://img.shields.io/badge/license-MIT-blue.svg?style=flat">
  </a>
  <br>
  <a>
    <img src="https://img.shields.io/badge/platform-win--32%20%7C%20win--64%20%7C%20CentOS-lightgrey">
  </a>
</p>

<h2> Contents </h2>

- [Description](#description)
- [Usage](#usage)
- [Requirements](#requirements)
- [Download](#download)
- [License](#license)
- [Author](#author)

## Description

_pyConsoleAnime_ is a kind of toy that plays animations on the command line.

## Usage

```py
from console_anime import *
my_img = BasicBinaryImage(width = 50, height = 30)
my_img.SetLayers(my_img.Convert("./out.mp4"))
my_anime = BasicConsoleAnime(width = 50, height = 30)
my_anime.SetLayers(_o)
my_anime.Run()
```

## Requirements

requirements

- Python (above 3.8.0)
- numpy

optional

- ffmpeg (build with gcc 9.2.1)
- youtube_dl
- opencv


See also [requirements.txt](./requirements.txt).

## Download

```sh
git clone --depth 1 https://github.com/nakashimas/pyConsoleAnime
```

or [releases](https://github.com/nakashimas/pyConsoleAnime/releases)

## License

The _pyConsoleAnime_ project is licensed under the terms of the [BSD 2-Clause](./LICENSE).

## Author

_pyConsoleAnime_ authors.
