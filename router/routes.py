import math
import os
import random
import subprocess
import threading
import time

import cv2
import numpy as np
import requests
from flask import send_from_directory, request, Blueprint, Response, stream_with_context, jsonify
from ultralytics import YOLO

from utils.app_root_dir import app_root_dir
from utils.get_file_path import get_file_path
from utils.parse_ini_file import parse_ini_file

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
@routes_bp.route('/image-recognition')
@routes_bp.route('/video-recognition')
@routes_bp.route('/live-recognition')
@routes_bp.route('/recognition')
@routes_bp.route('/settings/check-update')
@routes_bp.route('/changelog')
@routes_bp.route('/license')
def index():
    return send_from_directory("app", "index.html")


@routes_bp.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('app', filename)


@routes_bp.route('/check-license')
def check_license():
    # license_path = Path.home().joinpath("Documents", "CrowdQuant", "license.ini")
    data = None
    license_path = get_file_path("license/license.ini")
    if license_path.exists():
        license_file = parse_ini_file(license_path)
        if license_file is None or 'license_key' in license_file is None:
            data = {"license_exists": False}
        else:
            license_key = license_file['license_key']
            if len(license_key) != 20:
                data = {"license_exists": False}
            else:
                app_name = "CrowdQuant"
                api_key = "f5b2c6d8174e93520ab9d6c48f12e3d7c9f"
                headers = {
                    'User-Agent': f'{app_name}-Application',
                    'Authorization': f'Bearer {api_key}'
                }
                try:
                    response = requests.get(
                        f'https://api.devdj.pl/app/license?check=desktop-app&license_key={license_key}&app={app_name}',
                        headers=headers, timeout=0.4)
                    response.raise_for_status()
                    api_data = response.json()
                    if api_data.success:
                        data = {"license_exists": True}
                    else:
                        data = {"license_exists": False}
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")
                    if license_key != "8lMy8BUDvLLo2luKkBrJ":
                        data = {"license_exists": False}
                    else:
                        data = {"license_exists": True}
    else:
        data = {"license_exists": False}

    return jsonify(data), 200


@routes_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'media[][]' not in request.files and 'media[]' not in request.files:
        print('No files uploaded')
        return 'No files uploaded', 400

    if 'media[][]' in request.files:
        files = request.files.getlist('media[][]')
        filename_without_extension = '.'.join(files[0].filename.split('.')[:-1])
        with open(os.path.join('data', 'temp', filename_without_extension), 'wb') as output_file:
            for part in files:
                output_file.write(part.read())

        print('Files uploaded and merged successfully!')
        return 'Files uploaded and merged successfully!', 200
    else:
        file = request.files.get('media[]')
        file.save(os.path.join('data', 'temp', file.filename))
        print('File uploaded successfully!')
        return 'File uploaded successfully!', 200


@routes_bp.route('/media/processed/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join('data', 'processed'), filename)


@routes_bp.route('/media/processed-image/output')
def processed_image():
    return send_from_directory("data/processed", "image.png")


def putFramesToFfmpegAndRecognite(media_source, process):
    cap = cv2.VideoCapture(os.path.normpath(app_root_dir().joinpath("data/temp", media_source)))
    model = YOLO(app_root_dir().joinpath("libs/models", "crowdquant-v3.pt"))
    classnames = ['person']
    if not cap.isOpened():
        print("Unable to open the video file.")
        return

    path_dict = {}
    track_id = 0
    color_dict = {}
    ret, prev_frame = cap.read()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        prev_frame = cv2.resize(prev_frame, (1280, 720))
        frame = cv2.resize(frame, (1280, 720))
        diff = np.abs(frame.astype(np.int32) - prev_frame.astype(np.int32))
        threshold = 30
        thresholded_diff = np.where(diff > threshold, 255, 0).astype(np.uint8)
        num_changed_pixels = np.sum(thresholded_diff)
        if num_changed_pixels > 1000:
            result = model(frame, stream=True)

            try:
                info = next(result)
            except StopIteration:
                info = None

            if info is not None:
                boxes = info.boxes
                for box in boxes:
                    confidence = box.conf[0]
                    confidence = math.ceil(confidence * 100)
                    Class = int(box.cls[0])
                    if confidence > 51:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        center_point = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                        if Class == 0:
                            found = False
                            for person_id, points in path_dict.items():
                                if len(points) > 0 and abs(center_point[0] - points[-1][0]) < 50 and abs(
                                        center_point[1] - points[-1][1]) < 50:
                                    path_dict[person_id].append(center_point)
                                    found = True
                                    track_id = person_id
                                    break

                            if not found:
                                track_id += 1
                                path_dict[track_id] = [center_point]

                            if track_id not in color_dict:
                                color_dict[track_id] = (
                                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                            for person_id, points in path_dict.items():
                                for j in range(1, len(points)):
                                    if points[j - 1] is not None and points[j] is not None:
                                        cv2.line(frame, points[j - 1], points[j], color_dict[person_id], 1)

            process.stdin.write(frame.tobytes())
            process.stdin.flush()

        prev_frame = frame

    cap.release()
    process.stdin.close()


def generateVideoStreamFromOutput(process):
    startTime = time.time()
    buffer = []
    sentBurst = False
    for chunk in iter(lambda: process.stdout.read(32568), b''):
        # We buffer everything before outputting it
        buffer.append(chunk)

        # Minimum buffer time, 3 seconds
        if sentBurst is False and time.time() > startTime + 3 and len(buffer) > 0:
            sentBurst = True
            for i in range(0, len(buffer) - 2):
                yield buffer.pop(0)

        elif time.time() > startTime + 3 and len(buffer) > 0:
            yield buffer.pop(0)

        process.poll()
        if isinstance(process.returncode, int):
            if process.returncode > 0:
                print('FFmpeg Error', process.returncode)

            break

    process.stdout.close()


@routes_bp.route('/media/processed-video/<media_source>/output')
def processed_video(media_source):
    if media_source is not None:
        source = os.path.normpath(app_root_dir().joinpath("data/temp", media_source))
        ffmpeg_command = [
            'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s:v', '1280x720', '-r', '30',
            '-i', '-', '-vf', 'setpts=2.5*PTS',  # Video Speed
            '-an',  # Soundtrack Off
            '-c:v', 'libvpx-vp9', '-g', '30', '-keyint_min', '30',
            '-b:v', '6M', '-minrate', '4M', '-maxrate', '12M', '-bufsize', '8M',
            '-crf', '0', '-deadline', 'realtime', '-tune', 'psnr', '-quality', 'good',
            '-tile-columns', '6', '-threads', '8', '-lag-in-frames', '16',
            '-f', 'webm', '-'
        ]
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=-1)
        ffmpeg_thread = threading.Thread(target=putFramesToFfmpegAndRecognite, args=(source, ffmpeg_process))
        ffmpeg_thread.start()
        
        return Response(stream_with_context(generateVideoStreamFromOutput(ffmpeg_process)), 200, mimetype='video/webm',
                        content_type="video/webm; codecs=vp9")