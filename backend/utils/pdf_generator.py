from fpdf import FPDF
import datetime

class DisasterReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'DRISHTI.AI - DISASTER SITUATION REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

def generate_disaster_pdf(data, output_path):
    pdf = DisasterReport()
    pdf.add_page()
    
    # Summary Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'System Summary Status:', 0, 1)
    pdf.set_font('Arial', '', 11)
    stats = data['stats']
    pdf.cell(0, 10, f"- Active Alerts: {stats['active_alert_count']}", 0, 1)
    pdf.cell(0, 10, f"- Population at Risk: {stats['total_affected_population_M']} Million", 0, 1)
    pdf.cell(0, 10, f"- AI Confidence Level: {stats['ai_accuracy_percent']}%", 0, 1)
    
    pdf.ln(5)
    
    # Active Threats Table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Active Critical Threats:', 0, 1)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, 'Type', 1)
    pdf.cell(100, 10, 'Location/Label', 1)
    pdf.cell(50, 10, 'Risk Intensity', 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 10)
    for p in data['heatmap']:
        if p['hourOffset'] == 0: # Only live data
            pdf.cell(40, 10, str(p['type']).upper(), 1)
            pdf.cell(100, 10, str(p['label']), 1)
            pdf.cell(50, 10, f"{int(p['intensity']*100)}%", 1)
            pdf.ln()
            
    pdf.output(output_path)
    return output_path