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

        tools=[ScrapeGraphTools(ap_key=os.getenv("SGAI_API_KEY"))],
        model=Nebius(
            id = ""deepseek-ai/DeepSeek-V3-0324", api_key=os.getenv("NEBIUS_API_KEY")  
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
    
    