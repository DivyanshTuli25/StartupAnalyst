# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
import os
from crewai import Crew, Process, Agent, Task
from langchain_groq import ChatGroq
import fitz
from crewai_tools import SerperDevTool

st.title("💬 Startup Analyst")

# File uploader for the PDF document
pdf_document = st.file_uploader("Upload Resume", type="pdf", help="Please upload pdf")

# Input field for the website URL
url_input = st.text_input("Enter Company Website URL", help="Please enter the URL of the company website")

# Initialize the tool for internet searching capabilities
os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(temperature=0.2, model_name="llama3-70b-8192")

# Serper tool for extracting information from URLs
search_tool = SerperDevTool()

# Agent for company research
site_info = Agent(
    role='Company Research Specialist',
    goal='Extract comprehensive information about the company from the given {URL} and provide insights to other agents to improve their analysis.',
    verbose=True,
    backstory=(
        "You are an expert in conducting thorough research on companies. With your skills, you delve deep into the provided websites to extract vital information about the company's history, mission, vision, products, services, market presence, competitors, and any other relevant data. Your detailed findings help other agents enhance their understanding and analysis of the company's business model, market strategy, technology use, and revenue streams."
    ),
    llm=llm,
    allow_delegation=True,
    tools=[search_tool],
    max_iter=7
)

# Other agents for different aspects of the analysis
market_research_agent = Agent(
    role='Market Research Analyst',
    goal='Extract market size and market research information from the {prompt}',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in market analysis, skilled at identifying key market trends and insights from various texts."
    ),
    llm=llm,
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
    llm=llm,
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
    llm=llm,
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
    llm=llm,
    allow_delegation=True,
    max_iter=10
)

# Process the uploaded PDF
if pdf_document is not None:
    pdf_document = fitz.open(stream=pdf_document.read(), filetype="pdf")
    pdf_text = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text("text")
        pdf_text.append(page_text)
    full_text = "\n".join(pdf_text)

# Button to trigger the analysis
submit1 = st.button("Pitch Deck Summary")

if submit1:
    if pdf_document is not None and url_input:
        st.subheader("The response is")

        # Define the tasks
        site_research_task = Task(
            description="Extract comprehensive information about the company from the provided {URL}. Focus on the company's history, mission, vision, products, services, market presence, competitors, and any other relevant data.",
            expected_output='Detailed company information extracted from the site.',
            agent=site_info,
            tools=[search_tool]
        )

        market_research_task = Task(
            description=(
                "Extract the market size and market research information from the provided {prompt}. "
                "Focus on identifying key market trends, target demographics, and market potential."
            ),
            expected_output='A summary of the market size and market research findings.',
            agent=market_research_agent,
        )

        business_model_task = Task(
            description=(
                "Extract the business model information from the provided {prompt}. "
                "Focus on how the business operates, its value proposition, and its key activities."
            ),
            expected_output='A detailed description of the business model.',
            agent=business_model_agent,
        )

        technology_task = Task(
            description=(
                "Extract the technology used from the provided {prompt}. "
                "Focus on the main technologies employed and their applications."
            ),
            expected_output='A summary of the technologies used in the business.',
            agent=technology_agent,
        )

        revenue_model_task = Task(
            description=(
                "Extract the revenue model information from the provided {prompt}. "
                "Focus on how the business generates revenue, including pricing strategies and revenue streams."
            ),
            expected_output='A comprehensive overview of the revenue model.',
            agent=revenue_model_agent,
        )

        # Define the crew
        crew = Crew(
            agents=[site_info, market_research_agent, business_model_agent, technology_agent, revenue_model_agent],
            tasks=[site_research_task, market_research_task, business_model_task, technology_task, revenue_model_task],
            process=Process
            .sequential,
            rpm=5000
        )

        # Kickoff the crew with the provided inputs
        result = crew.kickoff(inputs={"prompt": full_text, "URL": url_input})

        # Display the result
        result_display = f"## Here is the Final Result \n\n {result}"
        # st.session_state.messages.append({"role": "assistant", "content": result_display})
        st.write(result_display)
    else:
        st.write("Please upload a PDF and enter a valid URL to start the analysis.")