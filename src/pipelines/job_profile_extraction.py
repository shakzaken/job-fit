from agents import Agent, Runner

from src.models.job_profile import JobProfile


async def job_profile_extraction(input_text: str) -> JobProfile:


    job_profile_agent = Agent(
        name="job_profile_agent",
        instructions="You get a job description as text and you need to extract the job profile from it.",
        output_type=JobProfile,
        model="gpt-5-mini"
    )

    result  = await Runner.run(job_profile_agent, input_text)
    job_profile : JobProfile = result.final_output
    return job_profile