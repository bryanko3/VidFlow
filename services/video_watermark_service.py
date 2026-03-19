import cv2
import os
from config import Config
import subprocess

def create_protected_video(input_video, output_video, username, watermark_path):

    command = [
        "ffmpeg",
        "-i", input_video,
        "-i", watermark_path,

        "-filter_complex",
        f"overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2,"
        f"drawtext=text='@{username}':x=w-tw-20:y=40:fontsize=32:fontcolor=white",

        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "28",
        "-y",
        output_video
    ]

    subprocess.run(command)

def add_watermark(original_path, output_path, username, watermark_path=None):

    cap = cv2.VideoCapture(original_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    wm_img = None

    if watermark_path and os.path.exists(watermark_path):

        wm_img = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)

        h, w = wm_img.shape[:2]

        max_w = int(width * 0.5)

        scale = max_w / w

        new_w = int(w * scale)
        new_h = int(h * scale)

        wm_img = cv2.resize(wm_img, (new_w, new_h))

        wm_x = (width - new_w) // 2
        wm_y = (height - new_h) // 2

        overlay = wm_img[:, :, :3]
        alpha = wm_img[:, :, 3] / 255.0

        alpha = alpha * 0.25

    text = f"@{username}"

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

    text_x = width - text_width - 20
    text_y = 40

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        if wm_img is not None:

            for c in range(3):
                frame[
                    wm_y:wm_y + overlay.shape[0],
                    wm_x:wm_x + overlay.shape[1],
                    c
                ] = (
                    frame[
                        wm_y:wm_y + overlay.shape[0],
                        wm_x:wm_x + overlay.shape[1],
                        c
                    ] * (1 - alpha) +
                    overlay[:, :, c] * alpha
                )

        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )

        out.write(frame)

    cap.release()
    out.release()