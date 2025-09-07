import cv2
import numpy as np

class ObjectDetector:
    def get_bound_box_by_color(self, color):
        # Convert the color from BGR to HSV
        c = np.uint8([[color]])
        hsv_color = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

        # Get the HSV values
        hue = hsv_color[0][0][0]  # Hue value

        # Define the lower and upper bounds for other colors
        lower_bound = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_bound = np.array([hue + 10, 255, 255], dtype=np.uint8)

        # Return the lower and upper bounds
        return [lower_bound], [upper_bound]
