
import cv2
import numpy as np

class ScannerAgent:
    def process_sheet(self, image_path):
        """Custom tool: Process test sheet and extract answers"""
        print(f"Scanning {image_path}...")
 
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # Simple approach: Assume fixed bubble positions
        answers = {}
        answers['1'] = self._detect_bubble_at_position(gray, x=100, y=100)  # Position for Q1
        answers['2'] = self._detect_bubble_at_position(gray, x=100, y=150)  # Position for Q2
        answers['3'] = self._detect_bubble_at_position(gray, x=100, y=200)  # Position for Q3
    
        return answers

    def _detect_bubble_at_position(self, gray_img, x, y):
    # Check pixel darkness at bubble position
        if gray_img[y, x] < 128:  # Dark = filled
           return "A"
        else:
           return "B" 
    
    def _detect_answer_for_question(self, gray_img, question_num, bubble_positions):

        for answer_letter, (x, y) in bubble_positions.items():
             if gray_img[y, x] < 128:  # Dark pixel = filled
                return answer_letter
        return "?" 
