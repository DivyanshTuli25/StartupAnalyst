import fitz

# Define the path to the PDF file
pdf_path = 'Pitch 1.5.pdf'

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Initialize an empty list to store the text from each page
pdf_text = []

# Iterate through each page and extract text
for page_num in range(pdf_document.page_count):
    page = pdf_document.load_page(page_num)
    page_text = page.get_text("text")
    pdf_text.append(page_text)

# Join the extracted text into a single string
full_text = "\n".join(pdf_text)

# Print the extracted text
# print(full_text)

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

# pdf_search_tool = PDFSearchTool(
#     pdf='Pitch 1.5.pdf',
#     config=dict(
#         llm=dict(
#             provider="google", # or google, openai, anthropic, llama2, ...
#             config=dict(
#                 model="gemini-1.5-flash",
#                 # temperature=0.5,
#                 # top_p=1,
#                 # stream=true,
#             ),
#         ),
#         embedder=dict(
#             provider="google", # or openai, ollama, ...
#             config=dict(
#                 model="models/text-embedding-004",
#                 task_type="retrieval_document",
#                 # title="Embeddings",
#             ),
#         ),
#     )
# )





market_research_agent = Agent(
    role='Market Research Analyst',
    goal='Extract market size and market research information from the {prompt}',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in market analysis, skilled at identifying key market trends and insights from various texts."
    ),
    # tools=[pdf_search_tool],
    llm = llm,
    allow_delegation=True
)

business_model_agent = Agent(
    role='Business Analyst',
    goal='Extract business model information from the {prompt}',
    verbose=True,
    memory=True,
    backstory=(
        "You have a deep understanding of business models and are adept at dissecting them from any business document."
    ),
    # tools=[pdf_search_tool],
    llm = llm,
    allow_delegation=True
)

technology_agent = Agent(
    role='Technology Specialist',
    goal='Extract information on the technology used from the {prompt}',
    verbose=True,
    memory=True,
    backstory=(
        "With a keen eye for technological details, you excel at uncovering the specifics of technologies used in various contexts."
    ),
    # tools=[pdf_search_tool],
    llm = llm,
    allow_delegation=True
)

revenue_model_agent = Agent(
    role='Financial Analyst',
    goal='Extract revenue model information from the {prompt}',
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in financial analysis and have a knack for identifying revenue models in business documents."
    ),
    # tools=[pdf_search_tool],
    llm = llm,
    allow_delegation=True
)

# Define the tasks
market_research_task = Task(
    description=(
        "Extract the market size and market research information from the provided {prompt}"
        "Focus on identifying key market trends, target demographics, and market potential."
    ),
    expected_output='A summary of the market size and market research findings.',
    # tools=[pdf_search_tool],
    agent=market_research_agent,
)

business_model_task = Task(
    description=(
        "Extract the business model information from the provided {prompt}. "
        "Focus on how the business operates, its value proposition, and its key activities."
    ),
    expected_output='A detailed description of the business model.',
    # tools=[pdf_search_tool],
    agent=business_model_agent,
)

technology_task = Task(
    description=(
        "Extract the technology used from the provided {prompt}. "
        "Focus on the main technologies employed and their applications."
    ),
    expected_output='A summary of the technologies used in the business.',
    # tools=[pdf_search_tool],
    agent=technology_agent,
)

revenue_model_task = Task(
    description=(
        "Extract the revenue model information from the provided {prompt}. "
        "Focus on how the business generates revenue, including pricing strategies and revenue streams."
    ),
    expected_output='A comprehensive overview of the revenue model.',
    # tools=[pdf_search_tool],
    agent=revenue_model_agent,
)

# Define the crew
crew = Crew(
    agents=[market_research_agent, business_model_agent, technology_agent, revenue_model_agent],
    tasks=[market_research_task, business_model_task, technology_task, revenue_model_task],
    process=Process.sequential
)

# Function to kickoff the crew with the pitch deck PDF
result = crew.kickoff(inputs = {"prompt":full_text})
print(result)