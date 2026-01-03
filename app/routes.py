from flask import Blueprint, render_template, request, send_file
import pandas as pd
from werkzeug.utils import secure_filename
import os
import uuid
from etl.roaster import DataRoaster
from etl.pdf_gen import generate_pdf_report

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    report = None
    roast_list = []
    pdf_link = None
    error = None

    if request.method == 'POST':
        try:
            file = request.files.get('file')
            if not file or file.filename == '':
                raise ValueError("Nenhum arquivo selecionado.")

            filename = secure_filename(file.filename)
            
            # Leitura Agnóstica (Excel ou CSV)
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Formato não suportado. Use CSV ou Excel.")

            # Processamento
            roaster = DataRoaster(df)
            report = roaster.analyze()
            roast_list = roaster.get_roast()

            # Gera PDF
            pdf_name = f"report_{uuid.uuid4().hex[:8]}.pdf"
            generate_pdf_report(report, roast_list, pdf_name)
            pdf_link = pdf_name

        except Exception as e:
            error = str(e)

    return render_template('dashboard.html', report=report, roast=roast_list, pdf_link=pdf_link, error=error)

@bp.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(os.getcwd(), 'reports', filename)
    return send_file(path, as_attachment=True)