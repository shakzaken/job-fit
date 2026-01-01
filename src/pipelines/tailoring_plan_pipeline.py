from agents import Agent, Runner

from src.models.agent_input import JobAndResume
from src.models.tailoring_plan import TailoringPlan


async def create_tailoring_plan(agent_input: JobAndResume) -> TailoringPlan:

    instructions = """You get a resume profile and a job profile
        and you need to create a tailoring plan       
        to improve the resume to better match the job profile.
     """

    tailoring_plan_agent = Agent(
        name="tailoring_plan_agent",
        instructions=instructions,
        output_type=TailoringPlan,
        model="gpt-5-mini"
    )
    result = await Runner.run(tailoring_plan_agent, agent_input.model_dump_json())
    tailoring_plan: TailoringPlan = result.final_output
    return tailoring_plan