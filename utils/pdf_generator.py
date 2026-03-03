from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def gerar_pdf_sbar(dados_handoff):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "🛡️ CORE NEXUS - RELATÓRIO DE PASSAGEM DE PLANTÃO")
    p.setFont("Helvetica", 10)
    p.drawString(100, 735, f"Leito: {dados_handoff['paciente_leito']} | Data: {dados_handoff['created_at']}")
    
    # Conteúdo SBAR
    sbar = dados_handoff['sbar_json']
    y = 700
    sections = [
        ("SITUATION", sbar.get('situation', '')),
        ("BACKGROUND", sbar.get('background', '')),
        ("ASSESSMENT", sbar.get('assessment', '')),
        ("RECOMMENDATION", sbar.get('recommendation', '')),
        ("RED FLAGS", dados_handoff.get('red_flags', 'Nenhuma detectada'))
    ]
    
    for title, content in sections:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, f"{title}:")
        p.setFont("Helvetica", 11)
        # Quebra de linha simples
        text_obj = p.beginText(100, y - 15)
        text_obj.textLines(content)
        p.drawText(text_obj)
        y -= 80
        
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
