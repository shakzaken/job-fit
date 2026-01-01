from src.models.output_report import OutPutReport, MatchResults, CategoryScore
import os
from datetime import datetime


def write_output_mdfile(output_report: OutPutReport, output_path: str) -> None:
    """
    Write a Markdown file summarizing the job fit report.

    Sections:
    - Header with timestamp
    - Base match results
    - Final match results
    """
    def render_match_results(title: str, mr: MatchResults) -> str:
        lines: list[str] = []
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"- Overall fit score: **{mr.fit_score_overall}/100**")
        lines.append("")
        if mr.fit_score_by_category:
            lines.append("### Fit score by category")
            lines.append("")
            lines.append("| Category | Score |")
            lines.append("|---|---|")
            for cs in mr.fit_score_by_category:
                lines.append(f"| {cs.category_name} | {cs.score} |")
            lines.append("")
        if mr.missing_keywords:
            lines.append("### Missing keywords")
            lines.append("")
            lines.append(", ".join(mr.missing_keywords))
            lines.append("")
        if mr.evidence:
            lines.append("### Evidence")
            lines.append("")
            lines.append(mr.evidence.strip())
            lines.append("")
        return "\n".join(lines)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    parts: list[str] = []
    parts.append("# Job Fit Report")
    parts.append("")
    parts.append(f"_Generated at: {created_at}_")
    parts.append("")

    # Base and Final sections
    parts.append(render_match_results("Base Match Results", output_report.base_match_result))
    parts.append(render_match_results("Final Match Results", output_report.final_match_result))

    content = "\n".join(parts).rstrip() + "\n"

    # Write the file (sync write inside async is acceptable for small outputs)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
