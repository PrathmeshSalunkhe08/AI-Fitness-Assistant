from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_diet_pdf(filename, title, username, lines):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 40
    line_height = 14
    y_position = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_position, title)
    y_position -= line_height * 2

    c.setFont("Helvetica", 11)
    c.drawString(margin, y_position, f"User: {username}")
    y_position -= line_height
    c.drawString(margin, y_position, f"Generated on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    y_position -= line_height
    c.drawString(margin, y_position, "-" * 60)
    y_position -= line_height * 2

    for line in lines:
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 11)
            y_position = height - 50
        
        c.drawString(margin, y_position, str(line))
        y_position -= line_height

    c.save()
