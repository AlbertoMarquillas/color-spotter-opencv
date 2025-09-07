import numpy as np # Import numpy library
import cv2 # Import OpenCV library
from PIL import Image # Import Image class from PIL library

from object_detector import ObjectDetector # Import the ObjectDetector class from object_detector.py

# Load the webcam
cap = cv2.VideoCapture(0)

# create an object of the class ObjectDetector
obj_detector = ObjectDetector()

    
#dictionary to store the colors in bgr
colors = {
    'yellow': (0, 255, 255),
    'blue': (255, 0, 0),
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'orange': (0, 165, 255),
    'purple': (128, 0, 128),
    'pink': (147, 20, 255),
    'brown': (42, 42, 165),
    'black': (0, 0, 0),
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # We are working in HSV color space (Hue, Saturation, Value)
    
    # Hue: This channel encodes color information. Hue can be thought of an angle where 0 degree corresponds to the red color, 
    # 120 degrees corresponds to the green color, and 240 degrees corresponds to the blue color.
    # Saturation: Saturation is the amount of color (depth of the pigment). For example, pink is less saturated than red.
    # Value: Value works in conjunction with saturation and describes the brightness or intensity of the color.
    
    # Define regions for detecting colors
    # yellow intervals: [20, 100, 100] - [30, 255, 255]
    # blue intervals: [110, 100, 100] - [130, 255, 255]
    # red intervals: [0, 100, 100] - [10, 255, 255]
    
    
    # Convert the frame to HSV
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get a mask for the pink color 
    
    #get the bounds for the pink color
    pink_lower_bound, pink_upper_bound = obj_detector.get_bound_box_by_color(colors['pink'])


    # Create a mask for the pink color
    pink_mask = cv2.inRange(hsv_img, pink_lower_bound[0], pink_upper_bound[0])
    
    # Draw bounding box around the detected object
    mask_img = Image.fromarray(pink_mask) # Convert the mask from a numpy array to an Image object
    
    # Get the bounding box
    bbox = mask_img.getbbox()
    
    print('Bounding Box:', bbox)    
    
    if bbox:
        # Draw the bounding box
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #Show the frame
    cv2.imshow('frame', frame)

    # Convert the frame to BGR
    if cv2.waitKey(1) == ord('q'):
        break
    
# Release the webcam
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()

