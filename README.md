# Student Performance Analysis System

An AI-powered system that analyzes student test performance and generates detailed feedback reports using Google's Gemini AI model.

## Features

- Analyzes student test data from JSON format
- Generates comprehensive performance reports
- Creates visual performance charts
- Provides AI-powered insights and recommendations
- Generates PDF reports with detailed analysis

## APIs and Models Used

### Google Gemini AI
- **Model**: `gemini-2.0-flash`
- **Purpose**: 
  - Initial data analysis and pattern recognition
  - Generating structured feedback
  - Providing actionable recommendations
- **Key Features Used**:
  - JSON response formatting
  - Structured data analysis
  - Natural language generation

### Data Processing APIs
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Performance visualization
- **ReportLab**: PDF report generation
- **BeautifulSoup4**: HTML parsing for syllabus data

## Prompt Logic

### 1. Data Analysis Prompt
```python
{
    "strengths": [],        # 2-3 key strengths
    "improvements": [],     # 2-3 areas for improvement
    "time_management": [],  # 2-3 time management insights
    "recommendations": []   # 3-4 specific recommendations
}
```

### 2. Feedback Generation Prompt Structure
1. **Test Overview**
   - Total duration
   - Total questions
   - Total marks

2. **Overall Performance**
   - Time taken
   - Marks scored
   - Questions attempted
   - Accuracy

3. **Subject-wise Analysis**
   - Performance metrics per subject
   - Time management
   - Accuracy patterns

4. **Section-wise Analysis**
   - Question-level performance
   - Difficulty-wise breakdown
   - Chapter-wise analysis
   - Topic-wise analysis

5. **AI Analysis**
   - Strengths
   - Areas for improvement
   - Time management insights
   - Specific recommendations

## Report Structure

### 1. PDF Report Components
- **Title Page**
  - Student Performance Report
  - Date and Time

- **Executive Summary**
  - Overall performance score
  - Key achievements
  - Areas needing attention

- **Detailed Analysis**
  - Subject-wise performance
  - Section-wise breakdown
  - Time management analysis
  - Question difficulty analysis

- **Visual Elements**
  - Subject-wise performance chart
  - Section-wise performance chart
  - Time distribution graphs

- **Recommendations**
  - Subject-specific improvements
  - Time management strategies
  - Learning resource suggestions

### 2. Performance Metrics
- **Overall Metrics**
  - Total score
  - Accuracy percentage
  - Time efficiency

- **Subject-wise Metrics**
  - Individual subject scores
  - Subject-wise accuracy
  - Time spent per subject

- **Section-wise Metrics**
  - Question-wise performance
  - Difficulty level analysis
  - Topic-wise breakdown

### 3. AI-Generated Insights
- **Strengths**
  - Top performing areas
  - Notable achievements
  - Effective strategies

- **Areas for Improvement**
  - Identified gaps
  - Weak topics
  - Time management issues

- **Actionable Recommendations**
  - Study strategies
  - Resource suggestions
  - Practice recommendations

## Prerequisites

- Python 3.8 or higher
- Google AI API key (Gemini)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/student-performance-analysis.git
cd student-performance-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On Unix or MacOS
source myenv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Place your test data JSON file in the `data` directory
2. Run the main script:
```bash
python main.py
```

3. Find the generated report in the `output` directory

## Project Structure

```
student-performance-analysis/
├── data/                   # Input data directory
├── output/                 # Generated reports and charts
├── src/                    # Source code
│   ├── data_processor.py   # Data processing and analysis
│   ├── feedback_generator.py # AI feedback generation
│   └── pdf_generator.py    # PDF report generation
├── main.py                 # Main application script
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Dependencies

- pandas: Data manipulation and analysis
- matplotlib: Data visualization
- google-generativeai: Google's Gemini AI model
- python-dotenv: Environment variable management
- reportlab: PDF generation
- beautifulsoup4: HTML parsing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI model
- All contributors who have helped improve this project 
