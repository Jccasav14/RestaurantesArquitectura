from flask import Blueprint, send_file, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.services.report_service import ReportService

report_bp = Blueprint('admin_report', __name__, url_prefix='/admin/report')

@report_bp.route('/<fmt>')
@login_required
def generate_report(fmt):
    if current_user.role != 'admin':
        abort(403)

    data = ReportService.fetch_reservation_data()
    if fmt == 'excel':
        buf = ReportService.create_excel(data)
        return send_file(
            buf,
            as_attachment=True,
            download_name=f"reservas_{datetime.today().strftime('%Y%m%d')}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    elif fmt == 'pdf':
        buf = ReportService.create_pdf(data)
        return send_file(
            buf,
            as_attachment=True,
            download_name=f"reservas_{datetime.today().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )
    else:
        abort(404)
