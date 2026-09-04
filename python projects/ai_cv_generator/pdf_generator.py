import io
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
)

from utils import ResumeData

class PDFResumeGenerator:
    """Generates styled vector PDFs from ResumeData using ReportLab."""

    THEME_COLORS = {
        "Modern Executive": {
            "primary": colors.HexColor("#1e3a8a"),    # Deep Navy Blue
            "secondary": colors.HexColor("#3b82f6"),  # Bright Blue
            "text": colors.HexColor("#1f2937"),       # Charcoal Gray
            "accent": colors.HexColor("#f3f4f6"),     # Light Gray Background
            "divider": colors.HexColor("#cbd5e1")
        },
        "Creative Tech": {
            "primary": colors.HexColor("#0f766e"),    # Dark Teal
            "secondary": colors.HexColor("#0d9488"),  # Teal
            "text": colors.HexColor("#18181b"),       # Dark Zinc
            "accent": colors.HexColor("#ccfbf1"),     # Mint Tint
            "divider": colors.HexColor("#99f6e4")
        },
        "Minimalist Classic": {
            "primary": colors.HexColor("#18181b"),    # Almost Black
            "secondary": colors.HexColor("#52525b"),  # Medium Zinc
            "text": colors.HexColor("#27272a"),       # Soft Charcoal
            "accent": colors.HexColor("#f4f4f5"),     # Off-White
            "divider": colors.HexColor("#e4e4e7")
        }
    }

    def __init__(self, theme_name: str = "Modern Executive"):
        self.theme_name = theme_name if theme_name in self.THEME_COLORS else "Modern Executive"
        self.colors_cfg = self.THEME_COLORS[self.theme_name]

    def _get_styles(self):
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CVName',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=self.colors_cfg["primary"],
            spaceAfter=2
        )

        job_title_style = ParagraphStyle(
            'CVJobTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=self.colors_cfg["secondary"],
            spaceAfter=6
        )

        contact_style = ParagraphStyle(
            'CVContact',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=self.colors_cfg["text"],
            alignment=0 # Left aligned
        )

        section_heading = ParagraphStyle(
            'CVSectionHeading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=self.colors_cfg["primary"],
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            'CVBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=self.colors_cfg["text"],
            spaceAfter=4
        )

        bullet_style = ParagraphStyle(
            'CVBullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=self.colors_cfg["text"],
            leftIndent=12,
            spaceAfter=3
        )

        bold_item_title = ParagraphStyle(
            'CVItemTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10.5,
            leading=13,
            textColor=self.colors_cfg["primary"]
        )

        sub_item_title = ParagraphStyle(
            'CVSubItemTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9.5,
            leading=12,
            textColor=self.colors_cfg["secondary"]
        )

        right_date_style = ParagraphStyle(
            'CVRightDate',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=12,
            textColor=self.colors_cfg["secondary"],
            alignment=2 # Right aligned
        )

        return {
            "title": title_style,
            "job_title": job_title_style,
            "contact": contact_style,
            "heading": section_heading,
            "body": body_style,
            "bullet": bullet_style,
            "item_title": bold_item_title,
            "sub_title": sub_item_title,
            "date": right_date_style
        }

    def generate(self, data: ResumeData) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        st = self._get_styles()
        story = []

        # --- HEADER SECTION ---
        story.append(Paragraph(data.full_name, st["title"]))
        if data.job_title:
            story.append(Paragraph(data.job_title.upper(), st["job_title"]))

        # Contact line
        contact_parts = []
        if data.email: contact_parts.append(data.email)
        if data.phone: contact_parts.append(data.phone)
        if data.location: contact_parts.append(data.location)
        if data.linkedin: contact_parts.append(f"LinkedIn: {data.linkedin}")
        if data.github: contact_parts.append(f"GitHub: {data.github}")
        if data.portfolio: contact_parts.append(f"Portfolio: {data.portfolio}")

        contact_text = "  •  ".join(contact_parts)
        story.append(Paragraph(contact_text, st["contact"]))
        story.append(Spacer(1, 6))

        # Colored divider bar
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=self.colors_cfg["primary"],
            spaceAfter=8,
            spaceBefore=2
        ))

        # --- EXECUTIVE SUMMARY ---
        if data.summary:
            story.append(Paragraph("PROFESSIONAL SUMMARY", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))
            story.append(Paragraph(data.summary, st["body"]))
            story.append(Spacer(1, 6))

        # --- SKILLS SECTION ---
        if data.skills:
            story.append(Paragraph("CORE COMPETENCIES & TECHNICAL SKILLS", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))
            skills_formatted = "  •  ".join(data.skills)
            story.append(Paragraph(f"<b>Key Skills:</b> {skills_formatted}", st["body"]))
            story.append(Spacer(1, 6))

        # --- WORK EXPERIENCE ---
        if data.experiences:
            story.append(Paragraph("WORK EXPERIENCE", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))
            
            for exp in data.experiences:
                date_str = f"{exp.start_date} – {exp.end_date}" if exp.end_date else exp.start_date
                loc_str = f" ({exp.location})" if exp.location else ""
                
                header_table_data = [
                    [
                        Paragraph(f"<b>{exp.role}</b>", st["item_title"]),
                        Paragraph(date_str, st["date"])
                    ],
                    [
                        Paragraph(f"{exp.company}{loc_str}", st["sub_title"]),
                        Paragraph("", st["date"])
                    ]
                ]
                
                t = Table(header_table_data, colWidths=[380, 160])
                t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                ]))
                
                story.append(t)
                story.append(Spacer(1, 3))
                
                for b in exp.bullets:
                    if b.strip():
                        story.append(Paragraph(f"• {b.strip()}", st["bullet"]))
                story.append(Spacer(1, 6))

        # --- PROJECTS SECTION ---
        if data.projects:
            story.append(Paragraph("FEATURED PROJECTS", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))

            for proj in data.projects:
                tech_info = f" [{proj.tech_stack}]" if proj.tech_stack else ""
                link_info = f" ({proj.link})" if proj.link else ""
                
                header_table_data = [
                    [
                        Paragraph(f"<b>{proj.title}</b>{tech_info}", st["item_title"]),
                        Paragraph(link_info, st["date"])
                    ]
                ]
                t = Table(header_table_data, colWidths=[380, 160])
                t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                ]))
                story.append(t)
                if proj.description:
                    story.append(Paragraph(proj.description, st["body"]))
                for b in proj.bullets:
                    if b.strip():
                        story.append(Paragraph(f"• {b.strip()}", st["bullet"]))
                story.append(Spacer(1, 5))

        # --- EDUCATION SECTION ---
        if data.education:
            story.append(Paragraph("EDUCATION", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))

            for edu in data.education:
                date_str = f"{edu.start_date} – {edu.end_date}" if edu.end_date else edu.start_date
                gpa_str = f" (GPA: {edu.gpa})" if edu.gpa else ""
                degree_full = f"{edu.degree} in {edu.field_of_study}" if edu.field_of_study else edu.degree
                
                header_table_data = [
                    [
                        Paragraph(f"<b>{edu.institution}</b>", st["item_title"]),
                        Paragraph(date_str, st["date"])
                    ],
                    [
                        Paragraph(f"{degree_full}{gpa_str}", st["sub_title"]),
                        Paragraph("", st["date"])
                    ]
                ]
                t = Table(header_table_data, colWidths=[380, 160])
                t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                ]))
                story.append(t)
                story.append(Spacer(1, 4))

        # --- CERTIFICATIONS ---
        if data.certifications:
            story.append(Paragraph("CERTIFICATIONS & AWARDS", st["heading"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=self.colors_cfg["divider"], spaceAfter=4, spaceBefore=1))
            
            cert_lines = []
            for cert in data.certifications:
                yr = f" ({cert.year})" if cert.year else ""
                issuer = f" – {cert.issuer}" if cert.issuer else ""
                cert_lines.append(f"<b>{cert.name}</b>{issuer}{yr}")
            
            story.append(Paragraph("  •  ".join(cert_lines), st["body"]))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
