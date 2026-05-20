import cv2
import numpy as np


def analyze_video(video_path):

    # ==========================================
    # OUTPUT DICTIONARY
    # ==========================================

    result = {

        "top_wall_hits": 0,
        "bottom_wall_hits": 0,
        "left_wall_hits": 0,
        "right_wall_hits": 0

    }

    # ==========================================
    # OPEN VIDEO
    # ==========================================

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print("Error opening video")
        return result

    # ==========================================
    # GREEN COLOR RANGE (HSV)
    # ==========================================

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # ==========================================
    # FRAME DIMENSIONS
    # ==========================================

    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ==========================================
    # COLLISION FLAGS
    # ==========================================

    left_collision = False
    right_collision = False

    top_collision = False
    bottom_collision = False

    # ==========================================
    # WALL THRESHOLD
    # ==========================================

    wall_threshold = 50

    # ==========================================
    # PROCESS VIDEO
    # ==========================================

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # ==========================================
        # CONVERT FRAME TO HSV
        # ==========================================

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # ==========================================
        # CREATE GREEN MASK
        # ==========================================

        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        # ==========================================
        # REMOVE NOISE
        # ==========================================

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ==========================================
        # FIND CONTOURS
        # ==========================================

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # ==========================================
        # WRITE YOUR LOGIC BELOW
        # ==========================================

        if len(contours) > 0:

            # Find largest contour

            largest_contour = max(
                contours,
                key=cv2.contourArea
            )

            # Ignore small contours

            area = cv2.contourArea(
                largest_contour
            )

            if area > 100:

                # Bounding rectangle

                x, y, w, h = cv2.boundingRect(
                    largest_contour
                )

                if x <= wall_threshold:

                    if not left_collision:

                        result["left_wall_hits"] += 1

                        left_collision = True

                elif x > wall_threshold + 15:

                    left_collision = False

                if x + w >= WIDTH - wall_threshold:

                    if not right_collision:

                        result["right_wall_hits"] += 1

                        right_collision = True

                elif x + w < WIDTH - wall_threshold - 15:

                    right_collision = False

                if y <= wall_threshold:

                    if not top_collision:

                        result["top_wall_hits"] += 1

                        top_collision = True

                elif y > wall_threshold + 15:

                    top_collision = False

                if y + h >= HEIGHT - wall_threshold:

                    if not bottom_collision:

                        result["bottom_wall_hits"] += 1

                        bottom_collision = True

                elif y + h < HEIGHT - wall_threshold - 15:

                    bottom_collision = False

    # ==========================================
    # RELEASE VIDEO
    # ==========================================

    cap.release()

    return result
