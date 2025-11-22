from typing import Dict,Any,List
from llama_index.core.workflow import (
    Workflow,StartEvent,
    StopEvent,
    step,
    Event,
    Context
) 
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage

class ResearchEvent(Event):
    query:str

class AnalysisEvent(Event):
    research_data:str
    original_query:str

class ResearchWorkflow(Workflow):

    def __init__(
            self,
            research_agent: ReActAgent,
            analysis_agent: ReActAgent,
            verbose: bool = True,
            **kwargs
    ):
        # Call parent class constructor
        super().__init__(**kwargs)

        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.verbose = verbose  # set verbosity flag


    @step 
    async def start(self,ctx:Context, ev:StartEvent)-> ResearchEvent:
        query=ev.get("query","")

        if self.verbose:
            print(f"\nStarting Research Workflow...")
        await ctx.set("original_query",query)

        return ResearchEvent(query=query)
    
    @step
    async def research_phase(self,ctx:Context,ev:ResearchEvent)->AnalysisEvent:
        if self.verbose:
            print("Research agent is active...")

        research_task=(
            f"Research the following query and gather comprehensive information: {ev.query}\n\n"
            "Use the search_web tool to find relevant sources"
            "if needed,use get_content to fetch detailed information from specific URLs"
            "Provide a summary of all sources found with their URLs"
        )

        response = await self.research_agent.achat(research_task)

        research_data=str(response)

        if self.verbose:
            print(f"\n Research Complete. Data collected")

        return AnalysisEvent(
            research_data=research_data,
            original_query=ev.query
        )
    @step 
    async def analysis_phase(self,ctx:Context, ev:AnalysisEvent)->StopEvent:

        if self.verbose:
            print("Analysis agent active...")

        analysis_task=(
            "Analyze the following research data and answer user's question.\n\n"
            f"Original question: {ev.original_query}\n\n"
            f"Research data:{ev.research_data}\n\n"
            "Provide a comrehensive answer that:\n"
            "1.Directly address the user's question\n"
            "2.Synthesis key findingd from the research\n"
            "3.Includes relevant citations and sources\n"
            "4.Presents information in a clear,structred format"
        )

        response = await self.analysis_agent.achat(analysis_task)
        final_answer=str(response)

        if self.verbose:
            print("Workflow Complete.")

        return StopEvent(result=final_answer)
    
async def run_research_query(
        workflow:ResearchWorkflow,
        query:str
)->str:
    
    result= await workflow.run(query=query)

    return result
        

