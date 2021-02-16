#!Python3.8
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, string
import numpy as np
import tqdm
from PIL import Image, ImageDraw, ImageFont

try:
    import youtube_dl
    import cv2
except Exception:
    pass

class BasicImage:
    """BasicImage

    Raises:
        StopIteration: for iterator

    Returns:
        None
    """
    # ======================================================================== # 
    def __init__(self, width = 32, height = 32, frame_rate = 12):
        self.width = width * 2
        self.height = height
        self.frame_rate = frame_rate
        self.timeline = []
        self._c_timeline = []
    def __iter__(self):
        self._c_timeline = self.timeline.copy()
        return self
    def __next__(self):
        if len(self._c_timeline) > 0:
            return self._c_timeline.pop(0)
        else:
            raise StopIteration()
    def __str__(self):
        return "BasicImage"
    def __getitem__(self, k):
        return self.timeline[k]
    # ======================================================================== # 
    def pop(self, k):
        return self.timeline.pop(k)
    def push(self, x):
        self.timeline.append(x)
    def Convert(self, x):
        pass
    def Deconvert(self):
        pass
    # ======================================================================== # 
    def GetWidth(self):
        return self.width
    def GetHeight(self):
        return self.height
    def GetLayers(self):
        return self.timeline
    # ======================================================================== # 
    def SetWidth(self, x):
        self.width = x
    def SetHeight(self, x):
        self.height = x
    def SetLayers(self, x):
        self.timeline = x
    def SetLayer(self, x, idx):
        self.timeline[idx] = x
    def AddLayer(self, x):
        self.timeline.append(x)

class BasicBinaryImage(BasicImage):
    """BasicBinaryImage

    boolで表現された白黒画像を入力し, 二つの文字で表現して返す

    Raises:
        StopIteration: for iterator

    Returns:
        None
    """
    # ======================================================================== # 
    def __init__(self, *args, **kwargs):
        BasicImage.__init__(self, *args, **kwargs)
    def __str__(self):
        return "BasicBinaryImage"
    # ======================================================================== # 
    def Convert(self, x, str_white = "#", str_black = " ", fit_fr = True):
        # フレームレートを変更
        _tmp_file = "./_" + os.path.splitext(os.path.basename(x))[0] + ".mp4"
        if fit_fr:
            subprocess.run(f'ffmpeg -y -i {x} -vf "setpts=1.25*PTS" -loglevel quiet -r {self.frame_rate} {_tmp_file}')
        else:
            _tmp_file = x
        # 動画を読み込み
        cap = cv2.VideoCapture(_tmp_file)
        _fr = int(cap.get(cv2.CAP_PROP_FPS))
        _total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = cap.read()
        _output = []
        _height = self.GetHeight()
        _width = self.GetWidth()
        _fx = _width / cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        _fy = _height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        with tqdm.tqdm(total = _total) as pbar:
            while True:
                pbar.update(1)
                ret, frame = cap.read()
                if ret == False:
                    break
                # 加工
                frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)[1]
                frame = cv2.resize(frame, None, fx = _fx, fy = _fy)
                frame = np.reshape(frame, (1, int(_height), int(_width), 3))
                frame = np.sum(frame, axis = 3) / 3
                frame = frame[0]
                frame = "\n".join(["".join([str_white if j > 127 else str_black for j in i]) for i in frame])
                # 追加
                _output.append(frame)
        cap.release()
        if fit_fr:
            if os.path.exists(_tmp_file):
                os.remove(_tmp_file)
        return _output
    def Deconvert(self):
        pass
    # ======================================================================== # 

class MultiStringBinaryImage(BasicImage):
    """BasicBinaryImage

    boolで表現された白黒画像を入力し, 文字で表現して返す

    Raises:
        StopIteration: for iterator

    Returns:
        None
    """
    # ======================================================================== # 
    def __init__(self, *args, kernel_size = 32, high_cut = None, low_cut = None, **kwargs):
        BasicImage.__init__(self, *args, **kwargs)
        self.kernel_size = kernel_size
        self.high_cut = high_cut
        self.low_cut = low_cut
        if self.low_cut is None:
            self.low_cut = -1
        if self.high_cut is None:
            self.high_cut = 1E+99
        # fit用のデータ
        self.printable_strings = ""
        self.string_params = None
    def __str__(self):
        return "BasicBinaryImage"
    # ======================================================================== # 
    def _convert(self, x):
        if self.string_params is None:
            self.string_params, self.printable_strings = make_ascii_dict(
                width = self.kernel_size, height = self.kernel_size * 2
            )
        # 畳み込みを作成
        _output = []
        img = x
        _outshape = (int(img.shape[1]), int(img.shape[0]))
        img = cv2.resize(img, None, fx = self.kernel_size, fy = self.kernel_size * 2)
        for y in range(_outshape[1]):
            for x in range(_outshape[0]):
                # カーネル作成
                _kernel = np.ravel(
                    img[
                        (y * self.kernel_size * 2):((y + 1) * self.kernel_size * 2), 
                        (x * self.kernel_size):((x + 1) * self.kernel_size)
                    ]
                )
                if np.sum(_kernel) < self.low_cut:
                    _output.append(" ")
                elif np.sum(_kernel) > self.high_cut:
                    _output.append("#")
                else:
                    # 繰り返し
                    _kernel = np.repeat(_kernel[None, :], self.string_params.shape[0], axis = 0)
                    # ユークリッド距離が最小のものを選択
                    _euc = np.argmin(np.sqrt(np.mean((_kernel - self.string_params) ** 2, axis = 1)))
                    _output.append(self.printable_strings[_euc])
            _output.append("\n")
        return "".join(_output)
    def Convert(self, x, fit_fr = True):
        # フレームレートを変更
        _tmp_file = "./_" + os.path.splitext(os.path.basename(x))[0] + ".mp4"
        if fit_fr:
            subprocess.run(f'ffmpeg -y -i {x} -vf "setpts=1.25*PTS" -loglevel quiet -r {self.frame_rate} {_tmp_file}')
        else:
            _tmp_file = x
        # 動画を読み込み
        cap = cv2.VideoCapture(_tmp_file)
        _fr = int(cap.get(cv2.CAP_PROP_FPS))
        _total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = cap.read()
        _output = []
        _height = self.GetHeight()
        _width = self.GetWidth()
        _fx = _width / cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        _fy = _height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        with tqdm.tqdm(total = _total) as pbar:
            while True:
                pbar.update(1)
                ret, frame = cap.read()
                if ret == False:
                    break
                # 加工
                frame = cv2.resize(frame, None, fx = _fx, fy = _fy)
                frame = np.reshape(frame, (1, int(_height), int(_width), 3))
                frame = np.mean(frame, axis = 3)
                frame = frame[0]
                frame = self._convert(frame)
                # 追加
                _output.append(frame)
        cap.release()
        if fit_fr:
            if os.path.exists(_tmp_file):
                os.remove(_tmp_file)
        return _output
    def Deconvert(self):
        pass
    # ======================================================================== # 

class BasicConsoleAnime:
    """BasicConsoleAnime

    Raises:
        StopIteration: for iterator

    Returns:
        None
    """
    # ======================================================================== # 
    def __init__(self, width = 32, height = 32, frame_rate = 12):
        self.width = width * 2 # 縦との整合性 
        self.height = height
        self.frame_rate = frame_rate
        self.timeline = []
        # private attr
        self._previous_time = 0
        self._previous_frame_number = 0
        self._c_timeline = []
        # optional
        self.header = ("-" * (self.width + 2))
        self.footer = "-" * (self.width + 2)
        self.left_content = "|\n" * self.height
        self.right_content = "|\n" * self.height
    def __del__(self):
        if not (len(self._c_timeline) < 1):
            print(self._c_timeline.pop(0))
    def __iter__(self):
        self.Update()
        self._previous_frame_number = 0
        _layer = self.GetLayers()
        # ヘッダーとフッター、左右を追加
        _layer = [
            "\n".join(
                [
                    j + k + l for j, k, l in zip(
                        self.left_content.split("\n"),
                        i.split("\n"), 
                        self.right_content.split("\n")
                    )
                ]
            ) for i in _layer
        ]
        _layer = [str(self.header) + "\n" + str(i) + "\n" + str(self.footer) for i in _layer]
        self._c_timeline = _layer
        return self
    def __next__(self):
        os.system('cls' if os.name=='nt' else 'clear')
        self._previous_frame_number += 1
        print(self._c_timeline.pop(0))
        if (len(self._c_timeline) < 1):
            raise StopIteration()
        return None
    def __str__(self):
        return "BasicConsoleAnime"
    # ======================================================================== # 
    def Update(self):
        pass
    def Run(self):
        self._previous_time = time.time()
        for _ in self:
            _tmp = (1 / self.frame_rate) - (time.time() - self._previous_time)
            if _tmp > 0:
                time.sleep(_tmp)
            self._previous_time = time.time()
    # ======================================================================== # 
    def GetWidth(self):
        return self.width
    def GetHeight(self):
        return self.height
    def GetLayers(self):
        return self.timeline
    def GetLayer(self, x):
        return self.timeline[x]
    def GetLeftContent(self):
        return self.left_content
    def GetRightContent(self):
        return self.right_content
    def GetHeader(self):
        return self.header
    def GetFooter(self):
        return self.footer
    # ======================================================================== # 
    def SetWidth(self, x):
        self.width = x
    def SetHeight(self, x):
        self.height = x
    def SetLayers(self, x):
        self.timeline = x
    def SetLayer(self, x, idx):
        self.timeline[idx] = x
    def AddLayer(self, x):
        self.timeline.append(x)
    def SetLeftContent(self, x):
        self.left_content = x
    def SetRightContent(self, x):
        self.right_content = x
    def SetHeader(self, x):
        self.header = x
    def SetFooter(self, x):
        self.footer = x

def make_ascii_dict(width = 64, height = 128, img_write = False):
    _str = repr(string.printable)[:-16]
    _output = np.ravel(np.zeros((height, width)))[None,:]
    img = np.zeros((90, 50, 3))
    if img_write:
        cv2.imwrite("./_resource/base.png", img)
    for idx, i in enumerate(_str):
        img = cv2.imread("./_resource/base.png")
        img_p = Image.fromarray(img)
        d = ImageDraw.Draw(img_p)
        d.text((2.5,0), i, font = ImageFont.truetype("./_resource/fonts/msgothic.ttc", 90), fill = (255, 255, 255))
        img = np.array(img_p)
        img = cv2.resize(img, (width, height))
        kernel = np.ones((8,8),np.float32) / 25
        img = cv2.filter2D(img, -1, kernel)
        img = cv2.GaussianBlur(img, (15, 15), 3)
        if img_write:
            cv2.imwrite("./_resource/gen/" + str(idx) + ".png", img)
        _output = np.append(_output, np.ravel(np.mean(img, axis = 2))[None,:], axis = 0)
    _str = " " + _str
    return _output, _str

def basic_binaly_from_youtube(url, filename = "./from_youtube.%(ext)s", **kwargs):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": filename
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    _tmp = BasicBinaryImage(**kwargs)
    _tmp.SetLayers(_tmp.Convert(filename))
    return _tmp

def multi_string_binaly_from_youtube(url, filename = "./from_youtube.%(ext)s", **kwargs):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": filename
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    _tmp = MultiStringBinaryImage(**kwargs)
    _tmp.SetLayers(_tmp.Convert(filename))
    return _tmp

if __name__=='__main__':
    pass
    
    
