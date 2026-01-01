import asyncio
from agents import  trace
from dotenv import load_dotenv

from src.models.agent_input import JobAndResume
from src.models.output_report import OutPutReport
from src.pipelines.execute_plan import execute_plan
from src.pipelines.job_profile_extraction import job_profile_extraction
from src.pipelines.matching_score_pipeline import create_matching_score
from src.pipelines.resume_extraction import resume_profile_extraction
from src.pipelines.tailoring_plan_pipeline import create_tailoring_plan
from src.tools.output_file import write_output_mdfile
from src.tools.pdf_utils import convert_resume_pdf_to_str, write_resume_profile_to_pdf

from src.tools.txt_file import extract_text_from_file




async def main():
    with trace("Resume to Job Matching"):
        load_dotenv()
        resume_text = convert_resume_pdf_to_str("assets/input/resume_file.pdf")
        job_file = "assets/input/job_file.txt"
        job_description_text = await extract_text_from_file(job_file)



        resume_profile, job_profile = await asyncio.gather(
            resume_profile_extraction(resume_text),
            job_profile_extraction(job_description_text)
        )



        agent_input = JobAndResume(
            job_profile=job_profile,
            resume_profile=resume_profile
        )


        baseline_match_results,tailoring_plan = await asyncio.gather(
            create_matching_score(agent_input),
            create_tailoring_plan(agent_input)
        )

        tailored_resume = await execute_plan(tailoring_plan,resume_profile)

        updated_agent_input = JobAndResume(
            job_profile=job_profile,
            resume_profile=tailored_resume
        )

        final_match_results = await create_matching_score(updated_agent_input)


        write_resume_profile_to_pdf(tailored_resume, "assets/output/tailored_resume.pdf")
        output_report = OutPutReport(base_match_result=baseline_match_results,
                                     final_match_result=final_match_results)


        write_output_mdfile(output_report, "assets/output/job_fit_report.md")
        print("Process completed. Tailored resume and report generated.")







if __name__ == "__main__":
    asyncio.run(main())




