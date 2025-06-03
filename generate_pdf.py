from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os

def generate_pdf(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ✅ โลโก้ SAS มุมขวาบน
    try:
        logo_path = os.path.abspath("static/sas_logo.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=120, height=60)
            logo.hAlign = 'RIGHT'
            story.append(logo)
    except:
        pass

    story.append(Spacer(1, 12))

    # ✅ ข้อมูลทั่วไปในตาราง
    table_data = [
        ['Motor Model', data['motor_model']],
        ['Power', f"{data['motor_power']} {data['power_unit']}"],
        ['Gear Model', data['gear_model']],
        ['Gear Ratio', data['gear_ratio']],
        ['Voltage', data['voltage']],
        ['Customer Requirement', data['customer_requirement']],
        ['Accessories', ', '.join(data['accessories']) if data['accessories'] else '-'],
    ]

    table = Table(table_data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # ✅ แสดงรูปภาพแนวนอน
    images = []
    for key in ['motor_image', 'gear_image', 'installation_image']:
        img_path = os.path.abspath(data[key])
        if os.path.exists(img_path):
            img = Image(img_path, width=150, height=120)
            images.append(img)

    if images:
        image_table = Table([images], hAlign='CENTER', colWidths=[160]*len(images))
        story.append(image_table)

    story.append(Spacer(1, 50))

    # ✅ วันที่และชื่อผู้ขอ มุมขวาล่าง
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Paragraph(f"Requested by: {data['requested_by']}", styles['Normal']))

    doc.build(story)