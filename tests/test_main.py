"""test"""

# pylint: disable=(import-error, invalid-name, unnecessary-pass)
import time

import cv2
import numpy as np
from src.main import (
    _clicks,
    task_cam,
    task_gst,
    task_img,
    task_v4l2,
    task_video,
)


def test_task_v4l2(monkeypatch):
    """test for task_v4l2"""
    seen = []
    monkeypatch.setattr("src.main.run", lambda cmd: seen.append(cmd) or 0)
    res = task_v4l2()
    assert res["device"] == "/dev/video0"
    assert res["brightness"] == 128
    assert len(res["commands"]) == 3
    assert "--list-ctrls" in res["commands"][0]


def test_task_gst(monkeypatch):
    """test for task_gst"""
    holder = {}
    monkeypatch.setattr(
        "src.main.run", lambda cmd: holder.setdefault("cmd", cmd) or 0
    )
    res = task_gst()
    assert "gst-launch-1.0" in res["cmd"]
    assert res["output"] == "gst_output.mp4"


def test_task_img(monkeypatch):
    """test for task_img"""
    dummy = np.zeros((100, 200, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "imread", lambda _: dummy)
    monkeypatch.setattr(
        cv2,
        "resize",
        lambda img, dsize, interpolation: np.zeros(
            (150, 300, 3), dtype=np.uint8
        ),
    )
    monkeypatch.setattr(cv2, "imwrite", lambda p, img: True)
    res = task_img()
    assert res["ok"] is True
    assert res["orig_size"] == (100, 200)
    assert res["new_size"] == (150, 300)


def test_task_video(monkeypatch):
    """test for task_video"""

    class FakeCap:
        """fake cap"""

        def __init__(self, *_):
            self.n = 0

        def isOpened(self):
            """fake isOpend"""
            return True

        def get(self, prop):
            """fake get"""
            if prop == cv2.CAP_PROP_FPS:
                return 30.0

            if prop == cv2.CAP_PROP_FRAME_WIDTH:
                return 200

            if prop == cv2.CAP_PROP_FRAME_HEIGHT:
                return 100

            return 0

        def read(self):
            """fake read"""
            if self.n < 2:
                self.n += 1
                return True, np.zeros((100, 200, 3), dtype=np.uint8)
            return False, None

        def release(self):
            """fake release"""
            pass

    class FakeWriter:
        """fake writer"""

        def __init__(self, *_a):
            self._open = True
            self.w = 0

        def isOpened(self):
            """fake isOpened"""
            return True

        def write(self, _f):
            """fake write"""
            self.w += 1

        def release(self):
            """fake release"""
            self._open = False

    monkeypatch.setattr(cv2, "VideoCapture", lambda *_: FakeCap())
    monkeypatch.setattr(cv2, "VideoWriter_fourcc", lambda *a: 0)
    monkeypatch.setattr(cv2, "VideoWriter", lambda *a: FakeWriter())
    monkeypatch.setattr(cv2, "rotate", lambda f, _: np.transpose(f, (1, 0, 2)))

    res = task_video()
    assert res["ok"] is True
    # 입력 200x100 → 회전 후 out_size(h,w) = (200,100)
    assert res["out_size"] == (200, 100)
    assert res["frames"] == 2


def test_task_cam(monkeypatch):
    """test for task_cam"""
    # time을 0,6,7 순으로 반환해서 1~2회 루프 후 종료되게 함
    ticks = iter([0.0, 6.1, 7.0])
    monkeypatch.setattr(time, "time", lambda: next(ticks))

    class FakeCap:
        """fake cap"""

        def __init__(self, *_):
            pass

        def isOpened(self):
            """fake isOpened"""
            return True

        def set(self, *_):
            """fake set"""
            return True

        def read(self):
            """fake read"""
            return True, np.zeros((480, 640, 3), dtype=np.uint8)

        def release(self):
            """fake release"""
            pass

    # GUI 함수 no-op
    monkeypatch.setattr(cv2, "VideoCapture", lambda *_: FakeCap())
    monkeypatch.setattr(cv2, "namedWindow", lambda *_: None)
    monkeypatch.setattr(cv2, "setMouseCallback", lambda *_: None)
    monkeypatch.setattr(cv2, "circle", lambda *a, **k: None)
    monkeypatch.setattr(cv2, "imshow", lambda *_: None)
    monkeypatch.setattr(cv2, "waitKey", lambda *_: -1)
    monkeypatch.setattr(cv2, "destroyAllWindows", lambda: None)

    _clicks.clear()
    _clicks.append((10, 20))

    res = task_cam()
    assert res["ok"] is True
    assert res["clicks"] == 1
    assert res["frames_shown"] >= 1
