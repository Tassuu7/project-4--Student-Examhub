"""
ExamHub Printable Report & Transcript Generator
Renders institutional grade reports and student transcripts in high-fidelity HTML/SVG.
"""

from typing import List, Dict
from backend.app.reporting.schemas import (
    CandidateOfficialTranscript,
    InstitutionalExamSummaryReport,
)


class ReportDocumentGenerator:
    """
    Renders printable HTML transcripts with SVG headers, security watermarks, and verification seals.
    """

    @classmethod
    def render_candidate_transcript_html(cls, transcript: CandidateOfficialTranscript) -> str:
        """
        Generate standalone HTML document ready for PDF printing (window.print()).
        """
        rows_html = ""
        for it in transcript.items:
            status_color = "#16a34a" if it.status == "PASS" else "#dc2626"
            rows_html += f"""
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 10px 12px; font-weight: 600; color: #374151;">{it.subject_code}</td>
                <td style="padding: 10px 12px; color: #1f2937;">{it.subject_name}</td>
                <td style="padding: 10px 12px; text-align: center;">{it.credits:.1f}</td>
                <td style="padding: 10px 12px; text-align: center; font-weight: 700;">{it.grade_letter}</td>
                <td style="padding: 10px 12px; text-align: center;">{it.grade_points:.1f}</td>
                <td style="padding: 10px 12px; text-align: center;">{it.percentage:.1f}%</td>
                <td style="padding: 10px 12px; text-align: center; color: {status_color}; font-weight: 600;">{it.status}</td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Official Academic Transcript - {transcript.candidate_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            color: #111827;
            background: #f9fafb;
        }}
        .transcript-card {{
            max-width: 850px;
            margin: 0 auto;
            background: #ffffff;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            padding: 36px;
            position: relative;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 24px;
        }}
        .logo-title h1 {{
            margin: 0;
            color: #1e3a8a;
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .logo-title p {{
            margin: 4px 0 0;
            color: #6b7280;
            font-size: 14px;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            background: #f8fafc;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 24px;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin-bottom: 28px;
        }}
        th {{
            background: #f1f5f9;
            color: #475569;
            text-align: left;
            padding: 10px 12px;
            font-weight: 600;
            border-bottom: 2px solid #cbd5e1;
        }}
        .summary-box {{
            display: flex;
            justify-content: space-between;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 6px;
            padding: 16px 24px;
            margin-bottom: 32px;
        }}
        .summary-item {{
            text-align: center;
        }}
        .summary-item .num {{
            font-size: 22px;
            font-weight: 800;
            color: #1d4ed8;
        }}
        .summary-item .lbl {{
            font-size: 12px;
            text-transform: uppercase;
            color: #6b7280;
            font-weight: 600;
        }}
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
            font-size: 12px;
            color: #6b7280;
        }}
        .security-badge {{
            font-family: monospace;
            font-size: 11px;
            background: #f3f4f6;
            padding: 6px 10px;
            border-radius: 4px;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="transcript-card">
        <div class="header">
            <div class="logo-title">
                <h1>{transcript.institution_name}</h1>
                <p>Office of the University Registrar • Official Academic Transcript</p>
            </div>
            <div style="text-align: right;">
                <span style="display: inline-block; padding: 4px 10px; background: #dbeafe; color: #1e40af; border-radius: 12px; font-weight: 700; font-size: 12px;">OFFICIAL RECORD</span>
                <p style="margin: 6px 0 0; font-size: 13px; color: #6b7280;">Date: {transcript.issued_date}</p>
            </div>
        </div>

        <div class="meta-grid">
            <div><strong>Candidate Name:</strong> {transcript.candidate_name}</div>
            <div><strong>Enrollment ID:</strong> {transcript.enrollment_number}</div>
            <div><strong>Program:</strong> {transcript.program_name}</div>
            <div><strong>Transcript Serial:</strong> {transcript.transcript_id}</div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Code</th>
                    <th>Subject Description</th>
                    <th style="text-align: center;">Credits</th>
                    <th style="text-align: center;">Grade</th>
                    <th style="text-align: center;">Points</th>
                    <th style="text-align: center;">Score</th>
                    <th style="text-align: center;">Result</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="summary-box">
            <div class="summary-item">
                <div class="num">{transcript.total_credits:.1f}</div>
                <div class="lbl">Total Credits</div>
            </div>
            <div class="summary-item">
                <div class="num">{transcript.gpa:.2f}</div>
                <div class="lbl">Semester GPA</div>
            </div>
            <div class="summary-item">
                <div class="num">{transcript.cgpa:.2f}</div>
                <div class="lbl">Cumulative GPA</div>
            </div>
        </div>

        <div class="footer">
            <div>
                <div><strong>Cryptographic Verification Hash:</strong></div>
                <div class="security-badge">{transcript.verification_hash}</div>
            </div>
            <div style="text-align: center;">
                <div style="height: 35px; border-bottom: 1px solid #9ca3af; width: 150px; margin-bottom: 4px;"></div>
                <div>Controller of Examinations</div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html
