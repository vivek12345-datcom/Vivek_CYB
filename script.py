#!/usr/bin/env python3
import cv2
import numpy as np


def analyze_arena(input_image):

    # ==========================================
    # LOAD IMAGE
    # ==========================================

    image = cv2.imread(input_image)

    if image is None:

        print("Error loading image.")
        return {}

    # ==========================================
    # INITIALIZE OUTPUT
    # ==========================================

    result = {

        "arena_size": None,
        "start": None,
        "goal": None,
        "special_cells": {}

    }

    # ==========================================
    # WRITE YOUR LOGIC BELOW
    # ==========================================

    def detect_cell_type(hsv_roi):

        # ---------------- RED ----------------
        red_lower1 = np.array([0, 120, 70])
        red_upper1 = np.array([10, 255, 255])

        red_lower2 = np.array([170, 120, 70])
        red_upper2 = np.array([180, 255, 255])

        # ---------------- GREEN ----------------
        green_lower = np.array([35, 50, 50])
        green_upper = np.array([85, 255, 255])

        # ---------------- BLUE ----------------
        blue_lower = np.array([95, 100, 50])
        blue_upper = np.array([140, 255, 255])

        # ---------------- ORANGE ----------------
        orange_lower = np.array([10, 100, 100])
        orange_upper = np.array([25, 255, 255])

        # ---------------- YELLOW ----------------
        yellow_lower = np.array([20, 120, 120])
        yellow_upper = np.array([35, 255, 255])

        # ---------------- CYAN ----------------
        cyan_lower = np.array([75, 100, 100])
        cyan_upper = np.array([100, 255, 255])

        masks = {

            "DANGER":
                cv2.inRange(hsv_roi, red_lower1, red_upper1) +
                cv2.inRange(hsv_roi, red_lower2, red_upper2),

            "SAFE":
                cv2.inRange(hsv_roi, green_lower, green_upper),

            "REFUEL":
                cv2.inRange(hsv_roi, blue_lower, blue_upper),

            "SLOW":
                cv2.inRange(hsv_roi, orange_lower, orange_upper),

            "START":
                cv2.inRange(hsv_roi, yellow_lower, yellow_upper),

            "GOAL":
                cv2.inRange(hsv_roi, cyan_lower, cyan_upper)
        }

        counts = {}

        for key in masks:
            counts[key] = cv2.countNonZero(masks[key])

        detected = max(counts, key=counts.get)

        if counts[detected] < 40:
            return None

        return detected

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    best_contour = None
    best_area = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 10000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        aspect_ratio = w / float(h)

        if 0.9 <= aspect_ratio <= 1.1:

            if area > best_area:
                best_area = area
                best_contour = cnt

    if best_contour is None:

        print("Arena not found")
        return result

    x, y, w, h = cv2.boundingRect(best_contour)

    arena = image[y:y+h, x:x+w]

    gray_arena = cv2.cvtColor(arena, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_arena, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=100,
        minLineLength=w // 2,
        maxLineGap=10
    )

    vertical_lines = []
    horizontal_lines = []

    if lines is not None:

        for line in lines:

            x1, y1, x2, y2 = line[0]

            if abs(x1 - x2) < 5:
                vertical_lines.append(x1)

            if abs(y1 - y2) < 5:
                horizontal_lines.append(y1)

    def unique_lines(lines_list):

        lines_list = sorted(lines_list)

        unique = []

        for val in lines_list:

            if len(unique) == 0 or abs(val - unique[-1]) > 15:
                unique.append(val)

        return unique

    vertical_lines = unique_lines(vertical_lines)
    horizontal_lines = unique_lines(horizontal_lines)

    n = min(len(vertical_lines), len(horizontal_lines)) - 1

    result["arena_size"] = n

    cell_w = w / n
    cell_h = h / n

    for i in range(n):

        for j in range(n):

            x1 = int(j * cell_w)
            x2 = int((j + 1) * cell_w)

            y1 = int(i * cell_h)
            y2 = int((i + 1) * cell_h)

            cell = arena[y1:y2, x1:x2]

            if cell.size == 0:
                continue

            ch, cw = cell.shape[:2]

            cx1 = int(cw * 0.25)
            cx2 = int(cw * 0.75)

            cy1 = int(ch * 0.25)
            cy2 = int(ch * 0.75)

            center = cell[cy1:cy2, cx1:cx2]

            hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)

            detected = detect_cell_type(hsv)

            if detected is None:
                continue

            col = chr(ord('A') + j)

            row = n - i

            coord = f"{col}{row}"

            if detected == "START":

                result["start"] = coord

            elif detected == "GOAL":

                result["goal"] = coord

            else:

                result["special_cells"][coord] = detected

    # ==========================================
    # SORT SPECIAL CELLS
    # ==========================================

    sorted_cells = dict(

        sorted(

            result["special_cells"].items(),

            key=lambda item: (

                item[0][0],
                int(item[0][1:])

            )
        )
    )

    result["special_cells"] = sorted_cells

    # ==========================================
    # RETURN FINAL OUTPUT
    # ==========================================

    return result
