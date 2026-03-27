import torch
import cv2
import time
import numpy as np
from src.core.detector import ObjectDetector
from src.core.counting import LineCrossCounter
from src.core.ui_utils import Visualizer


class MonitoringEngine:
    def __init__(self, config: dict):
        # Загрузка настроек из конфига линии
        self.video_source = config['video']['source']
        self.target_width = config.get('video', {}).get('target_width', 1280)
        self.line_x = config['analytics']['line_x']

        self.detector = ObjectDetector(config['model']['path'])
        self.counter = LineCrossCounter(self.line_x)
        self.vis = Visualizer()

        self.is_running = False

    def start(self):
        """Основной цикл обработки"""
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print(f"Ошибка: не удалось открыть источник {self.video_source}")
            return

        self.is_running = True
        print("Движок запущен")

        while cap.isOpened() and self.is_running:
            start_time = time.time()
            success, frame = cap.read()
            if not success:
                break

            # Предобработка кадра
            h, w = frame.shape[:2]
            target_h = int(self.target_width * (h / w))
            frame = cv2.resize(frame, (self.target_width, target_h))

            # Детекция и трекинг
            results = self.detector.get_tracks(frame)

            # Логика подсчета и получение центров объектов
            counts, centers = self.counter.update(results)

            # Отрисовка слоёв
            frame = self._draw_frame(frame, results, counts, centers, start_time)

            # Вывод кадра
            cv2.imshow("KZTS Monitoring Engine", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break

        cap.release()
        cv2.destroyAllWindows()

    def _draw_frame(self, frame, results, counts, centers, fps_value):
        """Сборка кадра (рамка + линия + зона контроля + fps)"""
        # Рамка
        frame = results.plot(img=frame, line_width=1)
        # Линия и зона контроля
        frame = self.vis.draw_overlay_logic(frame, self.line_x)
        frame = self.vis.draw_points(frame, centers)
        frame = self.vis.draw_statistics(frame, counts, fps_value)
        frame = self.vis.put_russian_text_with_outline(
            frame, "ЗОНА КОНТРОЛЯ", (self.line_x // 2 - 100, frame.shape[0] - 50)
        )

        return frame

    def stop(self):
        """Остановка цикла"""
        self.is_running = False
        print("Движок остановлен")