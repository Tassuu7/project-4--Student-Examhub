"""
ExamHub Notification Template Compiler
Interpolates variables, handles conditional statements, and applies localized formatting.
"""

import re
from typing import Dict, Any, Optional
from backend.app.notifications_engine.schemas import NotificationTemplate


class TemplateCompiler:
    """
    Safely compiles text and HTML templates without external dependency on heavy templating engines.
    """

    VAR_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")
    COND_REGEX = re.compile(r"\{%\s*if\s+([a-zA-Z0-9_]+)\s*%\}(.*?)\{%\s*endif\s*%\}", re.DOTALL)

    @classmethod
    def render(cls, template_string: str, context: Dict[str, Any]) -> str:
        """
        Renders template with variables and simple conditional blocks.
        """
        # Process conditionals: {% if var %} content {% endif %}
        def replace_cond(match):
            var_name = match.group(1).strip()
            block_content = match.group(2)
            if context.get(var_name):
                return block_content
            return ""

        processed = cls.COND_REGEX.sub(replace_cond, template_string)

        # Process variable substitutions: {{ var }}
        def replace_var(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, f"[{var_name}]"))

        rendered = cls.VAR_REGEX.sub(replace_var, processed)
        return rendered.strip()

    @classmethod
    def get_standard_templates(cls) -> Dict[str, NotificationTemplate]:
        """Built-in templates for common academic lifecycle events."""
        return {
            "exam_reminder_en": NotificationTemplate(
                template_id="tpl-rem-01",
                event_type="exam_reminder",
                language_code="en",
                subject="Reminder: Your examination '{{ exam_title }}' begins in {{ time_left }}",
                body_text="Dear {{ student_name }},\n\nThis is a scheduled reminder that your exam '{{ exam_title }}' is scheduled to start at {{ start_time }}.\n\nPlease ensure your camera and microphone are configured. Link: {{ exam_url }}\n\nRegards,\nExam Administration",
                body_html="<p>Dear {{ student_name }},</p><p>This is a scheduled reminder that your exam <strong>{{ exam_title }}</strong> starts at {{ start_time }}.</p><p><a href='{{ exam_url }}'>Enter Exam Room</a></p>"
            ),
            "score_released_en": NotificationTemplate(
                template_id="tpl-score-01",
                event_type="score_released",
                language_code="en",
                subject="Grades Published: {{ exam_title }} Scorecard Available",
                body_text="Dear {{ student_name }},\n\nYour score for '{{ exam_title }}' has been finalized.\n\nScore: {{ final_score }}%\nStatus: {{ pass_fail_status }}\n\nView official certificate: {{ certificate_url }}\n\nExamHub Registrar",
                body_html="<p>Dear {{ student_name }},</p><p>Your grade for <strong>{{ exam_title }}</strong> is now available.</p><p>Score: <strong>{{ final_score }}%</strong> ({{ pass_fail_status }})</p><p><a href='{{ certificate_url }}'>View Certificate</a></p>"
            ),
            "proctor_flag_en": NotificationTemplate(
                template_id="tpl-proc-01",
                event_type="proctor_flag",
                language_code="en",
                subject="URGENT: Proctoring Anomaly Flagged on Candidate {{ candidate_name }}",
                body_text="Invigilator Alert: Candidate {{ candidate_name }} in exam {{ exam_title }} has triggered an anomaly flag: {{ anomaly_description }}.\n\nIntegrity Score: {{ trust_score }}%.\n\nLive stream: {{ proctor_console_url }}",
                body_html="<p><strong>Invigilator Alert:</strong> Candidate {{ candidate_name }} triggered: {{ anomaly_description }}.</p><p>Current Trust Score: {{ trust_score }}%</p><p><a href='{{ proctor_console_url }}'>Open Live Console</a></p>"
            )
        }
