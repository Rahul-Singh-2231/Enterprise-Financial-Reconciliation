import os
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def create_resume(output_path):
    # Standard Letter: 612 x 792 points
    # Printable area: 556 width x 752 height
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # Classic Monochrome Palette (No blue colors, pure clean black/charcoal)
    BLACK = colors.HexColor("#000000")
    DARK = colors.HexColor("#111111")
    LINE_COLOR = colors.HexColor("#000000")

    CONTENT_WIDTH = 556

    # Typography styles - ALL TIMES NEW ROMAN
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=20,
        textColor=BLACK,
        alignment=1 # Center
    )

    tagline_style = ParagraphStyle(
        'ResumeTagline',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=12,
        textColor=BLACK,
        alignment=1 # Center
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11,
        textColor=BLACK,
        alignment=1 # Center
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=12,
        textColor=BLACK,
        spaceAfter=0
    )

    summary_style = ParagraphStyle(
        'ResumeSummary',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=10.8,
        textColor=DARK
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=10.8,
        textColor=DARK
    )

    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.9,
        leading=11,
        textColor=BLACK
    )

    item_subtitle_style = ParagraphStyle(
        'ItemSubtitle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.2,
        leading=10,
        textColor=DARK
    )

    item_date_style = ParagraphStyle(
        'ItemDate',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        textColor=BLACK,
        alignment=2 # Right
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.3,
        leading=10.4,
        textColor=DARK
    )

    story = []

    # 1. HEADER
    story.append(Paragraph("RAHUL SINGH", name_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Data Analyst | Business Intelligence | Applied Machine Learning", tagline_style))
    story.append(Spacer(1, 2.5))
    
    contact_text = (
        "+91 7485056992 &nbsp;|&nbsp; "
        '<a href="mailto:rahulsinghrajput2231@gmail.com" color="#000000"><u>rahulsinghrajput2231@gmail.com</u></a> &nbsp;|&nbsp; '
        '<a href="https://linkedin.com/in/rahul-singh-867561336" color="#000000"><u>linkedin.com/in/rahul-singh-867561336</u></a> &nbsp;|&nbsp; '
        '<a href="https://github.com/Rahul-Singh-2231" color="#000000"><u>github.com/Rahul-Singh-2231</u></a> &nbsp;|&nbsp; '
        "Ahmedabad, Gujarat"
    )
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 4))

    def add_section_header(title):
        t = Table(
            [[Paragraph(title.upper(), section_heading_style)]],
            colWidths=[CONTENT_WIDTH]
        )
        t.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t)
        story.append(HRFlowable(width="100%", thickness=0.8, color=LINE_COLOR, spaceBefore=1, spaceAfter=3))

    def make_row(left_text, right_text, left_style=item_title_style, right_style=item_date_style):
        t = Table(
            [[Paragraph(left_text, left_style), Paragraph(right_text, right_style)]],
            colWidths=[428, 128]
        )
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def add_bullet(text):
        bullet_p = Paragraph(f"&bull;&nbsp;&nbsp;{text}", bullet_style)
        b_table = Table([[bullet_p]], colWidths=[CONTENT_WIDTH])
        b_table.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 0.35),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.35),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(b_table)

    # 2. PROFESSIONAL SUMMARY
    add_section_header("Professional Summary")
    summary_text = (
        "<b>B.Tech Computer Engineering student (Artificial Intelligence, CGPA: 7.20/10)</b> with hands-on expertise "
        "in end-to-end data analytics, SQL window functions, automated financial reconciliation, and regression modeling. "
        "Proficient in converting multi-source, unstructured, and transactional datasets into validated, decision-ready "
        "insights using <b>Python (Pandas, NumPy), SQL (Window Functions, CTEs), Tableau, and Power BI</b>. Proven track record "
        "in resolving temporal data mismatches, architecting Star Schema dimensional models, and deploying executive-level dashboards."
    )
    story.append(Paragraph(summary_text, summary_style))
    story.append(Spacer(1, 3.5))

    # 3. TECHNICAL SKILLS
    add_section_header("Technical Skills")
    skills = [
        ("Programming &amp; Querying:", "Python (Pandas, NumPy), SQL (MySQL, SQLite - Window Functions, CTEs), Regular Expressions (Regex), C"),
        ("Data Visualization &amp; BI:", "Tableau (Calculated Fields, Filter Actions), Power BI, Microsoft Excel, Matplotlib, Seaborn"),
        ("Data Engineering &amp; Analytics:", "Financial &amp; Temporal Data Reconciliation, ETL Pipelines, Slowly Changing Dimensions (SCD), Feature Engineering, Statistical Modeling, NLP (spaCy, NLTK)"),
        ("Tools &amp; Platforms:", "Git / GitHub, VS Code, Jupyter Notebook, Flask, Power Query")
    ]
    for cat, items in skills:
        p = Paragraph(f"<b>{cat}</b> {items}", body_style)
        t = Table([[p]], colWidths=[CONTENT_WIDTH])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 0.35),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.35),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t)
    story.append(Spacer(1, 3.5))

    # 4. PROJECTS
    add_section_header("Projects")

    # Project 1: Enterprise Financial Data Reconciliation (The New Project!)
    story.append(make_row("Enterprise Financial Data Reconciliation &amp; Audit Pipeline", "Oct 2026"))
    story.append(Paragraph("Technologies: Python (Pandas, NumPy), SQLite, Regular Expressions (Regex), Matplotlib, Seaborn", item_subtitle_style))
    add_bullet("Architected a multi-source financial reconciliation pipeline integrating 100K raw server logs, SQLite customer records, and daily FX market feeds to audit <b>$148.27M USD</b> in genuine enterprise revenue.")
    add_bullet("Formulated SQL Window Functions (<code>ROW_NUMBER() OVER PARTITION BY</code>) inside CTEs to resolve Slowly Changing Dimensions (SCD), deduplicating 47,464 historical records into <b>14,183 unique active customer states</b>.")
    add_bullet("Engineered vectorized regex extraction to parse semi-structured transaction logs with <b>100% match accuracy</b> (0 nulls), dropping 5,098 system ERROR logs to eliminate fictitious transactions.")
    add_bullet("Resolved temporal financial market mismatches (5-day FX market vs. 7-day transactional logs) using forward-fill (<code>ffill</code>), preserving <b>100% of weekend purchases</b> and preventing a ~28.5% data loss.")
    add_bullet("Delivered executive CFO visual analytics in Matplotlib/Seaborn tracking 12-month revenue stability ($12.36M/mo avg) and customer spend concentration to validate business risk diversification.")
    story.append(Spacer(1, 2.5))

    # Project 2: Manufacturing Telemetry Dashboard
    story.append(make_row("Manufacturing Telemetry Dashboard - Data Analytics Job Simulation", "Jul 2026"))
    story.append(Paragraph("Technologies: Tableau, Data Cleaning, Telemetry Analysis", item_subtitle_style))
    add_bullet("Built interactive Tableau executive dashboards to monitor telemetry across multiple factories and machine device types.")
    add_bullet("Created calculated fields to quantify machine downtime from status events, visualizing downtime by factory and device to pinpoint bottlenecks.")
    add_bullet("Added dashboard filter actions for seamless drill-down analysis from factory level to individual device types.")
    story.append(Spacer(1, 2.5))

    # Project 3: Real Estate Market Analysis
    story.append(make_row("Real Estate Market Analysis &amp; Price Prediction", "Aug 2025 - Present"))
    story.append(Paragraph("Technologies: Python (Pandas, Scikit-Learn), Random Forest, Gradient Boosting", item_subtitle_style))
    add_bullet("Executed exploratory data analysis and feature correlation on housing datasets to identify key valuation drivers.")
    add_bullet("Trained and evaluated Random Forest and Gradient Boosting regression models, achieving an <b>85% R<sup>2</sup> score</b>.")
    story.append(Spacer(1, 2.5))

    # Project 4: Automated Talent Data Matching
    story.append(make_row("Automated Talent Data Matching System", "Jul 2025"))
    story.append(Paragraph("Technologies: Python, NLP (spaCy, NLTK), SQL", item_subtitle_style))
    add_bullet("Leveraged NLP pipelines (spaCy, NLTK) to convert unstructured resume documents into structured, queryable data entities.")
    add_bullet("Designed a relational SQL backend ranking candidate-job alignment, streamlining large-scale talent candidate retrieval.")
    story.append(Spacer(1, 2.5))

    # Project 5: Data Transformation with Power Query
    story.append(make_row("Data Transformation &amp; Modeling with Power Query", "Jul 2025"))
    story.append(Paragraph("Technologies: Power Query, Star Schema, SQL, Microsoft Excel", item_subtitle_style))
    add_bullet("Cleaned and normalized raw transactional datasets from disparate SQL and Excel sources using Power Query.")
    add_bullet("Constructed a unified Star Schema dimensional model with fact and dimension tables to support consistent, scalable reporting.")
    story.append(Spacer(1, 3.5))

    # 5. EDUCATION
    add_section_header("Education")
    story.append(make_row("B.Tech - Computer Engineering (Artificial Intelligence)", "2023 - 2027"))
    story.append(Paragraph("UV Patel College of Engineering, Ganpat University, Gujarat &nbsp;|&nbsp; <b>CGPA: 7.20 / 10.0</b>", item_subtitle_style))
    coursework = (
        "<b>Coursework:</b> Machine Learning, Deep Learning, Computer Vision, Data Science, "
        "Database Management (SQL), Object-Oriented Programming (Python/C), Computer Networks."
    )
    story.append(Paragraph(coursework, body_style))
    story.append(Spacer(1, 3.5))

    # 6. CERTIFICATIONS
    add_section_header("Certifications")
    certs_row1 = "<b>IBM Certified:</b> Deep Learning Fundamentals (Intermediate) &nbsp;&nbsp;|&nbsp;&nbsp; <b>Python 101 for Data Science:</b> IBM Cognitive Class (Jul 2025)"
    certs_row2 = "<b>AWS Foundations:</b> Machine Learning Basics (Jul 2025) &nbsp;&nbsp;|&nbsp;&nbsp; <b>Introduction to Fundamentals of Databases:</b> Relational SQL (Oct 2024)"
    certs_row3 = "<b>Data Analytics Job Simulation:</b> End-to-End Analytics Completion (Jul 2026)"
    
    for row_text in [certs_row1, certs_row2, certs_row3]:
        p = Paragraph(f"&bull;&nbsp;&nbsp;{row_text}", bullet_style)
        t = Table([[p]], colWidths=[CONTENT_WIDTH])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 0.3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t)

    doc.build(story)

    # Check page count
    reader = pypdf.PdfReader(output_path)
    print(f"Generated PDF: {output_path}")
    print(f"Total Page Count: {len(reader.pages)}")

if __name__ == '__main__':
    create_resume("Rahul_Singh_Resume.pdf")
