

<h1 align="center">
  <br>
  pyConsoleAnime
  <br>
</h1>

<h4 align="center"></h4>

<p align="center">
  <a>
    <img src="https://img.shields.io/badge/build-passing-brightgreen">
  </a>
  <a href="https://github.com/nakashimas/pyConsoleAnime/releases">
    <img src="https://img.shields.io/badge/releace-v0.0.0-58839b.svg?style=flat">
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

**持っている動画を変換して再生する方法.**

```py
from console_anime import *

my_img = BasicBinaryImage()
my_img.SetLayers(my_img.Convert("path/to/video.mp4"))

my_anime = BasicConsoleAnime()
my_anime.SetLayers(my_img)

my_anime.Run()
```

BasicBinaryImageは, 画像を二値化して, 指定した文字で白と黒を置き換えます.

この例は, 勿論, 他の画像変換クラスでも同じ.
(一番生成が軽量なものはBasicBinaryImage)

```py
from console_anime import *

my_img = MultiStringBinaryImage() # here
my_img.SetLayers(my_img.Convert("path/to/video.mp4"))

my_anime = BasicConsoleAnime()
my_anime.SetLayers(my_img)

my_anime.Run()
```

MultiStringBinaryImageはグレースケールにした画像をAscii文字で置換します.

変換が遅い(要改良)です.kernel_size引数を下げたり, frame_rate引数を下げたりして精度を落とすと,
早くなります. 

また, 単にlow_passやhigh_passパラメータを設定しても早くなります. その場合, 値がhigh_passよりも大きい場合に「M」が, low_passよりも小さい場合に「 」が割り当てられます.

**youtubeの動画を変換して再生する方法. (BadApple!!を例に)**

```py
from console_anime import *
my_img = basic_binaly_from_youtube("https://youtu.be/FtutLA63Cp8", filename = "./tmp.mp4", width = 48, height = 36)
my_anime = BasicConsoleAnime(width = 48, height = 36)
my_anime.SetLayers(my_img)
my_anime.Run()
```

ここに動画を貼っていいのかわからないので, 結果は試してみてください.

## Requirements

requirements

- Python (above 3.8.0)
- numpy

(optional)

- ffmpeg (build with gcc 9.2.1)
- youtube_dl
- opencv
- PIL


See also [requirements.txt](./requirements.txt).

## Download

for pip

```sh
pip install git+https://github.com/nakashimas/pyConsoleAnime
```

download project

```sh
git clone --depth 1 https://github.com/nakashimas/pyConsoleAnime
```

or [releases](https://github.com/nakashimas/pyConsoleAnime/releases)

## License

The _pyConsoleAnime_ project is licensed under the terms of the [MIT](./LICENSE).

## Author

_pyConsoleAnime_ authors.
