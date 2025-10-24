from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_invoice_detail_pdf(invoice_data):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Contenedor de elementos
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    normal_style = styles['Normal']

    # Titulo
    title = Paragraph("FACTURA DETALLADA", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Informacion de la empresa
    company_data = [
        ["Tecnologías Chapinas, S.A."],
        ["Sistema de Facturación de Nube"],
        ["Guatemala, Guatemala"],
    ]
    company_table = Table(company_data, colWidths=[6*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 20))

    # Informacion de la factura
    invoice = invoice_data.get('invoice', {})
    invoice_info_data = [
        ["No. Factura:", invoice.get('id', 'N/A')],
        ["Fecha:", invoice.get('date', 'N/A')],
        ["NIT Cliente:", invoice.get('nit', 'N/A')],
    ]
    invoice_info_table = Table(invoice_info_data, colWidths=[2*inch, 4*inch])
    invoice_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(invoice_info_table)
    elements.append(Spacer(1, 20))

    # Informacion del cliente
    client = invoice_data.get('client', {})
    elements.append(Paragraph("DATOS DEL CLIENTE", heading_style))
    client_data = [
        ["Nombre:", client.get('name', 'N/A')],
        ["NIT:", client.get('nit', 'N/A')],
        ["Dirección:", client.get('address', 'N/A')],
        ["Email:", client.get('email', 'N/A')],
    ]
    client_table = Table(client_data, colWidths=[1.5*inch, 4.5*inch])
    client_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(client_table)
    elements.append(Spacer(1, 20))

    # Detalle de instancias y recursos
    elements.append(Paragraph("DETALLE DE CONSUMO", heading_style))

    instances = invoice_data.get('instances', [])
    grand_total = 0.0

    for instance in instances:
        # Encabezado de instancia
        instance_header = Paragraph(
            f"<b>Instancia:</b> {instance.get('instance_name', 'N/A')} (ID: {instance.get('instance_id', 'N/A')})", normal_style)
        elements.append(instance_header)
        elements.append(Spacer(1, 6))

        # Tabla de recursos de la instancia
        resources = instance.get('resources', [])
        if resources:
            resource_data = [["Recurso", "Cantidad",
                              "Costo/Hora", "Horas", "Subtotal"]]

            for resource in resources:
                resource_data.append([
                    resource.get('name', 'N/A'),
                    str(resource.get('quantity', 0)),
                    f"${resource.get('cost_per_hour', 0.0):.2f}",
                    f"{resource.get('hours', 0.0):.2f}",
                    f"${resource.get('amount', 0.0):.2f}"
                ])

            resource_table = Table(resource_data, colWidths=[
                                   2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            resource_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ]))
            elements.append(resource_table)

        # Subtotal de la instancia
        instance_subtotal = instance.get('subtotal', 0.0)
        grand_total += instance_subtotal
        subtotal_text = Paragraph(f"<b>Subtotal Instancia: ${instance_subtotal:.2f}</b>",
                                  ParagraphStyle('right', parent=normal_style, alignment=TA_RIGHT))
        elements.append(Spacer(1, 6))
        elements.append(subtotal_text)
        elements.append(Spacer(1, 12))

    # Total general
    elements.append(Spacer(1, 20))
    total_data = [
        ["", "", "", "TOTAL A PAGAR:", f"${grand_total:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[
                        2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
        ('ALIGN', (4, 0), (4, 0), 'CENTER'),
        ('FONTNAME', (3, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (3, 0), (-1, 0), 12),
        ('TEXTCOLOR', (3, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('BACKGROUND', (4, 0), (4, 0), colors.HexColor('#e0e7ff')),
        ('BOX', (4, 0), (4, 0), 2, colors.HexColor('#1e40af')),
    ]))
    elements.append(total_table)

    # Pie de pagina
    elements.append(Spacer(1, 40))
    footer_text = Paragraph(
        "Gracias por confiar en Tecnologías Chapinas, S.A.<br/>Este documento es una representación impresa de una factura electrónica.",
        ParagraphStyle('footer', parent=normal_style,
                       alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    )
    elements.append(footer_text)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_sales_analysis_pdf(analysis_data, analysis_type):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Titulo
    report_title = "ANÁLISIS DE VENTAS POR CATEGORÍAS/CONFIGURACIONES" if analysis_type == 'categories' else "ANÁLISIS DE VENTAS POR RECURSOS"
    title = Paragraph(report_title, title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Informacion de la empresa
    company_data = [
        ["Tecnologías Chapinas, S.A."],
        ["Reporte de Análisis de Ventas"],
        [f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"],
    ]
    company_table = Table(company_data, colWidths=[6*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 20))

    # Periodo de analisis
    date_range = analysis_data.get('date_range', {})
    period_data = [
        ["Período de Análisis:"],
        [f"Desde: {date_range.get('start', 'N/A')} - Hasta: {date_range.get('end', 'N/A')}"]
    ]
    period_table = Table(period_data, colWidths=[6*inch])
    period_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(period_table)
    elements.append(Spacer(1, 20))

    # Tabla de analisis
    elements.append(Paragraph("RESULTADOS DEL ANÁLISIS", heading_style))

    items = analysis_data.get('items', [])
    if items:
        # Encabezado segun tipo
        if analysis_type == 'categories':
            table_data = [["Categoría/Configuración",
                           "Descripción", "Ingresos", "% del Total"]]
        else:
            table_data = [["Recurso", "Tipo", "Ingresos", "% del Total"]]

        # Filas de datos
        for item in items:
            table_data.append([
                item.get('name', 'N/A'),
                item.get('description', 'N/A'),
                f"${item.get('revenue', 0.0):.2f}",
                f"{item.get('percentage', 0.0):.1f}%"
            ])

        # Crear tabla
        analysis_table = Table(table_data, colWidths=[
                               2.5*inch, 2*inch, 1*inch, 1*inch])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        elements.append(analysis_table)
    else:
        no_data_text = Paragraph(
            "No se encontraron datos para el período seleccionado.", styles['Normal'])
        elements.append(no_data_text)

    # Total de ingresos
    elements.append(Spacer(1, 20))
    total_revenue = analysis_data.get('total_revenue', 0.0)
    total_data = [
        ["TOTAL DE INGRESOS:", f"${total_revenue:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[4.5*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#e0e7ff')),
        ('BOX', (1, 0), (1, 0), 2, colors.HexColor('#1e40af')),
    ]))
    elements.append(total_table)

    # Pie de pagina
    elements.append(Spacer(1, 40))
    footer_text = Paragraph(
        f"Reporte generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}<br/>Tecnologías Chapinas, S.A. - Todos los derechos reservados",
        ParagraphStyle(
            'footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    )
    elements.append(footer_text)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
