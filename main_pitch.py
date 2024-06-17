# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
import os
import fitz
from crewai import Crew, Process, Agent, Task
from crewai_tools.tools.pdf_search_tool.pdf_search_tool import PDFSearchTool
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import fitz

st.title("💬 Startup Analyst")
pdf_document = st.file_uploader("Upload Resume", type="pdf", help="Please upload pdf")
# Define the path to the PDF file
# pdf_path = 'Pitch 1.5.pdf'

# Open the PDF file
if pdf_document is not None:
    pdf_document=fitz.open(stream=pdf_document.read(), filetype="pdf")
    # Initialize an empty list to store the text from each page
    pdf_text = []

    # Iterate through each page and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text("text")
        pdf_text.append(page_text)
    full_text = "\n".join(pdf_text)



# Initialize the tool for internet searching capabilities

os.environ ["GROQ_API_KEY"] = "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"
llm = ChatGroq(temperature = 0.2,model_name="llama3-70b-8192")


avators = {"Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
           "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"}

# pdf_search_tool = PDFSearchTool(
#     pdf=r'C:\Users\User\PycharmProjects\NonTech\Divyansh-CV-AI-May.pdf',
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
# class MyCustomHandler(BaseCallbackHandler):
#
#     def __init__(self, agent_name: str) -> None:
#         self.agent_name = agent_name
#
#     def on_chain_start(
#             self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
#     ) -> None:
#         """Print out that we are entering a chain."""
#         st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
#         st.chat_message("assistant").write(inputs['input'])
#
#     def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
#         """Print out that we finished a chain."""
#         st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
#         st.chat_message(self.agent_name, avatar=avators[self.agent_name]).write(outputs['output'])


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
    allow_delegation=True,
    max_iter=10
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
    allow_delegation=True,
max_iter=10



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
    allow_delegation=True,
max_iter=10
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
    allow_delegation=True,
max_iter=10
)



# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "What are you planning to build"}]
#
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])
#
# if prompt := st.chat_input():
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
submit1 = st.button("Pitch Deck Summary")

if submit1:
    if full_text is not None:

        st.subheader("The response is")

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
        process=Process.sequential,
        rpm=5000
    )

    # Function to kickoff the crew with the pitch deck PDF
    result = crew.kickoff(inputs={"prompt": full_text})

    result = f"## Here is the Final Result \n\n {full_text}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)



