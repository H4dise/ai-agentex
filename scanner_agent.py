import cv2
import numpy as np
import warnings

class ScannerAgent:
    
    def process_sheet(self, image_path):
        """Custom tool: Process test sheet and extract answers"""
        print(f"Scanning {image_path}...")
 
        img = cv2.imread(image_path)
        if img is None:
            print("ERROR: Could not load image!")
            return {}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        """def mouse_callback(event, x, y, flags, param):
           if event == cv2.EVENT_LBUTTONDOWN:
               print(f"Coordinates: ({x}, {y})")
               # Draw a circle where you clicked
               cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
               cv2.imshow('Click on bubbles', img)
    
        cv2.imshow('Click on bubbles', img)
        cv2.setMouseCallback('Click on bubbles', mouse_callback)
        print("Click on each bubble position, then press any key to exit...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
        
    
        # Define bubble positions
        question_bubbles = {
    '1': {
        'A': (18, 7),    # Q1 A
        'B': (31,9),   # Q1 B
        'C': (40, 10),    # Q1 C  
        'D': (50, 9)    # Q1 D
    },
    '2': {
        'A': (20, 19),    # Q2 A
        'B': (31, 19),   # Q2 B
        'C': (40, 20),   # Q2 C
        'D': (50, 21)    # Q2 D
    },
    '3': {
        'A': (19 ,30),   # Q3 A
        'B': (32, 31),   # Q3 B
        'C': (41, 31),    # Q3 C 
        'D': (50, 31)    # Q3 D 
    } }
    
        answers = {}
        for question, bubbles in question_bubbles.items():
            answers[question] = self._detect_answer_for_question(gray, bubbles)
            
        return answers
    
    def _detect_answer_for_question(self, gray_img, bubble_positions):
        """Find which bubble is filled for a question"""
        for answer_letter, (x, y) in bubble_positions.items():
            if self._is_bubble_filled(gray_img, x, y):
                return answer_letter
        return "?"  # No bubble filled
    
    def _is_bubble_filled(self, gray_img, x, y):
        """Check if bubble at position is filled (dark)"""
        # Check a small area around the point for better accuracy
        if 0 <= y < gray_img.shape[0] and 0 <= x < gray_img.shape[1]:
            return gray_img[y, x] < 128  # Dark = filled
        return False