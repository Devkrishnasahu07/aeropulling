import cv2
import numpy as np
from PIL import Image

def analyze_luggage(uploaded_file):
    """
    Analyzes an uploaded image or camera capture and returns
    luggage size (Light/Medium/Heavy), estimated units (1-3), and surcharge fee.
    """
    try:
        # Convert image to OpenCV format
        image = Image.open(uploaded_file)
        img_array = np.array(image.convert("RGB"))
        h, w, _ = img_array.shape
        
        # Grayscale and edge detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours to estimate bag area
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        total_bag_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > (w * h * 0.01):  # Filter out minor noise
                total_bag_area += area
                
        area_ratio = (total_bag_area / (w * h)) * 100
        
        # Classification thresholds
        if area_ratio > 25.0:
            return "Heavy", 3, 80.0
        elif area_ratio > 10.0:
            return "Medium", 2, 40.0
        else:
            return "Light", 1, 0.0
            
    except Exception:
        # Safe fallback
        return "Medium", 2, 40.0