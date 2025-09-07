import argparse
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

from object_detector import ObjectDetector

# --- CLI ---
def parse_args():
    p = argparse.ArgumentParser(description="Color Spotter (OpenCV, HSV)")
    p.add_argument("--color", type=str, default="pink",
                   help="Named BGR color key: yellow, blue, red, green, orange, purple, pink, brown, black")
    p.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    p.add_argument("--min-area", type=int, default=300, help="Minimum contour area to draw a bbox")
    p.add_argument("--show-mask", action="store_true", help="Show thresholded mask window")
    p.add_argument("--save", type=str, default=None, help="Optional output video path (mp4)")
    return p.parse_args()

# --- Predefined BGR colors (your original mapping) ---
BGR_COLORS = {
    "yellow": (0, 255, 255),
    "blue":   (255, 0, 0),
    "red":    (0, 0, 255),
    "green":  (0, 255, 0),
    "orange": (0, 165, 255),
    "purple": (128, 0, 128),
    "pink":   (147, 20, 255),
    "brown":  (42, 42, 165),
    "black":  (0, 0, 0),
}

def open_writer(save_path, w, h, fps=30.0):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(save_path, fourcc, fps, (w, h))

def main():
    args = parse_args()
    if args.color not in BGR_COLORS:
        raise SystemExit(f"Unknown color '{args.color}'. Available: {', '.join(BGR_COLORS.keys())}")

    # Webcam
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    # Detector
    obj_detector = ObjectDetector()

    # HSV bounds from named BGR
    lower_list, upper_list = obj_detector.get_bound_box_by_color(BGR_COLORS[args.color])
    lower, upper = lower_list[0], upper_list[0]

    writer = None
    win_name = "color-spotter"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    # Warm-up read for writer size if saving
    if args.save:
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("No frame from camera")
        h, w = frame.shape[:2]
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        writer = open_writer(args.save, w, h)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lower, upper)

        # Optional: simple morphology to clean noise (comment out if undesired)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)

        # Find bbox via PIL (as in your original code)
        bbox = Image.fromarray(mask).getbbox()
        if bbox:
            x1, y1, x2, y2 = bbox
            area = (x2 - x1) * (y2 - y1)
            if area >= args["min_area"] if isinstance(args, dict) else args.min_area:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cx, cy = x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2
                cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                cv2.putText(frame, f"area={area}", (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        cv2.imshow(win_name, frame)
        if args.show_mask:
            cv2.imshow("mask", mask)

        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q")):
            break

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
