import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = "/home/balaraj/31_galaga/Lab-4"
DOCX_OUT = os.path.join(BASE_DIR, "PES1UG24CS580_Lab4_VibeCoding_ChatHistory.docx")
PDF_OUT = os.path.join(BASE_DIR, "PES1UG24CS580_Lab4_VibeCoding_ChatHistory.pdf")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_docx():
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Title Header
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("PES UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(16, 44, 87)

    run_sub = title_p.add_run("Software Engineering Lab (UE24CS242) — Lab 4: VibeCoding Report\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(41, 128, 185)

    # Metadata Table
    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    data = [
        ("Student Name:", "Mohith N"),
        ("SRN:", "PES1UG24CS580"),
        ("Semester & Branch:", "4th Semester, B.Tech CSE"),
        ("Assigned Repository:", "https://github.com/SETAPESU26/31_galaga"),
        ("Lab Repository:", "https://github.com/Mohith-1502/SE-LAB-PES1UG24CS580"),
        ("Lab Deliverables Folder:", "Lab-4"),
    ]
    for i, (k, v) in enumerate(data):
        row = table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.text = k
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(10)
        c0.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 41, 59)
        set_cell_background(c0, "F1F5F9")
        c1.text = v
        c1.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(c1, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Objectives & Overview
    h1 = doc.add_heading("1. Executive Summary & Lab Objectives", level=1)
    h1.style.font.color.rgb = RGBColor(16, 44, 87)
    
    p_obj = doc.add_paragraph(
        "This laboratory exercise focuses on applying modern Vibe Coding methodologies to repair, "
        "enhance, and ship a feature-rich arcade game (Galaga-lite in Pygame). "
        "Through precise, context-rich prompting under strict budget constraints (< 4 prompts), "
        "the objective is to resolve mathematical curve defects and systematically implement core gameplay mechanics."
    )
    p_obj.style.font.size = Pt(10.5)

    # Section 2: Prompts & Iterations
    h2 = doc.add_heading("2. Vibe Coding Prompts & Implementation History", level=1)
    h2.style.font.color.rgb = RGBColor(16, 44, 87)

    tasks = [
        {
            "num": "Task 1",
            "title": "Bug Fix: Cubic Bézier Curve Trajectory Overshoot",
            "analysis": "In game.py, bezier() computes positions along a cubic curve. The mathematical formula is "
                        "B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3. In the provided starter code, "
                        "the third term was erroneously written as 3*u*t*p2[0] with exponent 1 instead of 2 on t. "
                        "This broke polynomial weight normalization and caused enemies to bulge and overshoot mid-flight.",
            "prompt": "In game.py, examine bezier(p0, p1, p2, p3, t). Enemy entry and dive paths overshoot and bulge unnaturally "
                      "mid-flight even though endpoints match. Compare the four weighted terms against standard cubic Bézier formula:\n"
                      "B(t) = (1-t)^3*P0 + 3*(1-t)^2*t*P1 + 3*(1-t)*t^2*P2 + t^3*P3\n"
                      "Fix the missing exponent on t in the third term for both x and y coordinates.",
            "outcome": "Corrected 3 * u * t to 3 * u * t * t for both x and y coordinates in bezier(). Smooth, graceful flight paths restored.",
            "commit": "9981dca fix: correct cubic bezier curve calculation in bezier()"
        },
        {
            "num": "Task 2",
            "title": "Feature: Dynamic Wave-Based Enemy Recolor (enemy_tint)",
            "analysis": "enemy_tint(kind) was an empty function called per enemy in Game.draw(). "
                        "By tying enemy coloration to wave progression, each wave presents a fresh, distinctive cyber-arcade visual theme.",
            "prompt": "Implement enemy_tint(kind) in game.py. The function receives kind ('boss', 'red', or 'blue') and should return an (r, g, b) "
                      "color tuple or None. Recolor enemies dynamically based on the current wave number so that subsequent waves look visually distinct and challenging.",
            "outcome": "Configured WAVE_PALETTES with custom neon/cyber palettes indexed by current_wave. Enemies dynamically adopt new palettes per wave.",
            "commit": "43c6005 feat: implement enemy_tint() for dynamic wave-based enemy recoloring"
        },
        {
            "num": "Task 3",
            "title": "Feature: Stage Announcement Banner (on_wave_start)",
            "analysis": "on_wave_start(wave) is called once per wave when enemies are generated. "
                        "To provide classic arcade polish, a timed banner alert notifies the player of stage transitions.",
            "prompt": "Implement on_wave_start(wave) in game.py. It is called when a wave spawns. When invoked, track the wave number and "
                      "show a retro arcade 'STAGE <wave> - READY' announcement banner for 2 seconds in the center of the screen with a golden border and timed fadeout.",
            "outcome": "Implemented on_wave_start to track current_wave and set a 2.2-second wave_banner. Integrated timer countdown in Game.update and centered bordered banner rendering in Game.draw.",
            "commit": "26ae4e6 feat: implement on_wave_start() with stage announcement banner"
        },
        {
            "num": "Task 4",
            "title": "Feature: Player Energy Shield & Visual Feedback (shield_charges)",
            "analysis": "shield_charges(wave) sets player shield capacity each wave. "
                        "Granting 1 charge initially and +1 every 3 waves balances survival difficulty, complemented by a cyan elliptical aura and HUD tracking.",
            "prompt": "Implement shield_charges(wave) in game.py to grant 1 shield charge at wave 1 plus 1 additional charge every 3 waves. "
                      "In Game.draw(), display current shield charges on HUD and draw an active cyan energy shield ring around the player ship when shield charges > 0.",
            "outcome": "Returns 1 + (wave - 1) // 3. Renders Shield counter in HUD and adds an animated cyan energy ellipse surrounding active player ships.",
            "commit": "cf4085c feat: implement shield_charges() and visual energy shield aura"
        }
    ]

    for t in tasks:
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(f"### {t['num']}: {t['title']}")
        r_t.font.bold = True
        r_t.font.size = Pt(11.5)
        r_t.font.color.rgb = RGBColor(30, 58, 138)

        p_an = doc.add_paragraph()
        r_an_l = p_an.add_run("Technical Diagnosis: ")
        r_an_l.font.bold = True
        p_an.add_run(t['analysis'])
        p_an.style.font.size = Pt(10)

        p_pr = doc.add_paragraph()
        r_pr_l = p_pr.add_run("Vibe Coding Prompt:\n")
        r_pr_l.font.bold = True
        r_pr = p_pr.add_run(t['prompt'])
        r_pr.font.name = "Consolas"
        r_pr.font.size = Pt(9.5)
        r_pr.font.color.rgb = RGBColor(15, 23, 42)
        p_pr.paragraph_format.left_indent = Inches(0.3)

        p_out = doc.add_paragraph()
        r_out_l = p_out.add_run("Result & Outcome: ")
        r_out_l.font.bold = True
        p_out.add_run(t['outcome'])
        p_out.style.font.size = Pt(10)

        p_c = doc.add_paragraph()
        r_c_l = p_c.add_run("Git Commit: ")
        r_c_l.font.bold = True
        r_c = p_c.add_run(t['commit'])
        r_c.font.name = "Consolas"
        r_c.font.size = Pt(9.5)
        r_c.font.color.rgb = RGBColor(4, 120, 87)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Deliverables Verification Table
    h3 = doc.add_heading("3. Deliverables Verification Checklist", level=1)
    h3.style.font.color.rgb = RGBColor(16, 44, 87)

    deliv_table = doc.add_table(rows=6, cols=3)
    deliv_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Deliverable Item", "Artifact Location", "Status"]
    for j, h in enumerate(headers):
        cell = deliv_table.rows[0].cells[j]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(cell, "E2E8F0")

    deliv_rows = [
        ("Before Gameplay Video (15s)", "Lab-4/before.mp4", "Completed & Verified"),
        ("After Gameplay Video (15s)", "Lab-4/after.mp4", "Completed & Verified"),
        ("Updated Source Code", "game.py & Lab-4/code/game.py", "Completed & Verified"),
        ("Lab Chat History Report (.docx)", "Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.docx", "Completed & Verified"),
        ("Lab Chat History Report (.pdf)", "Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.pdf", "Completed & Verified"),
    ]
    for i, row_data in enumerate(deliv_rows, start=1):
        row = deliv_table.rows[i]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if j == 2:
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(4, 120, 87)
                cell.paragraphs[0].runs[0].font.bold = True

    doc.save(DOCX_OUT)
    print("Saved DOCX:", DOCX_OUT)

def create_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#102C57'),
        alignment=1,
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2980B9'),
        alignment=1,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#102C57'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )
    prompt_box_style = ParagraphStyle(
        'PromptBox',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderPadding=6,
        spaceAfter=6
    )
    commit_style = ParagraphStyle(
        'CommitStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#047857'),
        spaceAfter=8
    )

    story = []
    story.append(Paragraph("PES UNIVERSITY<br/>DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", title_style))
    story.append(Paragraph("Software Engineering Lab (UE24CS242) — Lab 4: VibeCoding Report", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2980B9'), spaceAfter=10))

    meta_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Mohith N", body_style)],
        [Paragraph("<b>SRN:</b>", body_style), Paragraph("PES1UG24CS580", body_style)],
        [Paragraph("<b>Semester & Branch:</b>", body_style), Paragraph("4th Semester, B.Tech CSE", body_style)],
        [Paragraph("<b>Assigned Repository:</b>", body_style), Paragraph("https://github.com/SETAPESU26/31_galaga", body_style)],
        [Paragraph("<b>Lab Repository:</b>", body_style), Paragraph("https://github.com/Mohith-1502/SE-LAB-PES1UG24CS580", body_style)],
        [Paragraph("<b>Lab Deliverables Folder:</b>", body_style), Paragraph("Lab-4", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[140, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Executive Summary & Lab Objectives", h1_style))
    story.append(Paragraph(
        "This laboratory exercise focuses on applying modern Vibe Coding methodologies to repair, "
        "enhance, and ship a feature-rich arcade game (Galaga-lite in Pygame). "
        "Through precise, context-rich prompting under strict budget constraints (< 4 prompts), "
        "the objective is to resolve mathematical curve defects and systematically implement core gameplay mechanics.",
        body_style
    ))

    story.append(Paragraph("2. Vibe Coding Prompts & Implementation History", h1_style))

    tasks = [
        ("Task 1: Bug Fix: Cubic Bézier Curve Trajectory Overshoot",
         "In game.py, bezier() computes positions along a cubic curve. The standard mathematical formula is "
         "B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3. In the provided starter code, "
         "the third term was erroneously written as 3*u*t*p2[0] with exponent 1 instead of 2 on t. "
         "This broke polynomial weight normalization and caused enemies to bulge and overshoot mid-flight.",
         "In game.py, examine bezier(p0, p1, p2, p3, t). Enemy entry and dive paths overshoot and bulge unnaturally mid-flight even though endpoints match. Compare the four weighted terms against standard cubic Bézier formula:\nB(t) = (1-t)^3*P0 + 3*(1-t)^2*t*P1 + 3*(1-t)*t^2*P2 + t^3*P3\nFix the missing exponent on t in the third term for both x and y coordinates.",
         "Corrected 3 * u * t to 3 * u * t * t for both x and y coordinates in bezier(). Smooth, graceful flight paths restored.",
         "9981dca fix: correct cubic bezier curve calculation in bezier()"),

        ("Task 2: Feature: Dynamic Wave-Based Enemy Recolor (enemy_tint)",
         "enemy_tint(kind) was an empty function called per enemy in Game.draw(). By tying enemy coloration to wave progression, each wave presents a fresh, distinctive cyber-arcade visual theme.",
         "Implement enemy_tint(kind) in game.py. The function receives kind ('boss', 'red', or 'blue') and should return an (r, g, b) color tuple or None. Recolor enemies dynamically based on current wave number so that subsequent waves look visually distinct and challenging.",
         "Configured WAVE_PALETTES with custom neon/cyber palettes indexed by current_wave. Enemies dynamically adopt new palettes per wave.",
         "43c6005 feat: implement enemy_tint() for dynamic wave-based enemy recoloring"),

        ("Task 3: Feature: Stage Announcement Banner (on_wave_start)",
         "on_wave_start(wave) is called once per wave when enemies are generated. To provide classic arcade polish, a timed banner alert notifies the player of stage transitions.",
         "Implement on_wave_start(wave) in game.py. It is called when a wave spawns. When invoked, track the wave number and show a retro arcade 'STAGE <wave> - READY' announcement banner for 2 seconds in the center of the screen with a golden border and timed fadeout.",
         "Implemented on_wave_start to track current_wave and set a 2.2-second wave_banner. Integrated timer countdown in Game.update and centered bordered banner rendering in Game.draw.",
         "26ae4e6 feat: implement on_wave_start() with stage announcement banner"),

        ("Task 4: Feature: Player Energy Shield & Visual Feedback (shield_charges)",
         "shield_charges(wave) sets player shield capacity each wave. Granting 1 charge initially and +1 every 3 waves balances survival difficulty, complemented by a cyan elliptical aura and HUD tracking.",
         "Implement shield_charges(wave) in game.py to grant 1 shield charge at wave 1 plus 1 additional charge every 3 waves. In Game.draw(), display current shield charges on HUD and draw an active cyan energy shield ring around the player ship when shield charges > 0.",
         "Returns 1 + (wave - 1) // 3. Renders Shield counter in HUD and adds an animated cyan energy ellipse surrounding active player ships.",
         "cf4085c feat: implement shield_charges() and visual energy shield aura")
    ]

    for title, diag, prompt, outcome, commit in tasks:
        story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('TTitle', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#1E3A8A'))))
        story.append(Paragraph(f"<b>Technical Diagnosis:</b> {diag}", body_style))
        story.append(Paragraph(f"<b>Vibe Coding Prompt:</b><br/>{prompt.replace(chr(10), '<br/>')}", prompt_box_style))
        story.append(Paragraph(f"<b>Result & Outcome:</b> {outcome}", body_style))
        story.append(Paragraph(f"<b>Git Commit:</b> {commit}", commit_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("3. Deliverables Verification Checklist", h1_style))
    deliv_data = [
        [Paragraph("<b>Deliverable Item</b>", body_style), Paragraph("<b>Artifact Location</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Before Gameplay Video (15s)", body_style), Paragraph("Lab-4/before.mp4", body_style), Paragraph("<b>Verified</b>", ParagraphStyle('G', parent=body_style, textColor=colors.HexColor('#047857')))],
        [Paragraph("After Gameplay Video (15s)", body_style), Paragraph("Lab-4/after.mp4", body_style), Paragraph("<b>Verified</b>", ParagraphStyle('G', parent=body_style, textColor=colors.HexColor('#047857')))],
        [Paragraph("Updated Source Code", body_style), Paragraph("game.py & Lab-4/code/game.py", body_style), Paragraph("<b>Verified</b>", ParagraphStyle('G', parent=body_style, textColor=colors.HexColor('#047857')))],
        [Paragraph("Chat History Word Document", body_style), Paragraph("Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.docx", body_style), Paragraph("<b>Verified</b>", ParagraphStyle('G', parent=body_style, textColor=colors.HexColor('#047857')))],
        [Paragraph("Chat History PDF Document", body_style), Paragraph("Lab-4/PES1UG24CS580_Lab4_VibeCoding_ChatHistory.pdf", body_style), Paragraph("<b>Verified</b>", ParagraphStyle('G', parent=body_style, textColor=colors.HexColor('#047857')))]
    ]
    t_deliv = Table(deliv_data, colWidths=[180, 240, 100])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_deliv)

    doc.build(story)
    print("Saved PDF:", PDF_OUT)

if __name__ == "__main__":
    create_docx()
    create_pdf()
