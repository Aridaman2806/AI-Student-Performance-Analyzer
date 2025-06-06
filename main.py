import os
import sys
from dotenv import load_dotenv
from src.feedback_generator import generate_feedback
from src.pdf_generator import create_pdf
from src.data_processor import DataProcessor
import matplotlib.pyplot as plt
import pandas as pd

def create_performance_charts(data, output_dir):
    """Create performance visualization charts."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Subject-wise Performance Chart
    subjects = list(data['subject_wise'].keys())
    accuracies = [data['subject_wise'][subject]['accuracy'] for subject in subjects]
    
    plt.figure(figsize=(10, 6))
    plt.bar(subjects, accuracies)
    plt.title('Subject-wise Performance')
    plt.xlabel('Subjects')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    for i, v in enumerate(accuracies):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'subject_performance.png'))
    plt.close()
    
    # 2. Section-wise Performance Chart
    sections = []
    correct = []
    total = []
    
    for section, analysis in data['section_wise'].items():
        sections.append(section)
        correct.append(analysis['correct_answers'])
        total.append(analysis['total_questions'])
    
    plt.figure(figsize=(12, 6))
    x = range(len(sections))
    width = 0.35
    
    plt.bar(x, total, width, label='Total Questions', color='lightgray')
    plt.bar(x, correct, width, label='Correct Answers', color='green')
    
    plt.title('Section-wise Performance')
    plt.xlabel('Sections')
    plt.ylabel('Number of Questions')
    plt.xticks(x, sections, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'section_performance.png'))
    plt.close()
    
    return [
        os.path.join(output_dir, 'subject_performance.png'),
        os.path.join(output_dir, 'section_performance.png')
    ]

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        print("Error: GOOGLE_API_KEY not found!")
        print("\nPlease do ONE of the following:")
        print("\n1. Create a .env file in the project root with:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        print("\n2. OR set it directly in your command prompt:")
        print("   set GOOGLE_API_KEY=your_api_key_here")
        print("\nYou can get an API key from https://ai.google.dev/")
        sys.exit(1)
    
    # Initialize data processor with API key
    processor = DataProcessor('data/sample_submission_analysis_1.json', API_KEY)
    
    # Process data and get LLM prompt
    data = processor.process_data()
    prompt = processor.get_llm_prompt()
    
    # Generate feedback using the LLM
    feedback = generate_feedback(prompt, API_KEY)
    
    # Create performance charts
    chart_paths = create_performance_charts(data, 'output')
    
    # Generate PDF report
    create_pdf(feedback, chart_paths, 'output/report.pdf')
    
    print("Report generated successfully!")

if __name__ == "__main__":
    main()
