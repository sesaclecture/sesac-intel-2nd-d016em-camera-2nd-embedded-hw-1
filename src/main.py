# pylint: disable=import-error
"""
SeSAC 과제 모음 (파라미터 없이 실행 / 하드코딩 값 사용)
- Q1: v4l2-ctl 제어
- Q2: GStreamer로 짧게 녹화 (자동 종료)
- Q3: OpenCV 이미지 1.5배 확대 저장
- Q4: OpenCV 비디오 90도 회전 저장
- Q5: OpenCV 카메라 미리보기 + 마우스 클릭 원 (짧게 자동 종료)
"""

import shlex
import subprocess as sp
import time

import cv2


def run(cmd: str) -> int:
    """wrapper for subprocess call with error handling"""
    print(f"[RUN] {cmd}")
    try:
        return sp.call(shlex.split(cmd))
    except FileNotFoundError as e:
        print(f"[ERR] 명령을 찾을 수 없습니다: {e}")
        return 127


_clicks = []  # 좌표 누적


def _on_mouse(event, x, y, _flags, _param):
    if event == cv2.EVENT_LBUTTONDOWN:
        _clicks.append((x, y))


def task_v4l2():
    """
    [Q1] v4l2-ctl 제어
    - 카메라 장치(/dev/video0)의 제어 항목(ctrls)을 나열한다.
    - brightness 값을 지정 값(128)으로 변경한다.
    - brightness 값을 다시 읽어 확인한다.
    """
    # TODO: device, brightness 값을 환경에 맞게 조정
    device = ""
    brightness = -1
    cmds = [
            "..."
    ]

    for c in cmds:
        run(c)

    return {"device": device, "brightness": brightness, "commands": cmds}


def task_gst():
    """
    [Q2] GStreamer 파이프라인
    - GStreamer를 이용해 카메라 입력을 gst_output.mp4 파일로 저장한다.
    - v4l2src → videoconvert → x264enc → mp4mux → filesink 파이프라인을 구성.
    - num-buffers를 설정하여 짧게 녹화 후 자동 종료되도록 한다.
    """
    # TODO: device, out_mp4 값을 환경에 맞게 조정
    device = ""
    out_mp4 = ""
    cmd = (...)
    run(cmd)
    return {"device": device, "output": out_mp4, "cmd": cmd}


def task_img():
    """
    [Q3] OpenCV 이미지 처리
    - 이미지(lenna.png)를 읽는다.
    - 1.5배 확대하여 새로운 파일(lenna_big.png)로 저장한다.
    - 원본 크기와 변경된 크기를 출력으로 확인한다.
    """
    inp, outp, scale = "lenna.png", "lenna_big.png", 1.5
    # TODO: 코드 구현

    img = cv2.imread(inp)
    if img is None:
        return {"ok": False, "reason": f"missing_input:{inp}"}

    h, w = 0, 0
    new = None
    ok = None
    return {
        "ok": ok,
        "input": inp,
        "output": outp,
        "orig_size": (h, w),
        "new_size": (int(h * scale), int(w * scale)),
    }


def task_video():
    """
    [Q4] OpenCV 비디오 처리
    - 동영상(ronaldinho.mp4)을 읽는다.
    - 각 프레임을 90도 시계 방향으로 회전한다.
    - 회전된 영상을 rotated.mp4로 저장한다.
    - 저장 완료 후 fps, frame 수, 최종 크기를 로그로 출력한다.
    """
    inp, outp = "ronaldinho.mp4", "rotated.mp4"
    # TODO: 코드 구현

    cap = cv2.VideoCapture(inp)
    if not cap.isOpened():
        return {"ok": False, "reason": f"missing_input:{inp}"}

    fps = 0
    in_w = 0
    in_h = 0
    out_w, out_h = in_h, in_w

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(outp, fourcc, fps, (out_w, out_h))
    if not out.isOpened():
        cap.release()
        return {"ok": False, "reason": "videowriter_open_failed"}

    frames = 0
    while True:
        break

    cap.release()
    out.release()
    return {
        "ok": True,
        "output": outp,
        "fps": fps,
        "frames": frames,
        "out_size": (out_h, out_w),
    }


def task_cam():
    """
    [Q5] OpenCV 카메라 처리
    - 카메라(인덱스 0)를 열고 해상도(640x480)를 설정한다.
    - 미리보기 창을 띄우고 5초간 실행한다.
    - 마우스 왼쪽 버튼을 클릭하면 해당 좌표에 원(circle)을 그린다.
    - 'q' 키 입력 시 즉시 종료할 수 있도록 한다.
    """
    # TODO: 코드 구현
    index = 0
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
    if not cap.isOpened():
        return {"ok": False, "reason": f"camera_open_failed:{index}"}

    # TODO: 해상도 설정
    cap.set()
    cap.set()

    cv2.namedWindow("Camera")

    # 마우스 콜백 설정
    cv2.setMouseCallback()

    start = time.time()
    shown = 0
    while True:
        if time.time() - start > 5:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return {"ok": True, "frames_shown": shown, "clicks": len(_clicks)}


if __name__ == "__main__":
    task_v4l2()
    task_gst()
    task_img()
    task_video()
    task_cam()
