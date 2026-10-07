"""
MediPlant AI - PDF Report Generator
Generates a downloadable PDF report for each plant identification
"""

from fpdf import FPDF
from datetime import datetime
import io
import json


class MediPlantReport(FPDF):
    def header(self):
        self.set_fill_color(46, 139, 87)
        self.rect(0, 0, 210, 25, "F")
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, "  MediPlant AI - Identification Report", ln=True, align="L")
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"MediPlant AI  |  Page {self.page_no()}  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")

    def section_title(self, title, color=(46, 139, 87)):
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*color)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(*color)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def info_row(self, label, value):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(55, 7, f"  {label}:", ln=False)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, str(value), ln=True)

    def bullet_item(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(8, 6, "  •", ln=False)
        self.multi_cell(0, 6, text)


def generate_pdf_report(result, plant_info, username="Guest"):
    """
    Generate a full PDF report for a plant identification result.
    Returns bytes of the PDF.
    """
    pdf = MediPlantReport()
    pdf.set_margins(10, 28, 10)
    pdf.add_page()

    # ── Date/User Info ───────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}    User: {username}", ln=True)
    pdf.ln(3)

    # ── Main Result Banner ────────────────────────────────────────────────────
    pdf.set_fill_color(240, 255, 240)
    pdf.set_draw_color(46, 139, 87)
    pdf.rect(10, pdf.get_y(), 190, 22, "FD")
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(46, 139, 87)
    pdf.ln(4)
    pdf.cell(0, 10, f"  {result['plant_name']}", ln=True, align="L")
    conf = result["confidence"] * 100
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, f"  Confidence: {conf:.1f}%   |   Model: Ensemble DL", ln=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)

    # ── Plant Information ─────────────────────────────────────────────────────
    if plant_info:
        pdf.section_title("Plant Information")
        pdf.info_row("Common Name",    plant_info.get("common_name", "N/A"))
        pdf.info_row("Scientific Name",plant_info.get("scientific_name", "N/A"))
        pdf.info_row("Tamil Name",     plant_info.get("tamil_name", "N/A"))
        pdf.info_row("Hindi Name",     plant_info.get("hindi_name", "N/A"))
        pdf.info_row("Family",         plant_info.get("family", "N/A"))
        pdf.info_row("Category",       plant_info.get("category", "N/A"))
        pdf.info_row("Region",         plant_info.get("region", "N/A"))
        pdf.info_row("Availability",   plant_info.get("availability", "N/A"))
        pdf.ln(2)

        # Description
        pdf.section_title("Description")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, plant_info.get("description", ""))
        pdf.ln(2)

        # Medicinal Uses
        pdf.section_title("Medicinal Uses")
        for use in plant_info.get("medicinal_uses", []):
            pdf.bullet_item(use)
        pdf.ln(2)

        # Active Compounds
        pdf.section_title("Active Compounds")
        compounds = ", ".join(plant_info.get("active_compounds", []))
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, compounds)
        pdf.ln(2)

        # Preparation Methods
        pdf.section_title("Preparation Methods")
        for method in plant_info.get("preparation_methods", []):
            pdf.bullet_item(method)
        pdf.ln(2)

        # Safety Information
        pdf.section_title("Safety Information", color=(200, 80, 0))
        pdf.set_font("Helvetica", "B", 10)
        toxicity = plant_info.get("toxicity_level", "Unknown")
        color = (0, 150, 0) if toxicity in ["Low", "Very Low"] else (200, 0, 0)
        pdf.set_text_color(*color)
        pdf.cell(0, 7, f"  Toxicity Level: {toxicity}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, plant_info.get("safety_info", ""))
        pdf.ln(2)

        warnings = plant_info.get("warnings", [])
        if warnings:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 7, "  Warnings:", ln=True)
            pdf.set_text_color(0, 0, 0)
            for w in warnings:
                pdf.bullet_item(w)
        pdf.ln(2)

    # ── Model Performance ─────────────────────────────────────────────────────
    pdf.section_title("AI Model Analysis")
    pdf.info_row("Primary Model",   "Ensemble (VGG16 + ResNet50 + InceptionV3)")
    pdf.info_row("Confidence",      f"{result['confidence']*100:.1f}%")
    pdf.ln(2)

    if result.get("top5"):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "  Top 5 Predictions:", ln=True)
        for i, p in enumerate(result["top5"], 1):
            bar_w = int(p["confidence"] * 80)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(8,  6, f"  {i}.", ln=False)
            pdf.cell(50, 6, p["name"], ln=False)
            pdf.set_fill_color(46, 139, 87)
            pdf.rect(pdf.get_x(), pdf.get_y() + 1, bar_w, 4, "F")
            pdf.cell(bar_w + 5, 6, "", ln=False)
            pdf.cell(0, 6, f"{p['confidence']*100:.1f}%", ln=True)

    # ── Disclaimer ───────────────────────────────────────────────────────────
    pdf.ln(5)
    pdf.set_fill_color(255, 255, 220)
    pdf.set_draw_color(200, 150, 0)
    pdf.rect(10, pdf.get_y(), 190, 18, "FD")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(150, 100, 0)
    pdf.ln(2)
    pdf.multi_cell(0, 5,
        "  DISCLAIMER: This report is generated by AI for informational purposes only. "
        "Always consult a qualified botanist, Ayurvedic practitioner, or medical professional "
        "before using any medicinal plant for treatment."
    )

    return bytes(pdf.output())
