from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def gerar_relatorio_pdf(email, score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Cabeçalho de Elite
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "🛡️ CORE NEXUS - RELATÓRIO DE PERFORMANCE")
    p.line(100, 745, 500, 745)
    
    # Conteúdo do Médico
    p.setFont("Helvetica", 12)
    p.drawString(100, 710, f"Médico: {email}")
    p.drawString(100, 690, f"Data do Relatório: 02/03/2026")
    p.drawString(100, 670, f"Instituição: UNIFESP / Dante Pazzanese")
    
    # Métricas
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 630, "Métricas de Performance:")
    p.setFont("Helvetica", 12)
    p.drawString(120, 610, f"• Core Score Atual: {score} pontos")
    p.drawString(120, 590, "• Status de Revisão: Em Dia")
    p.drawString(120, 570, "• Nível de Retenção Estimado: 94%")
    
    # Rodapé
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 100, "Gerado automaticamente pelo Sistema CORE NEXUS - Medicina Baseada em Evidências.")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
