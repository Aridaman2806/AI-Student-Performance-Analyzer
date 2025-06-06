import json
from typing import Dict, List, Any
import re
from bs4 import BeautifulSoup
import google.generativeai as genai

class DataProcessor:
    def __init__(self, json_path: str, api_key: str):
        self.json_path = json_path
        self.api_key = api_key
        self.data = self._load_json()
        genai.configure(api_key=self.api_key)
        # Try to use gemini-pro model first, fallback to gemini-2.0-flash if not available
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def _load_json(self) -> Dict:
        """Load and parse the JSON file."""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)[0]  # Assuming first item in array
            
    def _parse_syllabus(self) -> Dict[str, List[str]]:
        """Parse the syllabus HTML into a structured format."""
        soup = BeautifulSoup(self.data['test']['syllabus'], 'html.parser')
        syllabus = {}
        
        # Extract subject sections
        for subject in soup.find_all('h2'):
            subject_name = subject.text.strip()
            topics = [li.text.strip() for li in subject.find_next('ul').find_all('li')]
            syllabus[subject_name] = topics
            
        return syllabus
        
    def _get_subject_name(self, subject_id: str) -> str:
        """Map subject ID to subject name."""
        subject_map = {
            "607018ee404ae53194e73d92": "Physics",
            "607018ee404ae53194e73d90": "Chemistry",
            "607018ee404ae53194e73d91": "Mathematics"
        }
        return subject_map.get(subject_id, "Unknown")
        
    def _is_correct_answer(self, question: Dict) -> bool:
        """Check if the question was answered correctly."""
        # Check marked options
        if 'markedOptions' in question:
            for option in question['markedOptions']:
                if option.get('isCorrect', False):
                    return True
                    
        # Check input value for numerical questions
        if 'inputValue' in question and question['inputValue'] is not None:
            return question['inputValue'].get('isCorrect', False)
            
        return False
        
    def _analyze_question_performance(self, questions: List[Dict]) -> Dict[str, Any]:
        """Analyze performance at question level."""
        analysis = {
            'total_questions': len(questions),
            'correct_answers': 0,
            'incorrect_answers': 0,
            'unattempted': 0,
            'time_analysis': {
                'total_time': 0,
                'avg_time_per_question': 0,
                'time_distribution': {
                    'quick': 0,  # < 30 seconds
                    'moderate': 0,  # 30-60 seconds
                    'slow': 0  # > 60 seconds
                }
            },
            'difficulty_analysis': {
                'easy': {'total': 0, 'correct': 0},
                'medium': {'total': 0, 'correct': 0},
                'tough': {'total': 0, 'correct': 0}
            },
            'chapter_wise': {},
            'topic_wise': {}
        }
        
        for q in questions:
            # Count correct/incorrect/unattempted
            if q['status'] == 'answered':
                if self._is_correct_answer(q):
                    analysis['correct_answers'] += 1
                else:
                    analysis['incorrect_answers'] += 1
            else:
                analysis['unattempted'] += 1
                
            # Time analysis
            time_taken = q.get('timeTaken', 0)
            analysis['time_analysis']['total_time'] += time_taken
            
            if time_taken < 30:
                analysis['time_analysis']['time_distribution']['quick'] += 1
            elif time_taken < 60:
                analysis['time_analysis']['time_distribution']['moderate'] += 1
            else:
                analysis['time_analysis']['time_distribution']['slow'] += 1
                
            # Difficulty analysis
            difficulty = q['questionId']['level']
            analysis['difficulty_analysis'][difficulty]['total'] += 1
            if self._is_correct_answer(q):
                analysis['difficulty_analysis'][difficulty]['correct'] += 1
                
            # Chapter and topic analysis
            for chapter in q['questionId']['chapters']:
                chapter_name = chapter['title']
                if chapter_name not in analysis['chapter_wise']:
                    analysis['chapter_wise'][chapter_name] = {'total': 0, 'correct': 0}
                analysis['chapter_wise'][chapter_name]['total'] += 1
                if self._is_correct_answer(q):
                    analysis['chapter_wise'][chapter_name]['correct'] += 1
                    
            for topic in q['questionId']['topics']:
                topic_name = topic['title']
                if topic_name not in analysis['topic_wise']:
                    analysis['topic_wise'][topic_name] = {'total': 0, 'correct': 0}
                analysis['topic_wise'][topic_name]['total'] += 1
                if self._is_correct_answer(q):
                    analysis['topic_wise'][topic_name]['correct'] += 1
                    
        # Calculate averages
        if analysis['total_questions'] > 0:
            analysis['time_analysis']['avg_time_per_question'] = (
                analysis['time_analysis']['total_time'] / analysis['total_questions']
            )
            
        return analysis
        
    def _parse_with_gemini(self, data: Dict) -> Dict:
        """Use Gemini to parse and structure the JSON data."""
        # Create a more focused prompt that's easier for the model to handle
        prompt = f"""Analyze this student test data and provide insights in a structured format.
        
        Test Data Summary:
        - Total Questions: {data['test_info']['total_questions']}
        - Total Marks: {data['test_info']['total_marks']}
        - Overall Accuracy: {data['overall_performance']['accuracy']}%
        
        Subject-wise Performance:
        {json.dumps(data['subject_wise'], indent=2)}
        
        Please analyze this data and provide:
        1. Overall strengths (list 2-3 key strengths)
        2. Areas for improvement (list 2-3 key areas)
        3. Time management analysis (2-3 points)
        4. Specific recommendations for improvement (3-4 points)
        
        Format your response as a JSON object with these exact keys:
        {{
            "strengths": [],
            "improvements": [],
            "time_management": [],
            "recommendations": []
        }}
        
        Keep each point concise and specific."""
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response text to ensure it's valid JSON
            response_text = response.text.strip()
            # Remove any markdown code block markers
            response_text = re.sub(r'```json\s*|\s*```', '', response_text)
            # Parse the cleaned response
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error in Gemini parsing: {str(e)}")
            # Return a default structure if parsing fails
            return {
                "strengths": ["Unable to analyze strengths at this time"],
                "improvements": ["Unable to analyze areas for improvement at this time"],
                "time_management": ["Unable to analyze time management at this time"],
                "recommendations": ["Please review the raw performance data for insights"]
            }

    def process_data(self) -> Dict[str, Any]:
        """Process all data and return a structured format for the LLM."""
        # First get the basic structured data
        processed_data = {
            'test_info': {
                'total_time': self.data['test']['totalTime'],
                'total_questions': self.data['test']['totalQuestions'],
                'total_marks': self.data['test']['totalMarks'],
                'syllabus': self._parse_syllabus()
            },
            'overall_performance': {
                'total_time_taken': self.data['totalTimeTaken'],
                'total_marks_scored': self.data['totalMarkScored'],
                'total_attempted': self.data['totalAttempted'],
                'total_correct': self.data['totalCorrect'],
                'accuracy': self.data['accuracy']
            },
            'subject_wise': {},
            'section_wise': {}
        }
        
        # Process subject-wise data
        for subject in self.data['subjects']:
            subject_name = self._get_subject_name(str(subject['subjectId']['$oid']))
            processed_data['subject_wise'][subject_name] = {
                'time_taken': subject['totalTimeTaken'],
                'marks_scored': subject['totalMarkScored'],
                'questions_attempted': subject['totalAttempted'],
                'correct_answers': subject['totalCorrect'],
                'accuracy': subject['accuracy']
            }
            
        # Process section-wise data
        for section in self.data['sections']:
            section_name = section['sectionId']['title']
            processed_data['section_wise'][section_name] = self._analyze_question_performance(section['questions'])
        
        # Use Gemini to get deeper insights
        gemini_analysis = self._parse_with_gemini(processed_data)
        processed_data['gemini_analysis'] = gemini_analysis
            
        return processed_data
        
    def get_llm_prompt(self) -> str:
        """Generate a comprehensive prompt for the LLM."""
        data = self.process_data()
        
        prompt = f"""Generate a detailed student performance report based on the following test data:

TEST OVERVIEW:
- Total Duration: {data['test_info']['total_time']} minutes
- Total Questions: {data['test_info']['total_questions']}
- Total Marks: {data['test_info']['total_marks']}

OVERALL PERFORMANCE:
- Total Time Taken: {data['overall_performance']['total_time_taken']} seconds
- Total Marks Scored: {data['overall_performance']['total_marks_scored']}
- Questions Attempted: {data['overall_performance']['total_attempted']}
- Correct Answers: {data['overall_performance']['total_correct']}
- Overall Accuracy: {data['overall_performance']['accuracy']}%

SUBJECT-WISE PERFORMANCE:
"""
        
        # Add subject-wise performance
        for subject, performance in data['subject_wise'].items():
            prompt += f"""
{subject}:
- Time Taken: {performance['time_taken']} seconds
- Marks Scored: {performance['marks_scored']}
- Questions Attempted: {performance['questions_attempted']}
- Correct Answers: {performance['correct_answers']}
- Accuracy: {performance['accuracy']}%
"""
            
        # Add section-wise analysis
        prompt += "\nDETAILED SECTION ANALYSIS:\n"
        for section, analysis in data['section_wise'].items():
            prompt += f"""
{section}:
- Total Questions: {analysis['total_questions']}
- Correct Answers: {analysis['correct_answers']}
- Incorrect Answers: {analysis['incorrect_answers']}
- Unattempted: {analysis['unattempted']}
- Average Time per Question: {analysis['time_analysis']['avg_time_per_question']:.2f} seconds

Difficulty-wise Performance:
"""
            
            for difficulty, stats in analysis['difficulty_analysis'].items():
                if stats['total'] > 0:
                    accuracy = (stats['correct'] / stats['total']) * 100
                    prompt += f"- {difficulty.capitalize()}: {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)\n"
                    
            prompt += "\nChapter-wise Performance:\n"
            for chapter, stats in analysis['chapter_wise'].items():
                if stats['total'] > 0:
                    accuracy = (stats['correct'] / stats['total']) * 100
                    prompt += f"- {chapter}: {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)\n"
                    
            prompt += "\nTopic-wise Performance:\n"
            for topic, stats in analysis['topic_wise'].items():
                if stats['total'] > 0:
                    accuracy = (stats['correct'] / stats['total']) * 100
                    prompt += f"- {topic}: {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)\n"

        # Add Gemini's analysis
        if 'gemini_analysis' in data:
            prompt += "\nAI ANALYSIS AND RECOMMENDATIONS:\n"
            gemini_data = data['gemini_analysis']
            
            if 'strengths' in gemini_data:
                prompt += "\nKey Strengths:\n"
                for strength in gemini_data['strengths']:
                    prompt += f"- {strength}\n"
            
            if 'improvements' in gemini_data:
                prompt += "\nAreas for Improvement:\n"
                for improvement in gemini_data['improvements']:
                    prompt += f"- {improvement}\n"
            
            if 'time_management' in gemini_data:
                prompt += "\nTime Management Analysis:\n"
                for point in gemini_data['time_management']:
                    prompt += f"- {point}\n"
            
            if 'recommendations' in gemini_data:
                prompt += "\nRecommendations:\n"
                for recommendation in gemini_data['recommendations']:
                    prompt += f"- {recommendation}\n"
                    
        prompt += """
Based on this data, generate a comprehensive performance report that:
1. Provides an overall assessment of the student's performance
2. Highlights strengths and areas for improvement
3. Analyzes time management and question selection strategy
4. Gives specific recommendations for improvement
5. Maintains an encouraging and positive tone throughout

Format the report with clear sections, bullet points, and bold headers for better readability.
"""
        
        return prompt
