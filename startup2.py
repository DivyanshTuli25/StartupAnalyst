# Pitch deck

import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import PDFSearchTool
from langchain_groq import ChatGroq
os.environ['GROQ_API_KEY'] = "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"
#os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['GOOGLE_API_KEY'] = "AIzaSyDmoR__x6AA3PxbQlJy3ut_O_B4W2tZnrs"

# Initialize the LLM
llm = ChatGroq(temperature=0.2, model_name="llama3-70b-8192")


#Search PDF Tool

pdf_search_tool = PDFSearchTool(
    pdf='Pitch 1.5.pdf',
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini-1.5-flash",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/text-embedding-004",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)


# Define the extractor agent
extractor_agent = Agent(
    role='Information Extractor',
    goal='Extract market size, market research, business model, technology used, and revenue model information from the pitch deck',
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly efficient extractor, capable of pulling out key pieces of information from various documents with precision."
    ),
    tools=[pdf_search_tool],
    llm = llm,
    allow_delegation=False,
    max_iter=10
)

# Define the processing agents
market_research_agent = Agent(
    role='Market Research Analyst',
    goal='Summarize the market size and market research information extracted from the pitch deck',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in market analysis, skilled at identifying key market trends and insights from various documents."
    ),
    llm = llm,
    allow_delegation=True,
max_iter=10
)

business_model_agent = Agent(
    role='Business Analyst',
    goal='Summarize the business model information extracted from the pitch deck',
    verbose=True,
    memory=True,
    backstory=(
        "You have a deep understanding of business models and are adept at dissecting them from any business document."
    ),
    llm = llm,
    allow_delegation=True,
max_iter=10
)

technology_agent = Agent(
    role='Technology Specialist',
    goal='Summarize the information on the technology used extracted from the pitch deck',
    verbose=True,
    memory=True,
    backstory=(
        "With a keen eye for technological details, you excel at uncovering the specifics of technologies used in various contexts."
    ),
    llm = llm,
    allow_delegation=True,
max_iter=10
)

revenue_model_agent = Agent(
    role='Financial Analyst',
    goal='Summarize the revenue model information extracted from the pitch deck',
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in financial analysis and have a knack for identifying revenue models in business documents."
    ),
    llm = llm,
    allow_delegation=True,
max_iter=10
)

# Define the tasks
extractor_task = Task(
    description=(
        "Extract market size, market research, business model, technology used, and revenue model information from the provided pitch deck."
    ),
    expected_output='A dictionary containing the extracted information.',
    tools=[pdf_search_tool],
    agent=extractor_agent,
)

market_research_task = Task(
    description=(
        "Use the extracted information to summarize the market size and market research findings."
    ),
    expected_output='A summary of the market size and market research findings.',
    tools=[],
    agent=market_research_agent,
)

business_model_task = Task(
    description=(
        "Use the extracted information to summarize the business model."
    ),
    expected_output='A detailed description of the business model.',
    tools=[],
    agent=business_model_agent,
)

technology_task = Task(
    description=(
        "Use the extracted information to summarize the technology used."
    ),
    expected_output='A summary of the technologies used in the business.',
    tools=[],
    agent=technology_agent,
)

revenue_model_task = Task(
    description=(
        "Use the extracted information to summarize the revenue model."
    ),
    expected_output='A comprehensive overview of the revenue model.',
    tools=[],
    agent=revenue_model_agent,
)

# Define the crew
crew = Crew(
    agents=[extractor_agent, market_research_agent, business_model_agent, technology_agent, revenue_model_agent],
    tasks=[extractor_task, market_research_task, business_model_task, technology_task, revenue_model_task],
    process=Process.sequential,
    rpm=5000
)

# Function to kickoff the crew with the pitch deck PD
result = crew.kickoff()