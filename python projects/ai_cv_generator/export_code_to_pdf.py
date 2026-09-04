import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted, PageBreak
)

def build_code_pdf(output_filename="AI_CV_Generator_SourceCode.pdf"):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_include = [
        ("README.md", "Documentation & LinkedIn Post Template"),
        ("requirements.txt", "Project Dependencies Specification"),
        ("app.py", "Streamlit Main Web Application & Glassmorphism UI"),
        ("ai_engine.py", "AI Engine Wrapper (Gemini, OpenAI & Smart Fallback)"),
        ("pdf_generator.py", "ReportLab Vector PDF Resume Generator Engine"),
        ("utils.py", "Data Models, Sample Data & Helper Utilities"),
        (".env.example", "Environment Variables Template")
    ]

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1, # Centered
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=20
    )

    section_header_style = ParagraphStyle(
        'FileHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=15,
        spaceAfter=4
    )

    file_desc_style = ParagraphStyle(
        'FileDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#e2e8f0"),
        borderWidth=0.5,
        borderPadding=8,
        spaceAfter=12
    )

    story = []

    # Title Banner
    story.append(Spacer(1, 20))
    story.append(Paragraph("📄 AI RESUMIX PRO — SOURCE CODE DOCUMENT", title_style))
    story.append(Paragraph("Complete Python Codebase & Project Specifications", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1e3a8a"), spaceAfter=20))

    for filename, description in files_to_include:
        filepath = os.path.join(project_dir, filename)
        if not os.path.exists(filepath):
            continue

        story.append(Paragraph(f"📁 {filename}", section_header_style))
        story.append(Paragraph(description, file_desc_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=8))

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Sanitize HTML tags for ReportLab Paragraph compatibility
        content_escaped = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Preformatted code snippet
        story.append(Preformatted(content_escaped, code_style))
        story.append(Spacer(1, 10))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor("#94a3b8"))
        canvas.drawString(36, 20, "AI Resumix Pro — Source Code Compilation PDF")
        canvas.drawRightString(612 - 36, 20, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Code PDF generated successfully at: {output_filename}")

if __name__ == "__main__":
    build_code_pdf()
