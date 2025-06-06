from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

def create_pdf(feedback, chart_paths, output_path):
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Create styles
    styles = getSampleStyleSheet()
    
    # Create custom styles with unique names
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2E4053')
    ))
    
    styles.add(ParagraphStyle(
        name='ReportSection',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.HexColor('#2874A6')
    ))
    
    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='ReportBullet',
        parent=styles['Normal'],
        fontSize=12,
        leftIndent=20,
        spaceAfter=6,
        leading=14
    ))

    # Process the feedback text
    story = []
    
    # Add title
    story.append(Paragraph("Student Performance Report", styles['ReportTitle']))
    story.append(Spacer(1, 20))

    # Process the feedback text
    lines = feedback.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue

        # Handle section headers (text between **)
        if line.startswith('**') and line.endswith('**'):
            header_text = line[2:-2]  # Remove **
            story.append(Paragraph(header_text, styles['ReportSection']))
            current_section = header_text
            continue

        # Handle bullet points and bold text in the same line
        if line.startswith('*'):
            # Split the line into parts based on bold markers and bullet points
            parts = re.split(r'(\*\*.*?\*\*|\*)', line)
            formatted_parts = []
            
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    # Bold text
                    text = part[2:-2]
                    formatted_parts.append(f'<b>{text}</b>')
                elif part == '*':
                    # Bullet point
                    formatted_parts.append('•')
                else:
                    # Regular text
                    formatted_parts.append(part)
            
            # Join the parts and create the paragraph
            text = ' '.join(formatted_parts)
            story.append(Paragraph(text, styles['ReportBullet']))
        else:
            # Handle regular text with potential bold sections
            parts = re.split(r'(\*\*.*?\*\*)', line)
            formatted_parts = []
            
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    # Bold text
                    text = part[2:-2]
                    formatted_parts.append(f'<b>{text}</b>')
                else:
                    # Regular text
                    formatted_parts.append(part)
            
            # Join the parts and create the paragraph
            text = ' '.join(formatted_parts)
            story.append(Paragraph(text, styles['ReportBody']))

    # Add charts
    story.append(Spacer(1, 20))
    for chart in chart_paths:
        img = Image(chart, width=6*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 20))

    # Build the PDF
    doc.build(story)
