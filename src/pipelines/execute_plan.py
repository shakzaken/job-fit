from agents import Agent, Runner
from pydantic import BaseModel

from src.models.resume_profile import ResumeProfile
from src.models.tailoring_plan import TailoringPlan


class ExecutionInput(BaseModel):
    tailoring_plan: TailoringPlan
    resume: ResumeProfile

async def execute_plan(tailoring_plan: TailoringPlan, resume: ResumeProfile) -> ResumeProfile:

    instructions = """
            You get a resume profile and a tailoring plan.
            You need to apply the tailoring plan to the resume profile
            and return the updated resume profile.
        """

    execute_plan_agent = Agent(
        name="execute_plan_agent",
        instructions=instructions,
        output_type=ResumeProfile,
        model="gpt-5-mini"
    )

    execution_input = ExecutionInput(
        tailoring_plan=tailoring_plan,
        resume=resume
    )

    result = await Runner.run(execute_plan_agent, execution_input.model_dump_json())
    updated_resume: ResumeProfile = result.final_output
    return updated_resume
