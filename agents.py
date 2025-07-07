import os
from agno.agent import Agent
from agno.models.nebius import Nebius
from dotenv import load_dotenv
from typing import Iterator
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.workflow import RunEvent, RunResponse, Workflow
from pydantic import BaseModel, Field

load_dotenv()

class DeepReasearchAgent(Workflow):

    """
        A multi-stage research workflow that:
        1. Gathers information from the web using advanced scraping tools.
        2. Analyzes and synthesizes the findings.
        3. Produces a clear, well-structured report.
        """
    
    #Searcher: Finds and extracts relevant information from the web

    searcher: Agent = Agent(
        tools=[ScrapeGraphTools(api_key=os.getenv("SGAI_API_KEY"))],
        model=Nebius(
            id="deepseek-ai/DeepSeek-V3-0324",
            api_key=os.getenv("NEBIUS_API_KEY")
        ),
        show_tool_calls=True,
        markdown=True,
        description=(
            "You are ResearchBot-X, an expert at finding and extracting high-quality, "
            "up-to-date information from the web. Your job is to gather comprehensive, "
            "reliable, and diverse sources on the given topic."
        ),
        instructions=(
            "1. Search for the most recent and authoritative and up-to-date sources (news, blogs, official docs, research papers, forums, etc.) on the topic.\n"
            "2. Extract key facts, statistics, and expert opinions.\n"
            "3. Cover multiple perspectives and highlight any disagreements or controversies.\n"
            "4. Include relevant statistics, data, and expert opinions where possible.\n"
            "5. Organize your findings in a clear, structured format (e.g., markdown table or sections by source type).\n"
            "6. If the topic is ambiguous, clarify with the user before proceeding.\n"
            "7. Be as comprehensive and verbose as possible—err on the side of including more detail.\n"
            "8. Mention the References & Sources of the Content. (It's Must)"
        ),
    )

    #Analyst: synthesizes and interprets the research findings
    analyst: Agent = Agent(
        model=Nebius(
            id="deepseek-ai/DeepSeek-V3-0324",
            api_key=os.getenv("NEBIUS_API_KEY")
        ),
        markdown=True,
        description=(
            "You are AnalystBot-X, a critical thinker who synthesizes research findings "
            "into actionable insights. Your job is to analyze, compare, and interpret the "
            "information provided by the researcher."
        )
        instructions=(
            "1. Identify key themes, trends, and contradictions in the research.\n"
            "2. Highlight the most important findings and their implications.\n"
            "3. Suggest areas for further investigation if gaps are found.\n"
            "4. Present your analysis in a structured, easy-to-read format.\n"
            "5. Extract and list ONLY the reference links or sources that were ACTUALLY found and provided by the researcher in their findings. Do NOT create, invent, or hallucinate any links.\n"
            "6. If no links were provided by the researcher, do not include a References section.\n"
            "7. Don't add hallucinations or make up information. Use ONLY the links that were explicitly passed to you by the researcher.\n"
            "8. Verify that each link you include was actually present in the researcher's findings before listing it.\n"
            "9. If there's no Link found from the previous agent then just say, No reference Found."
        ),
    )
        

        
    
    