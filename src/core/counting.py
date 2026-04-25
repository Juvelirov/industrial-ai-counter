import torch
from typing import Dict, List, Set, Tuple
import numpy as np


class LineCrossCounter:
    def __init__(self, line_x_position: int):
        self.line_x = line_x_position
        self.counters: Dict[str, int] = {}
        self.passed_ids: Set[int] = set()
        self.last_positions: Dict[int, float] = {}

        self.NAMES_MAPPING = {
            "rezec_r50ec19": "Резец R50EC-19.5/20",
            "koronka_db41": "Коронка DB41.2507L",
        }

    def update(self, results) -> Tuple[Dict[str, int], List[Tuple[int, int]]]:
        """
        Обрабатывает результаты детекции.
        Возвращает:
        1. Словарь счетчиков {Название изделия: количество}
        2. Список координат центров объектов [(cx, cy), ...]
        """
        centers = []
        if results.boxes.id is None:
            return self.counters, centers

        boxes = results.boxes.xyxy.cpu().numpy()
        track_ids = results.boxes.id.cpu().numpy().astype(int)
        class_indices = results.boxes.cls.cpu().numpy().astype(int)
        names_dict = results.names

        for box, track_id, cls_idx in zip(boxes, track_ids, class_indices):
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            centers.append((int(center_x), int(center_y)))

            label = names_dict[cls_idx]

            label = self.NAMES_MAPPING.get(label, label)

            if track_id not in self.passed_ids:
                if track_id in self.last_positions:
                    prev_x = self.last_positions[track_id]
                    if (prev_x < self.line_x) != (center_x < self.line_x):
                        self.counters[label] = self.counters.get(label, 0) + 1
                        self.passed_ids.add(track_id)
                self.last_positions[track_id] = center_x

        return self.counters, centers