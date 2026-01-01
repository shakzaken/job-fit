from agents import Runner, Agent

from src.models.resume_profile import ResumeProfile


async def resume_profile_extraction(text_input: str) -> ResumeProfile:


    resume_agent = Agent(
        name="resume_profile_agent",
        instructions="You get a resume as text and you need to extract the job profile from it.",
        output_type=ResumeProfile,
        model="gpt-5-mini"
    )

    result  = await Runner.run(resume_agent, text_input)
    resume_profile : ResumeProfile = result.final_output
    return resume_profile