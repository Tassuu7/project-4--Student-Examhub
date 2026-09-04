"""
ExamHub - Certificate Visual Layout & Document Generator
Renders publication-quality HTML & SVG certificates with formal typography,
guilloche borders, security crests, and verification QR/barcode indicators.
"""

from typing import Dict, Any

class CertificateGenerator:
    """HTML and SVG template rendering engine for academic credentials."""

    @staticmethod
    def render_html_certificate(cert_data: Dict[str, Any]) -> str:
        """Renders self-contained responsive and print-ready HTML certificate."""
        student_name = cert_data.get("student_name", "Student")
        roll_number = cert_data.get("roll_number", "N/A")
        exam_name = cert_data.get("exam_name", "Comprehensive Examination")
        subject_name = cert_data.get("subject_name", "Curriculum Subject")
        subject_code = cert_data.get("subject_code", "SUB101")
        grade = cert_data.get("grade", "Pass")
        percentage = cert_data.get("percentage", 0.0)
        cert_code = cert_data.get("certificate_code", "EXAM-0000-0000")
        issue_date = cert_data.get("issue_date", "")[:10]
        verification_hash = cert_data.get("verification_hash", "")[:16]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Certificate of Achievement - {student_name}</title>
    <style>
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
        body {{
            margin: 0;
            padding: 40px;
            background-color: #f8fafc;
            font-family: 'Georgia', serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            box-sizing: border-box;
        }}
        .certificate-frame {{
            width: 1050px;
            height: 720px;
            background: #ffffff;
            border: 12px double #1e293b;
            padding: 30px;
            box-shadow: 0 20px 30px rgba(0,0,0,0.12);
            position: relative;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
        }}
        .inner-border {{
            border: 2px solid #b45309;
            height: 100%;
            padding: 30px 40px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .header {{
            margin-top: 10px;
        }}
        .crest {{
            font-size: 32px;
            color: #b45309;
            margin-bottom: 5px;
        }}
        .institution-title {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: #475569;
            font-weight: 700;
        }}
        .main-heading {{
            font-size: 38px;
            font-weight: bold;
            color: #0f172a;
            margin: 15px 0 5px 0;
            letter-spacing: 1px;
        }}
        .subtitle {{
            font-size: 16px;
            color: #64748b;
            font-style: italic;
        }}
        .recipient-section {{
            margin: 25px 0 15px 0;
        }}
        .recipient-name {{
            font-size: 36px;
            font-weight: bold;
            color: #b45309;
            border-bottom: 2px solid #cbd5e1;
            display: inline-block;
            padding: 0 40px 6px 40px;
            margin-bottom: 8px;
        }}
        .recipient-id {{
            font-family: monospace;
            font-size: 13px;
            color: #64748b;
        }}
        .achievement-text {{
            font-size: 16px;
            line-height: 1.6;
            color: #334155;
            max-width: 800px;
            margin: 0 auto;
        }}
        .course-title {{
            font-weight: bold;
            color: #0f172a;
        }}
        .meta-badges {{
            display: flex;
            justify-content: center;
            gap: 24px;
            margin: 20px 0;
        }}
        .badge {{
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 8px 18px;
            border-radius: 8px;
            font-family: sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #1e293b;
        }}
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }}
        .signature-block {{
            width: 220px;
            text-align: center;
        }}
        .signature-line {{
            border-bottom: 1.5px solid #475569;
            margin-bottom: 6px;
            height: 40px;
        }}
        .signature-title {{
            font-family: sans-serif;
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            font-weight: bold;
        }}
        .seal-center {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .seal-circle {{
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 3px double #b45309;
            background: #fef3c7;
            color: #92400e;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        .verification-code {{
            font-family: monospace;
            font-size: 11px;
            color: #475569;
            letter-spacing: 1px;
        }}
        .print-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #b45309;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 13px;
        }}
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; background: none; }}
            .certificate-frame {{ box-shadow: none; border-width: 8px; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">Print / Save PDF</button>

    <div class="certificate-frame">
        <div class="inner-border">
            <div class="header">
                <div class="crest">&#10022; &#10022; &#10022;</div>
                <div class="institution-title">ExamHub Academic Certification Board</div>
                <div class="main-heading">Certificate of Achievement</div>
                <div class="subtitle">This academic credential is formally awarded to</div>
            </div>

            <div class="recipient-section">
                <div class="recipient-name">{student_name}</div>
                <div class="recipient-id">Student Roll Identification: {roll_number}</div>
            </div>

            <div class="achievement-text">
                For successfully fulfilling all examination criteria and demonstrating verified competence in
                <span class="course-title">{exam_name}</span> ({subject_code} &mdash; {subject_name}),
                conducted under continuous proctored examination protocols.
            </div>

            <div class="meta-badges">
                <div class="badge">Grade Achieved: {grade}</div>
                <div class="badge">Assessment Score: {percentage:.1f}%</div>
                <div class="badge">Issued: {issue_date}</div>
            </div>

            <div class="footer">
                <div class="signature-block">
                    <div class="signature-line"></div>
                    <div class="signature-title">Academic Director</div>
                </div>

                <div class="seal-center">
                    <div class="seal-circle">VERIFIED</div>
                    <div class="verification-code">{cert_code}</div>
                    <div style="font-size: 9px; color: #94a3b8; font-family: monospace;">Hash: {verification_hash}</div>
                </div>

                <div class="signature-block">
                    <div class="signature-line"></div>
                    <div class="signature-title">Chief Proctor</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html
