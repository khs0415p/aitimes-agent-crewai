from datetime import datetime
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools import get_detail_news, get_today_newslink


@CrewBase
class NewsCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = LLM(
        model="hosted_vllm/google/gemma-3-27b-it",
        base_url="http://localhost:10530/v1",
        api_key="token123",
    )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            allow_delegation=False,
            verbose=True,
            tools=[get_today_newslink, get_detail_news],
            llm=self.llm,
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            llm=self.llm,
        )

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_task"],
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_task"],
            output_file=f"{str(datetime.today().date())}-news.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewTest crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
