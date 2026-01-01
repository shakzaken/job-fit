import os
import fitz  # PyMuPDF
import json

from src.models.resume_profile import ResumeProfile


def convert_resume_pdf_to_str(resume_path: str) -> str:
    """
    Read a PDF and return its text content as a single string.
    Uses PyMuPDF (fast, accurate on most PDFs).
    """


    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"PDF not found: {resume_path}")

    with fitz.open(resume_path) as doc:
        if getattr(doc, "needs_pass", False):
            raise ValueError("PDF is password-protected.")

        parts: list[str] = []
        for page in doc:
            # "text" provides a readable flow for most documents
            parts.append(page.get_text("text"))

    # Normalize trailing spaces and return
    text = "\n".join(parts)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def write_resume_profile_to_pdf(resume_profile: ResumeProfile, output_path: str) -> None:
    """
    Write a ResumeProfile object to a formatted PDF file.
    Uses PyMuPDF to create a professional-looking resume.
    """
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # Letter size (8.5" x 11")

    # Define formatting constants
    margin_left = 50
    margin_right = 562
    y_position = 50
    line_height = 15

    # Font sizes
    title_size = 16
    heading_size = 14
    subheading_size = 11
    body_size = 10

    def add_text(text: str, x: float, y: float, size: float, bold: bool = False) -> float:
        """Add text to the page and return the new y position."""
        font = "helv" if not bold else "hebo"
        page.insert_text((x, y), text, fontsize=size, fontname=font)
        return y + size + 5

    def add_multiline_text(text: str, x: float, y: float, size: float, max_width: float, bold: bool = False) -> float:
        """Add text with word wrapping and return the new y position."""
        font = "helv" if not bold else "hebo"
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            text_width = fitz.get_text_length(test_line, fontname=font, fontsize=size)
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        for line in lines:
            page.insert_text((x, y), line, fontsize=size, fontname=font)
            y += line_height

        return y

    def check_page_space(current_y: float, needed_space: float = 100) -> tuple:
        """Check if we need a new page and return (page, y_position)."""
        nonlocal page, y_position
        if current_y + needed_space > 750:  # Near bottom of page
            page = doc.new_page(width=612, height=792)
            return page, 50
        return page, current_y

    # Contact Information
    y_position = add_text(resume_profile.contact, margin_left, y_position, body_size)
    y_position += 10

    # Summary Section
    if resume_profile.summary:
        page, y_position = check_page_space(y_position)
        y_position = add_text("PROFESSIONAL SUMMARY", margin_left, y_position, heading_size, bold=True)
        y_position = add_multiline_text(
            resume_profile.summary,
            margin_left,
            y_position,
            body_size,
            margin_right - margin_left
        )
        y_position += 10

    # Skills Section
    page, y_position = check_page_space(y_position)
    y_position = add_text("SKILLS", margin_left, y_position, heading_size, bold=True)
    skills_text = " • ".join(resume_profile.skills)
    y_position = add_multiline_text(
        skills_text,
        margin_left,
        y_position,
        body_size,
        margin_right - margin_left
    )
    y_position += 10

    # Experience Section
    page, y_position = check_page_space(y_position)
    y_position = add_text("EXPERIENCE", margin_left, y_position, heading_size, bold=True)

    for exp in resume_profile.experiences:
        page, y_position = check_page_space(y_position, 80)

        # Company and Role
        y_position = add_text(f"{exp.company} - {exp.role}", margin_left, y_position, subheading_size, bold=True)

        # Dates
        start = exp.start_date.strftime("%b %Y")
        end = "Present" if exp.end_date.year == 9999 else exp.end_date.strftime("%b %Y")
        y_position = add_text(f"{start} - {end}", margin_left, y_position, body_size)

        # Bullets
        for bullet in exp.bullets:
            page, y_position = check_page_space(y_position)
            bullet_text = f"• {bullet.content}"
            y_position = add_multiline_text(
                bullet_text,
                margin_left + 10,
                y_position,
                body_size,
                margin_right - margin_left - 10
            )

        # Technologies
        if exp.technologies:
            tech_text = f"Technologies: {', '.join(exp.technologies)}"
            y_position = add_multiline_text(
                tech_text,
                margin_left + 10,
                y_position,
                body_size,
                margin_right - margin_left - 10
            )

        y_position += 10

    # Projects Section
    if resume_profile.projects:
        page, y_position = check_page_space(y_position)
        y_position = add_text("PROJECTS", margin_left, y_position, heading_size, bold=True)

        for project in resume_profile.projects:
            page, y_position = check_page_space(y_position, 60)

            # Project name
            y_position = add_text(project.name, margin_left, y_position, subheading_size, bold=True)

            # Technologies
            tech_text = f"Technologies: {', '.join(project.technologies)}"
            y_position = add_multiline_text(
                tech_text,
                margin_left + 10,
                y_position,
                body_size,
                margin_right - margin_left - 10
            )

            # Description
            y_position = add_multiline_text(
                project.description,
                margin_left + 10,
                y_position,
                body_size,
                margin_right - margin_left - 10
            )
            y_position += 5

    # Education Section
    page, y_position = check_page_space(y_position)
    y_position = add_text("EDUCATION", margin_left, y_position, heading_size, bold=True)
    y_position = add_text(resume_profile.education.school_name, margin_left, y_position, subheading_size, bold=True)
    y_position = add_multiline_text(
        resume_profile.education.degree,
        margin_left,
        y_position,
        body_size,
        margin_right - margin_left
    )

    # Save the PDF
    doc.save(output_path)
    doc.close()



