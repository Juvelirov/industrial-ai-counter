import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Visualizer:

    @staticmethod
    def put_text_with_outline(img, text, position, font_scale=0.7, color=(139, 69, 19),
                              outline_color=(0, 0, 0), thickness=2):
        x, y = position
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, outline_color, thickness + 2)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        return img

    @staticmethod
    def draw_overlay_logic(frame, line_x):
        h, w = frame.shape[:2]

        # Полупрозначная синяя зона контроля
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (line_x, h), (139, 69, 19), -1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)

        # Рамка зоны контроля
        cv2.rectangle(frame, (0, 0), (line_x, h), (139, 69, 19), 3)

        # Активная линия подсчета
        cv2.line(frame, (line_x, 0), (line_x, h), (139, 69, 19), 2)

        return frame

    @staticmethod
    def draw_points(frame, centers):
        """Рисование центральных точек объектов."""
        for cx, cy in centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
        return frame



    @staticmethod
    def put_russian_text_with_outline(img, text, position, line_x, font_size=30, color=(0, 0, 255),
                                      outline_color=(0, 0, 0), outline_width=2):
        # Конвертация BGR в RGB для PIL
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        draw = ImageDraw.Draw(pil_img)

        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        header_y = 20

        # Выравнивание внутри шапки
        text_x = (line_x - text_w) // 2
        text_y = header_y  # отступ внутри шапки

        # Параметры шапки
        padding = 10

        # Координаты прямоугольника фона "Зоны контроля"
        rect_left = text_x - padding
        rect_top = header_y
        rect_right = text_x + text_w + padding
        rect_bottom = header_y + text_h + padding * 2 - 10

        # Шапка
        draw.rectangle(
            [(rect_left, rect_top), (rect_right, rect_bottom)],
            fill=(26, 76, 122)
        )

        # Нижняя граница шапки
        draw.rectangle(
            [(rect_left, rect_top), (rect_right, rect_bottom)],
            outline=(0, 0, 0),
            width=outline_width
        )

        # Обводка текста
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((text_x + dx, text_y + dy), text, font=font, fill=(0, 0, 0))

        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

        # Линия под шапкой
        line_y = rect_bottom + 5
        draw.line([(0, line_y), (line_x, line_y)], fill=(26, 76, 122), width=outline_width + 2)

        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)