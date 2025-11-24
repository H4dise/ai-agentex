import cv2
import numpy as np
import warnings

class ScannerAgent:
    
    # ----------------------------------------------------
    # متدهای کمکی CV (خارج از process_sheet)
    # ----------------------------------------------------
    def _order_points(self, pts):
        """
        مرتب‌سازی ۴ نقطه گوشه بر اساس ترتیب استاندارد: (بالا چپ، بالا راست، پایین راست، پایین چپ)
        """
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect
    
    def _find_all_bubbles_dynamically(self, thresh_img):
        """
        [جدید] تشخیص پویا (Dynamic Detection): یافتن مختصات حباب‌ها بدون نیاز به مختصات ثابت.
        فرض: هر سطر باید 4 حباب داشته باشد.
        """

        """
        [بهبود یافته] تشخیص پویا: یافتن مختصات حباب‌ها با فیلتر ضریب گردی.
        فرض: هر سطر باید 4 حباب داشته باشد.
        """
        # --- پارامترهای حیاتی (نیاز به تنظیم دقیق توسط شما) ---
        min_area = 10    # حداقل مساحت حباب (اغلب نیاز به کاهش دارد)
        max_area = 1700  # حداکثر مساحت حباب (بسیار افزایش یافته)
        CIRCULARITY_THRESHOLD = 0.65 # حداقل ضریب گردی (باید بین 0 تا 1 باشد. 1 = دایره کامل)
        row_threshold = 10 # فاصله Y مجاز برای قرارگیری در یک سطر
        # ---------------------------------------------------------------------

        # ۱. پیدا کردن کانتورها (حباب‌ها)
        contours, _ = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bubble_list = []
        
        for c in contours:
            area = cv2.contourArea(c)
            
            # فیلتر ۱: فیلتر کردن بر اساس مساحت
            if min_area < area < max_area:
                
                # فیلتر ۲: محاسبه ضریب گردی (Circularity)
                perimeter = cv2.arcLength(c, True)
                if perimeter == 0:
                    continue # جلوگیری از تقسیم بر صفر

                # ضریب گردی: هرچه به ۱ نزدیک‌تر، شکل دایره‌ای‌تر است.
                # (4 * PI * Area) / (Perimeter^2)
                circularity = (4 * np.pi * area) / (perimeter ** 2)
                
                if circularity > CIRCULARITY_THRESHOLD:
                    # استفاده از مرکز محاصره شده (Enclosing Circle Center)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    
                    # فیلتر ۳ (اختیاری): فیلتر کردن بر اساس شعاع برای حذف نویزهای بزرگ
                    if radius < 35: 
                        bubble_list.append((int(x), int(y)))
                    
        if not bubble_list:
            warnings.warn("No bubbles were detected dynamically. Check image contrast and area settings.")
            return {}
        bubble_list.sort(key=lambda item: item[1]) # مرتب‌سازی اولیه بر اساس Y
        questions = []
        current_row = []
        row_threshold = 15 # فاصله Y مجاز برای قرارگیری در یک سطر
        
        if bubble_list:
            current_row.append(bubble_list[0])
            for i in range(1, len(bubble_list)):
                # اگر حباب بعدی در فاصله Y مجاز باشد، به همین سطر اضافه می‌شود
                if abs(bubble_list[i][1] - current_row[-1][1]) < row_threshold:
                    current_row.append(bubble_list[i])
                else:
                    questions.append(current_row) # سطر قبل را ثبت کن
                    current_row = [bubble_list[i]] # سطر جدید را شروع کن
            questions.append(current_row) # ثبت آخرین سطر

        # ۳. پردازش نهایی گروه‌ها (ساخت دیکشنری خروجی)
        final_bubbles = {}
        option_letters = ['A', 'B', 'C', 'D']
        
        for q_index, row in enumerate(questions, 1):
            # مرتب‌سازی بر اساس X (از چپ به راست: A, B, C, D)
            row.sort(key=lambda item: item[0])
            
            # فرض بر 4 گزینه بودن
            if len(row) >= 4:
                final_bubbles[str(q_index)] = {}
                for opt_index in range(4): 
                    # فقط 4 گزینه اول را در نظر می‌گیریم
                    final_bubbles[str(q_index)][option_letters[opt_index]] = row[opt_index]
            else:
                warnings.warn(f"Skipping question {q_index}: found {len(row)} bubbles, expected 4.")

        return final_bubbles

    # ----------------------------------------------------
    # متد اصلی process_sheet
    # ----------------------------------------------------
    def process_sheet(self, image_path):
        """Custom tool: Process test sheet and extract answers automatically with Dynamic Detection."""
        print(f"Scanning {image_path}...")
 
        img = cv2.imread(image_path)
        if img is None:
            print("ERROR: Could not load image!")
            return {}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
                
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        doc_contour = None
        if contours:
             contours = sorted(contours, key=cv2.contourArea, reverse=True)
             for c in contours:
                 peri = cv2.arcLength(c, True)
                 approx = cv2.approxPolyDP(c, 0.04 * peri, True) 
                 if len(approx) == 4:
                    doc_contour = approx
                    break
        
        # --- اعمال تصحیح پرسپکتیو ---
        if doc_contour is not None:
            points = doc_contour.reshape(4, 2)
            rect = self._order_points(points) 
    
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
    
            dst = np.array([
                  [0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
     
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(gray, M, (maxWidth, maxHeight))
        else:
          warnings.warn("Could not find the document contour, processing original image without correction.")
          warped = gray
          
        # --- آستانه‌گیری تطبیقی برای تشخیص دقیق ---
        thresh = cv2.adaptiveThreshold(warped, 255, 
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 
                                       11, 4) 
        
        # =================================================================
        # جایگزینی مختصات ثابت با تشخیص پویا
        # =================================================================
        question_bubbles = self._find_all_bubbles_dynamically(thresh)

        answers = {}
        for question, bubbles in question_bubbles.items():
            # استفاده از تصویر "thresh" برای تشخیص پاسخ
            answers[question] = self._detect_answer_for_question(thresh, bubbles)
            
        return answers
    
    # ----------------------------------------------------
    # متدهای تشخیص (برای نمونه‌برداری ناحیه‌ای و تصویر باینری)
    # ----------------------------------------------------
    def _detect_answer_for_question(self, binary_img, bubble_positions):
        """Find which bubble is filled for a question using the binary image."""
        for answer_letter, (x, y) in bubble_positions.items():
            if self._is_bubble_filled(binary_img, x, y): 
                return answer_letter
        return "?"
    
    def _is_bubble_filled(self, binary_img, x, y):
        """Check if bubble at position is filled (dark) by sampling a region."""
        sample_size = 5 
        x1, y1 = x - sample_size, y - sample_size
        x2, y2 = x + sample_size, y + sample_size

        if 0 <= y1 < y2 < binary_img.shape[0] and 0 <= x1 < x2 < binary_img.shape[1]:
            roi = binary_img[y1:y2, x1:x2]
            mean_intensity = np.mean(roi)
            # در تصویر سیاه و سفید مطلق، مقدار کمتر از ۱۲۸ یعنی تیره (پر شده) است.
            return mean_intensity < 128
        
        return False