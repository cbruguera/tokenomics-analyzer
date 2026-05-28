#!/usr/bin/env python3
"""
Auric Labs PDF report generator.
Usage: python templates/generate_pdf.py <token-name>
Run from the agent/ directory.
"""

import sys
import re
import base64
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.resolve()
AGENT_DIR = SCRIPT_DIR.parent.resolve()

GRADE_COLORS = {
    'A': '#16a34a', 'B': '#65a30d', 'C': '#ca8a04', 'D': '#ea580c', 'F': '#dc2626'
}

SEVERITY_COLORS = {
    'CRITICAL':      '#dc2626',
    'HIGH':          '#ea580c',
    'MEDIUM':        '#ca8a04',
    'LOW':           '#2563eb',
    'INFORMATIONAL': '#6b7280',
}


def parse_metadata(text):
    grade_m = re.search(r'\*\*Audit Grade:\*\*\s*([A-F])', text)
    name_m  = re.search(r'# Token Audit Report:\s*(.+?)\s*\((\w+)\)', text)
    date_m  = re.search(r'\*\*Date:\*\*\s*(.+)', text)
    grade   = grade_m.group(1) if grade_m else '?'
    return {
        'token_name':   name_m.group(1).strip() if name_m else 'Unknown Token',
        'token_symbol': name_m.group(2).strip() if name_m else '???',
        'grade':        grade,
        'grade_color':  GRADE_COLORS.get(grade, '#6b7280'),
        'audit_date':   date_m.group(1).strip() if date_m else datetime.today().strftime('%Y-%m-%d'),
    }


def strip_front_matter(text):
    """Return report body starting from the first ## section."""
    m = re.search(r'^(## .+)', text, re.MULTILINE)
    if m:
        return text[m.start():]
    parts = text.split('\n---\n', 1)
    return parts[1] if len(parts) > 1 else text


def embed_images(html, analysis_dir):
    """Replace PNG src paths with inline base64 data URIs."""
    def replace(m):
        src = m.group(1)
        candidates = [
            analysis_dir / Path(src).name,
            (AGENT_DIR / src.lstrip('../').lstrip('/')).resolve(),
        ]
        for p in candidates:
            try:
                if p.resolve().exists():
                    b64 = base64.b64encode(p.read_bytes()).decode()
                    return f'src="data:image/png;base64,{b64}"'
            except Exception:
                continue
        return m.group(0)
    return re.sub(r'src="([^"]+\.png)"', replace, html)


def severity_badge(severity, color):
    return (
        f'<span style="display:inline-block;background:{color};color:#fff;'
        f'padding:1px 7px;border-radius:3px;font-size:0.66em;font-weight:700;'
        f'letter-spacing:0.07em;vertical-align:middle;margin-right:6px;">'
        f'{severity}</span>'
    )


def style_findings(html):
    """Add colored left border and severity badge to each finding header."""
    for sev, color in SEVERITY_COLORS.items():
        pattern = re.compile(
            rf'<h3>((?:[^<]|\s)*\[{sev}[^\]]*\][^<]*)</h3>',
            re.IGNORECASE
        )
        repl = (
            f'<h3 style="border-left:4px solid {color};padding-left:12px;'
            f'margin-top:2.2em;padding-top:3px;padding-bottom:3px;">'
            f'{severity_badge(sev, color)}\\1</h3>'
        )
        html = pattern.sub(repl, html)
    return html


def build_toc(toc_tokens):
    """Build ToC HTML from H2-level sections only."""
    import html as html_lib
    items = []
    for t in toc_tokens:
        if t['level'] == 2:
            name = html_lib.unescape(t['name'])
            items.append(
                f'<div class="toc-item">'
                f'<a class="toc-link" href="#{t["id"]}">{name}</a>'
                f'</div>'
            )
    return '\n'.join(items)


def main():
    if len(sys.argv) < 2:
        print("Usage: python templates/generate_pdf.py <token-name>")
        sys.exit(1)

    token_slug   = sys.argv[1].lower().strip()
    report_md    = AGENT_DIR / 'reports'  / f'{token_slug}_audit.md'
    analysis_dir = AGENT_DIR / 'analysis' / token_slug
    output_pdf   = AGENT_DIR / 'reports'  / f'{token_slug}_audit.pdf'
    template     = SCRIPT_DIR / 'pdf_report.html.j2'

    if not report_md.exists():
        print(f"Error: {report_md} not found")
        sys.exit(1)

    import markdown as md_lib
    from jinja2 import Template
    from weasyprint import HTML

    text    = report_md.read_text(encoding='utf-8')
    meta    = parse_metadata(text)
    body_md = strip_front_matter(text)

    md      = md_lib.Markdown(extensions=['extra', 'toc'])
    content_html = md.convert(body_md)
    toc_html     = build_toc(md.toc_tokens)

    if analysis_dir.exists():
        content_html = embed_images(content_html, analysis_dir)
    content_html = style_findings(content_html)

    full_html = Template(template.read_text()).render(
        **meta, content=content_html, toc_html=toc_html
    )
    HTML(string=full_html, base_url=str(AGENT_DIR)).write_pdf(str(output_pdf))
    print(f"PDF written: {output_pdf}")


if __name__ == '__main__':
    main()
