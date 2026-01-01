# Job-Fit: AI-Powered Resume Tailoring & Job Matching System

## Overview

Job-Fit is an intelligent resume optimization system that leverages AI agents to analyze job descriptions, evaluate resume compatibility, and automatically tailor resumes to maximize job-fit scores. The application uses multiple AI agents working in concert to extract structured data from resumes and job postings, calculate detailed matching scores, generate tailoring plans, and produce optimized resume outputs. The system provides quantitative before-and-after matching analysis, showing how tailoring improves your resume's alignment with specific job requirements.

## Technologies Used

- **Python 3.11+**: Core programming language
- **OpenAI Agents (0.6.3+)**: Agentic AI framework for orchestrating multiple AI agents
- **Pydantic (2.x)**: Data validation and structured output modeling
- **PyMuPDF (1.26.7+)**: PDF processing for reading and generating resume PDFs
- **Trafilatura & lxml**: Web scraping and text extraction from job postings
- **OpenAI GPT-5-mini**: Language model powering all AI agents
- **asyncio**: Asynchronous execution for parallel agent workflows
- **dotenv**: Environment variable management

## Application Flow & Agent Interactions

### Input
The application expects two inputs:
1. **Resume PDF**: A PDF file containing the candidate's resume (placed in `assets/input/resume_file.pdf`)
2. **Job Description**: A text file with the job posting (placed in `assets/input/job_file.txt`)

### Agent Workflow

The application orchestrates five specialized AI agents in a multi-stage pipeline:

1. **Resume Parser Agent** (`resume_profile_agent`)
   - Extracts structured data from resume text
   - Outputs: `ResumeProfile` object with contact info, summary, skills, experiences (with bullets), projects, and education

2. **Job Profile Agent** (`job_profile_agent`)
   - Analyzes job description text
   - Outputs: `JobProfile` object with title, company, responsibilities (ranked), must-have skills, nice-to-have skills, keywords, and seniority/domain signals

3. **Matching Agent** (`matching_agent`)
   - Compares resume against job requirements
   - Calculates fit scores by category (1-100 scale)
   - Identifies missing keywords and provides evidence mapping
   - Runs twice: baseline (original resume) and final (tailored resume)

4. **Tailoring Plan Agent** (`tailoring_plan_agent`)
   - Creates strategic plan to optimize resume
   - Generates per-bullet instructions (keep/rewrite/emphasize/de-emphasize/remove)
   - Prioritizes changes and sets aggressiveness level

5. **Execute Plan Agent** (`execute_plan_agent`)
   - Applies tailoring plan to original resume
   - Produces optimized `ResumeProfile` with improved alignment

### Execution Flow

```
┌─────────────────┐         ┌─────────────────┐
│  Resume PDF     │         │ Job Description │
└────────┬────────┘         └────────┬────────┘
         │                           │
         v                           v
   [PDF Parser]              [Text Extractor]
         │                           │
         v                           v
┌─────────────────┐         ┌─────────────────┐
│ Resume Profile  │         │  Job Profile    │
│     Agent       │         │     Agent       │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └──────────┬────────────────┘
                    v
        ┌─────────────────────────┐
        │   Matching Agent        │
        │  (Baseline Scoring)     │
        └───────────┬─────────────┘
                    │
        ┌───────────┴─────────────┐
        v                         v
┌─────────────────┐    ┌─────────────────────┐
│ Tailoring Plan  │    │  Baseline Match     │
│     Agent       │    │     Results         │
└────────┬────────┘    └─────────────────────┘
         │
         v
┌─────────────────┐
│  Execute Plan   │
│     Agent       │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Tailored Resume │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Matching Agent  │
│ (Final Scoring) │
└────────┬────────┘
         │
         v
┌─────────────────────────────┐
│      Final Outputs:         │
│  • Tailored Resume PDF      │
│  • Comparison Report (MD)   │
└─────────────────────────────┘
```

### Output
The application produces:
1. **Tailored Resume PDF**: Optimized resume formatted as PDF (`assets/output/tailored_resume.pdf`)
2. **Job Fit Report**: Markdown report comparing baseline vs. final match scores (`assets/output/job_fit_report.md`)

## Project Structure

```
job-fit/
├── main.py                           # Main application entry point
├── pyproject.toml                    # Project dependencies and configuration
├── uv.lock                          # Dependency lock file
├── README.md                        # This file
├── .env                             # Environment variables (create this)
│
├── assets/
│   ├── input/                       # Input files directory
│   │   ├── resume_file.pdf         # Your resume (PDF format)
│   │   └── job_file.txt            # Job description (text format)
│   │
│   └── output/                      # Generated outputs
│       ├── tailored_resume.pdf     # Optimized resume
│       └── job_fit_report.md       # Matching analysis report
│
└── src/
    ├── __init__.py
    ├── agents.py                    # Agent definitions
    │
    ├── models/                      # Pydantic data models
    │   ├── __init__.py
    │   ├── agent_input.py          # JobAndResume input model
    │   ├── evidence_map.py         # Evidence mapping structures
    │   ├── job_profile.py          # Job description structure
    │   ├── output_report.py        # Report output models
    │   ├── resume_profile.py       # Resume structure
    │   └── tailoring_plan.py       # Tailoring plan structure
    │
    ├── pipelines/                   # Agent workflow pipelines
    │   ├── __init__.py
    │   ├── execute_plan.py         # Execute tailoring plan
    │   ├── job_profile_extraction.py      # Extract job profile
    │   ├── matching_score_pipeline.py     # Calculate match scores
    │   ├── resume_extraction.py    # Extract resume profile
    │   └── tailoring_plan_pipeline.py     # Generate tailoring plan
    │
    └── tools/                       # Utility functions
        ├── __init__.py
        ├── extract_job.py          # Job description extraction
        ├── output_file.py          # Report generation
        ├── pdf_utils.py            # PDF read/write operations
        └── txt_file.py             # Text file operations
```

## How to Run the Application

### Prerequisites

1. **Python 3.11 or higher** installed on your system
2. **OpenAI API key** with access to GPT models

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd /path/to/job-fit
   ```

2. **Install dependencies**
   
   This project uses `uv` for dependency management. Install dependencies with:
   ```bash
   uv sync
   ```
   
   All dependencies are defined in `pyproject.toml`.

3. **Create a `.env` file** in the project root with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```
   
   Replace `your-openai-api-key-here` with your actual OpenAI API key.

4. **Prepare your input files**
   
   Place the following files in the `assets/input/` directory:
   - **Resume**: Save your resume as `resume_file.pdf`
   - **Job Description**: Save the job posting as `job_file.txt`
   
   The application is configured to look for these exact file names. No changes to `main.py` are needed.

5. **Run the application**
   ```bash
   python main.py
   ```

### What the Application Does

When you run the application, it will:

1. ✓ Read your resume PDF and job description
2. ✓ Extract structured data using AI agents (parallel processing)
3. ✓ Calculate baseline matching score
4. ✓ Generate tailoring plan with specific improvement actions
5. ✓ Apply tailoring plan to create optimized resume
6. ✓ Calculate final matching score
7. ✓ Generate tailored resume PDF
8. ✓ Create comparison report in Markdown format

### Expected Outputs

After successful execution, check the `assets/output/` directory for:

1. **`tailored_resume.pdf`**: Your optimized resume with improved bullet points, enhanced keywords, and better alignment with the job requirements

2. **`job_fit_report.md`**: A detailed report containing:
   - Baseline fit score (before optimization)
   - Final fit score (after optimization)
   - Category-by-category comparison
   - Missing keywords identified
   - Evidence mapping showing how your experience matches requirements

### Troubleshooting

- **OpenAI API errors**: Verify your API key is correct in the `.env` file and you have sufficient credits
- **PDF reading errors**: Ensure your resume PDF is not password-protected or corrupted
- **Module not found errors**: Verify all dependencies are installed correctly
- **Model access errors**: The application uses `gpt-5-mini` - ensure your API key has access to this model (or update to `gpt-4o-mini` in the pipeline files if needed)

### Customization

- **Change AI model**: Edit the `model="gpt-5-mini"` parameter in files under `src/pipelines/` to use different OpenAI models
- **Adjust tailoring aggressiveness**: The tailoring plan agent automatically determines this, but you can modify the logic in `src/pipelines/tailoring_plan_pipeline.py`
- **Customize output format**: Modify `src/tools/output_file.py` and `src/tools/pdf_utils.py` for different output formats

---

**Note**: This application uses AI agents that make API calls to OpenAI. Processing time depends on resume/job description length and typically takes 30-90 seconds. API costs vary based on usage (typically $0.10-0.50 per run with GPT-5-mini).
