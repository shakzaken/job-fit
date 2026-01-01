from agents import Agent, Runner

from src.models.agent_input import JobAndResume
from src.models.job_profile import JobProfile
from src.models.output_report import MatchResults
from src.models.resume_profile import ResumeProfile


async def create_matching_score(agent_input: JobAndResume) -> MatchResults:


    matching_agent = Agent(
        name="matching_agent",
        instructions="You get a resume profile and a job profile and you need to create a matching score report between them.",
        output_type=MatchResults,
        model="gpt-5-mini"
    )



    result  = await Runner.run(matching_agent, agent_input.model_dump_json())
    match_results : MatchResults = result.final_output
    return match_results