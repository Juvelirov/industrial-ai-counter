import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Visualizer:
    @staticmethod
    def put_russian_text_with_outline(img, text, position, font_size=30, color=(0, 0, 255),
                                      outline_color=(0, 0, 0), outline_width=2):
        # Конвертация BGR в RGB для PIL
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        draw = ImageDraw.Draw(pil_img)

        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        x, y = position
        # Контур
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color[::-1])

        draw.text(position, text, font=font, fill=color[::-1])
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    @staticmethod
    def put_text_with_outline(img, text, position, font_scale=0.7, color=(0, 255, 255),
                              outline_color=(0, 0, 0), thickness=2):
        x, y = position
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, outline_color, thickness + 2)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        return img

    @staticmethod
    def draw_overlay_logic(frame, line_x):
        """Заливка зоны контроля."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (line_x, h), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        cv2.rectangle(frame, (0, 0), (line_x, h), (0, 0, 255), 3)
        cv2.line(frame, (line_x, 0), (line_x, h), (0, 0, 255), 2)
        return frame

    @staticmethod
    def draw_points(frame, centers):
        """Рисование центральных точек объектов."""
        for cx, cy in centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
        return frame

    @staticmethod
    def draw_statistics(frame, counts, fps: int):
        """Рисование FPS и счетчиков."""
        Visualizer.put_text_with_outline(frame, f"FPS: {fps}", (frame.shape[1] - 150, 40))

        y_off = 40
        for label, count in counts.items():
            Visualizer.put_text_with_outline(frame, f"{label}: {count}", (20, y_off), color=(139, 0, 0))
            y_off += 30
        return frame