class ReportAgent:
    def make_report(self, grading_results):
        """Custom tool: Generate comprehensive score report with analytics"""
        print("Generating detailed report...")
        
        # Calculate analytics
        total_correct = grading_results['score']
        total_answered = grading_results['total_answered']
        total_questions = grading_results['total_questions']
        percentage = grading_results['percentage']
        
        # Find difficult questions (wrong answers)
        difficult_questions = []
        for question, result in grading_results['results'].items():
            if result['is_correct'] == False:  # Only wrong answers
                difficult_questions.append(question)
        
        report = f"""
📊 COMPREHENSIVE TEST ANALYSIS REPORT
====================================

📈 SCORE SUMMARY:
• Correct Answers: {total_correct}/{total_answered}
• Percentage: {percentage:.1f}%
• Total Questions: {total_questions}
• Questions Attempted: {total_answered}

🔍 DETAILED BREAKDOWN:
"""
        
        for question, result in grading_results['results'].items():
            if result['is_correct']:
                status = "✅ CORRECT"
            elif result['is_correct'] is False:
                status = "❌ INCORRECT" 
            else:
                status = "⏸️  NOT ATTEMPTED"
                
            report += f"Q{question}: Student: {result['student_answer']} | Correct: {result['correct_answer']} - {status}\n"

        # Analytics Section
        report += f"""
📊 PERFORMANCE ANALYTICS:
• Accuracy Rate: {percentage:.1f}%
• Difficult Questions: {', '.join(difficult_questions) if difficult_questions else 'None'}
• Questions Attempted: {total_answered}/{total_questions} ({(total_answered/total_questions)*100:.1f}%)
• Mastery Level: {'Excellent' if percentage >= 80 else 'Good' if percentage >= 60 else 'Needs Improvement'}
"""

        report += "\n====================================\n"
        return report