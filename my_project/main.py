# main.py - Should be 20-30 lines max!
from scanner_agent import ScannerAgent
from grading_agent import GradingAgent
from report_agent import ReportAgent
import logging

def main():
    scanner = ScannerAgent()
    grader = GradingAgent() 
    reporter = ReportAgent()
    
    image = "test_sheet.jpg"
    answers = scanner.process_sheet(image)
    print(answers)  # {"1": "A", "2": "B", "3": "C"}
    #score = grader.grade_test(answers) 
    #report = reporter.make_report(score)
    
    #print("GRADING COMPLETE!")
    #print(report)

if __name__ == "__main__":
    main()