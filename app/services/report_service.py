# app/services/report_service.py

from io import BytesIO
from datetime import datetime
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from app.models.db import Reservation, User
from app.extensions import db

class ReportService:

    @staticmethod
    def fetch_reservation_data():
        query = (
            db.session.query(
                Reservation.id.label('ID'),
                Reservation.reservation_date.label('Fecha'),
                Reservation.reservation_time.label('Hora'),
                User.username.label('Usuario')
            )
            .join(User, User.id == Reservation.customer_id)
            .order_by(Reservation.created_at)
            .all()
        )
        return [row._asdict() for row in query]

    @staticmethod
    def create_excel(data):
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Reservas', index=False)
        output.seek(0)
        return output

    @staticmethod
    def create_pdf(data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, title="Reporte de Reservas")
        styles = getSampleStyleSheet()
        elems = []

        # Título
        elems.append(Paragraph("Reporte de Reservas", styles['Heading1']))
        elems.append(Spacer(1, 12))
        # Fecha de generación
        elems.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elems.append(Spacer(1, 24))

        if data:
            # Construir tabla: encabezados + filas
            header = list(data[0].keys())
            rows = [header] + [list(d.values()) for d in data]
            table = Table(rows, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ]))
            elems.append(table)
        else:
            elems.append(Paragraph("No hay datos de reservas.", styles['Normal']))

        doc.build(elems)
        buffer.seek(0)
        return buffer
