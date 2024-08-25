import math
import os.path
import random
from collections import Counter
import cv2
import pandas as pd
from ultralytics import YOLO

from utils.app_root_dir import app_root_dir
from utils.get_file_path import get_file_path


class Recognition:
    def __init__(self, media_source=None):
        self.media_source = media_source
        self.model = YOLO(get_file_path("libs/models/crowdquant-v2.pt"))
        self.classnames = ['person']
        self.confidence = 51

        self.ffmpeg_thread = None
        self.stop_ffmpeg = False

    def Image(self):
        try:
            img = cv2.imread(os.path.normpath(app_root_dir().joinpath("data/temp", self.media_source)))
            img = cv2.resize(img, (1280, 720))

            results = self.model.predict(img)
            a = results[0].boxes.cpu().data
            px = pd.DataFrame(a).astype("float")
            object_classes = []

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                confidence = math.ceil(row[4] * 100)  # confidence w %
                if confidence > self.confidence:
                    obj_class = self.classnames[d]
                    object_classes.append(obj_class)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            person_count = len([obj for obj in object_classes if obj == 'person'])
            counter = Counter(object_classes)
            for obj, count in counter.items():
                print(f"{obj}: {count}")

            #cv2.putText(img, f'Liczba osob: {person_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            file_extension = os.path.splitext(self.media_source)[1]
            processed_image_path = os.path.normpath(app_root_dir().joinpath("data/processed/image.png"))
            cv2.imwrite(processed_image_path, img,
                        [cv2.IMWRITE_JPEG_QUALITY, 95] if file_extension.lower() in ['.jpg', '.jpeg'] else [])

            cv2.destroyAllWindows()

        except Exception as e:
            print("Image processing error:", e)

    def Live(self):
        try:
            cap = cv2.VideoCapture(self.media_source)
            if not cap.isOpened():
                print(f"Unable to connect to the address: {self.media_source}")
                return

            path_dict = {}
            track_id = 0
            color_dict = {}
            detected_people = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (1280, 750))
                result = self.model(frame, stream=True)

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
                        if confidence > self.confidence:
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

                cv2.imshow('Live RTSP', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print("An error occurred while processing RTSP:", e)

    def Camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Failed to start the camera.")
                return

            path_dict = {}
            track_id = 0
            color_dict = {}
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (1280, 720))
                result = self.model(frame, stream=True)

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
                        if confidence > self.confidence:
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

                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print("An error occurred while processing the camera:", e)