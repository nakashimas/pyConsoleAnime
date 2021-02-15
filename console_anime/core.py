#!Python3.8
# -*- coding: utf-8 -*-

import sys, os, time, subprocess
import numpy as np
import tqdm

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
    def __init__(self, width = 32, height = 32):
        self.width = width * 2
        self.height = height
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
        if fit_fr:
            subprocess.run(f'ffmpeg -y -i {x} -vf "setpts=1.25*PTS" -loglevel quiet -r 12 tmp.mp4')
        # 動画を読み込み
        cap = cv2.VideoCapture("./tmp.mp4")
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
    def __init__(self, *args, **kwargs):
        BasicImage.__init__(self, *args, **kwargs)
    def __str__(self):
        return "BasicBinaryImage"
    # ======================================================================== # 
    def _convert(self, x):
        # 最適な文字を与える
        pass
    def Convert(self, x, fit_fr = True):
        # フレームレートを変更
        if fit_fr:
            subprocess.run(f'ffmpeg -y -i {x} -vf "setpts=1.25*PTS" -loglevel quiet -r 12 tmp.mp4')
        # 動画を読み込み
        cap = cv2.VideoCapture("./tmp.mp4")
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
                frame = "\n".join(["".join(["#" if j > 127 else " " for j in i]) for i in frame])
                # 追加
                _output.append(frame)
        cap.release()
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

def from_youtube(url, filename = "./from_youtube.%(ext)s"):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": filename
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    _tmp = BasicBinaryImage()
    _tmp.SetLayers(_tmp.Convert(filename))
    return _tmp

if __name__=='__main__':
    pass
    
    
