import io
import os
from weasyprint import HTML, CSS
from bidi.algorithm import get_display 
import arabic_reshaper

# Load Amiri Font explicitly
FONT_PATH = os.path.join(os.path.dirname(__file__), 'Amiri-Regular.ttf')

def format_arabic(text):
    """Reshape and apply BiDi algorithm for proper Arabic text rendering."""
    if not text: return text
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def generate_vajebaat_pdf(appointment, member, record):
    """
    Generates the official Al-Vajebaat 1447 Form using WeasyPrint and an HTML template.
    """
    its_value = member.get("its_id", "") if isinstance(member, dict) else (member.its_id if member else appointment.its_number)
    name_value = member.get("name", "") if isinstance(member, dict) else (member.full_name if member else appointment.name)
    mohalla_value = member.get("mohalla", "") if isinstance(member, dict) else (member.sector if member else "Mufaddal")
    file_value = member.get("file_no", "") if isinstance(member, dict) else (member.file_no if member else "")
    sector_value = member.get("sector", "") if isinstance(member, dict) else (member.sector if member else "")
    subsector_value = member.get("sub_sector", "") if isinstance(member, dict) else (member.sub_sector if member else "")

    zakat_mal = f"{record.zakat_mal:.2f}" if record else "0.00"
    khums = f"{record.khums:.2f}" if record else "0.00"
    nazr_muqam = f"{record.nazr_muqam:.2f}" if record else "0.00"
    kaffara = f"{record.kaffara:.2f}" if record else "0.00"
    minnat_niyaz = f"{record.minnat_niyaz:.2f}" if record else "0.00"
    najwa = f"{record.najwa:.2f}" if record else "0.00"
    jamiya = f"{record.jamiya:.2f}" if record else "0.00"
    total = f"{record.total:.2f}" if record else "0.00"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 20mm;
            }}
            @font-face {{
                font-family: 'Amiri';
                src: url('file://{FONT_PATH}') format('truetype');
            }}
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                color: #000;
                margin: 0;
                padding: 0;
            }}
            .font-arabic {{
                font-family: 'Amiri', serif;
                font-size: 1.25rem;
                margin-right: 8px;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid black;
                padding-bottom: 15px;
                margin-bottom: 25px;
            }}
            .header h1 {{
                font-size: 24px;
                margin: 0;
            }}
            .section-title {{
                font-weight: bold;
                font-size: 14px;
                margin-bottom: 15px;
            }}
            .member-grid {{
                display: table;
                width: 100%;
                margin-bottom: 30px;
                font-size: 12px;
            }}
            .member-col {{
                display: table-cell;
                width: 50%;
                padding-right: 20px;
            }}
            .member-row {{
                display: table-row;
            }}
            .member-label {{
                display: table-cell;
                font-weight: bold;
                padding-bottom: 8px;
                padding-right: 10px;
                width: 120px;
            }}
            .member-value {{
                display: table-cell;
                border-bottom: 1px dotted #888;
                padding-bottom: 8px;
            }}
            table.vajebaat-table {{
                width: 100%;
                border-collapse: collapse;
                border: 1px solid black;
                margin-bottom: 40px;
                font-size: 14px;
            }}
            .vajebaat-table th {{
                background-color: #112D4E;
                color: white;
                border: 1px solid black;
                padding: 10px 15px;
                font-weight: bold;
            }}
            .vajebaat-table td {{
                border: 1px solid black;
                padding: 10px 15px;
            }}
            .vajebaat-table th.col-1, .vajebaat-table td.col-1 {{ width: 50%; text-align: left; }}
            .vajebaat-table th.col-2, .vajebaat-table td.col-2 {{ width: 25%; text-align: center; color: #888; }}
            .vajebaat-table th.col-3, .vajebaat-table td.col-3 {{ width: 25%; text-align: right; }}
            .grand-total {{
                background-color: #f3f4f6;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                font-size: 10px;
                color: #666;
                font-style: italic;
                position: absolute;
                bottom: 0;
                width: 100%;
            }}
            .flex-item {{
                display: inline-block;
                vertical-align: middle;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Al Vajebaat 1447</h1>
        </div>
        
        <div class="section-title">Member details:</div>
        
        <div class="member-grid">
            <div class="member-col">
                <div class="member-row">
                    <div class="member-label">Mohalla:</div>
                    <div class="member-value">{mohalla_value}</div>
                </div>
                <div class="member-row">
                    <div class="member-label">Name:</div>
                    <div class="member-value">{name_value}</div>
                </div>
                <div class="member-row">
                    <div class="member-label">ITS:</div>
                    <div class="member-value">{its_value}</div>
                </div>
            </div>
            <div class="member-col">
                <div class="member-row">
                    <div class="member-label">File No:</div>
                    <div class="member-value">{file_value}</div>
                </div>
                <div class="member-row">
                    <div class="member-label">Sector Incharge:</div>
                    <div class="member-value">{sector_value}</div>
                </div>
                <div class="member-row">
                    <div class="member-label">Sub Sector Incharge:</div>
                    <div class="member-value">{subsector_value}</div>
                </div>
            </div>
        </div>
        
        <table class="vajebaat-table">
            <thead>
                <tr>
                    <th class="col-1">Vajebaat</th>
                    <th class="col-2">1446</th>
                    <th class="col-3">1447</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('زكوة المال')}</span>
                        <span class="flex-item">Zakat al-Mal</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{zakat_mal}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('الخمس')}</span>
                        <span class="flex-item">Khums</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{khums}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('نذر المقام')}</span>
                        <span class="flex-item">Nazr Muqam</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{nazr_muqam}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('الكفارة')}</span>
                        <span class="flex-item">Kaffara</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{kaffara}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('منة نياز')}</span>
                        <span class="flex-item">Minnat Niyaz</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{minnat_niyaz}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('النجوى')}</span>
                        <span class="flex-item">Najwa</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{najwa}</td>
                </tr>
                <tr>
                    <td class="col-1">
                        <span class="font-arabic">{format_arabic('الجامعة')}</span>
                        <span class="flex-item">Jamiya</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace;">{jamiya}</td>
                </tr>
                <tr class="grand-total">
                    <td class="col-1">
                        <span class="font-arabic" style="color: #112D4E;">{format_arabic('جملة روثثيه')}</span>
                        <span class="flex-item" style="text-transform: uppercase;">Grand Total</span>
                    </td>
                    <td class="col-2"></td>
                    <td class="col-3" style="font-family: monospace; font-size: 18px; font-weight: bold;">{total}</td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            Generated electronically by Sherullah Vajebaat Appointment System
        </div>
    </body>
    </html>
    """

    buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(buffer)
    buffer.seek(0)
    return buffer
