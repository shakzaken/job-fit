import os
import fitz  # PyMuPDF

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



