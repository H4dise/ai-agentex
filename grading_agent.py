class GradingAgent:
    def grade_test(self, student_answers):
        """Custom tool: Grade student answers against answer key"""
        print("Grading test...")
        
        # Answer key database
        answer_key = {
            '1': 'D',  # Correct answer for Q1
            '2': 'B',  # Correct answer for Q2  
            '3': 'C'   # Correct answer for Q3
        }
        score = 0
        results = {}
        
        for question, student_answer in student_answers.items():
            correct_answer = answer_key.get(question, '?')
        
        
            if student_answer == '?':
                is_correct = None  

            elif student_answer == correct_answer:
              score += 1
              is_correct = True

            else:
               is_correct = False
            
        results[question] = {
            'student_answer': student_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct  # True/False/None
        }
       
        total_answered = len(answer_key)
        percentage = (score /  total_answered) * 100 if  total_answered > 0 else 0
        
        return {
            'score': score,
            'total_questions':  total_answered,
            'total_questions': len(answer_key),
            'percentage': percentage,
            'results': results
        }