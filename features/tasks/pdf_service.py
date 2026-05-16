import io
import logging
from datetime import datetime, timezone

from flask import render_template
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)


def render_pdf(template_name: str, **context) -> bytes:
    html = render_template(template_name, **context)
    buf = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buf)
    if pisa_status.err:
        logger.error("PDF generation failed for %s", template_name)
        return b""
    buf.seek(0)
    pdf_bytes = buf.read()
    logger.info(
        "PDF generated: template=%s size=%d bytes",
        template_name,
        len(pdf_bytes),
    )
    return pdf_bytes


def export_task_report(org_name: str, tasks: list, generated_by: str) -> bytes:
    context = {
        "org_name": org_name,
        "tasks": tasks,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "generated_by": generated_by,
        "total": len(tasks),
        "done_count": sum(1 for t in tasks if t.status == "done"),
        "in_progress_count": sum(1 for t in tasks if t.status == "in_progress"),
        "todo_count": sum(1 for t in tasks if t.status == "todo"),
        "urgent_count": sum(1 for t in tasks if t.priority == "urgent"),
    }
    return render_pdf("tasks/pdf_report.html", **context)
