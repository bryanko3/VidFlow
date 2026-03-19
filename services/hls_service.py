import subprocess
import os
import secrets
from config import Config


def create_hls(input_video, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(input_video)

    playlist = os.path.join(output_dir, "playlist.m3u8")

    key_filename = f"{filename}.key"
    key_path = os.path.join(Config.KEY_FOLDER, key_filename)

    with open(key_path, "wb") as f:
        f.write(secrets.token_bytes(16))

    key_info_filename = f"{filename}_keyinfo.txt"
    key_info_path = os.path.join(Config.KEY_FOLDER, key_info_filename)

    with open(key_info_path, "w") as f:

        f.write(f"/key/{key_filename}\n")

        f.write(f"{key_path}\n")

    command = [
        "ffmpeg",
        "-i", input_video,

        "-codec:v", "libx264",
        "-codec:a", "aac",

        "-preset", "fast",

        "-hls_time", "6",
        "-hls_list_size", "0",

        "-hls_key_info_file", key_info_path,

        "-f", "hls",

        playlist
    ]

    subprocess.run(command)

    return playlist