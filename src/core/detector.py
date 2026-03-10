import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results

class ObjectDetector:
    def __init__(self, model_path: str, conf_threshold: float = 0.2):
        self.model = YOLO(model_path)
        self.conf = conf_threshold

    def get_tracks(self, frame) -> Results:
        results = self.model.track(
            frame,
            persist = True,
            tracker = "bytetrack.yaml",
            conf= self.conf,
            verbose =False
        )
        return results[0]