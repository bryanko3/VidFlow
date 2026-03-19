import cv2
import os
from config import Config


def create_thumbnail(video_path, filename):

    thumb_path = os.path.join(Config.THUMB_FOLDER, f"{filename}.jpg")

    os.system(f'ffmpeg -i "{video_path}" -ss 00:00:01 -vframes 1 "{thumb_path}"')

    cap = cv2.VideoCapture(video_path)

    success, frame = cap.read()

    if success:
        cv2.imwrite(thumb_path, frame)

    cap.release()