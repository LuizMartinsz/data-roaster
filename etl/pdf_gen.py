from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

def generate_pdf_report(metrics, roasts, filename):
    filepath = os.path.join('reports', filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Configurações de layout
    left_margin = 50
    right_margin = 50
    max_width = width - left_margin - right_margin
    line_height = 15
    
    # --- Cabeçalho ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, height - 50, "Data Roaster - Relatório de Qualidade")
    c.line(left_margin, height - 60, width - right_margin, height - 60)

    # --- Métricas Gerais ---
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(left_margin, y, f"Dimensões: {metrics['shape'][0]} linhas x {metrics['shape'][1]} colunas")
    c.drawString(left_margin, y - 20, f"Memória: {metrics['memory_mb']} MB")
    c.drawString(left_margin, y - 40, f"Duplicatas: {metrics['duplicates']}")
    
    y -= 70 
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y, "Integridade (Nulos por Coluna):")
    y -= 20
    
    c.setFont("Helvetica", 10)
    if 'null_percent' in metrics and metrics['null_percent']:
        for col, pct in metrics['null_percent'].items():
            # Verifica quebra de página
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            marker = " (!)" if pct > 0 else ""
            c.drawString(left_margin + 10, y, f"- {col}: {pct}%{marker}")
            y -= line_height
    else:
        c.drawString(left_margin + 10, y, "Nenhuma informação de nulos disponível.")
        y -= line_height

    y -= 20 # Espaço antes do Roast
    if y < 80:
        c.showPage()
        y = height - 50
        
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y, "O Veredito (Roast):")
    y -= 30
    
    c.setFont("Helvetica", 10)
    for roast in roasts:
        text = f"- {roast}"
        # Quebra o texto para não cortar na lateral
        lines = simpleSplit(text, "Helvetica", 10, max_width)
        
        for line in lines:
            if y < 50: 
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            
            c.drawString(left_margin, y, line)
            y -= line_height
            
        y -= 10 # Espaço extra entre parágrafos

    c.save()
    return filepath 