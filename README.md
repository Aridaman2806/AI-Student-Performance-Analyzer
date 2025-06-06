# Student Performance Analysis System

An AI-powered system that analyzes student test performance and generates detailed feedback reports using Google's Gemini AI model.

## Features

- Analyzes student test data from JSON format
- Generates comprehensive performance reports
- Creates visual performance charts
- Provides AI-powered insights and recommendations
- Generates PDF reports with detailed analysis

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