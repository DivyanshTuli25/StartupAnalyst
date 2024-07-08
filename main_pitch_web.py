# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2 streamlit-option-menu
import streamlit as st
import os
from crewai import Crew, Process, Agent, Task
from langchain_groq import ChatGroq
import fitz
from crewai_tools import SerperDevTool
from streamlit_option_menu import option_menu

# Page Configuration
st.set_page_config(page_title="Startup Analyst", page_icon="💬", layout="wide")

# Title and Description
st.title("💬 Startup Analyst")
st.markdown("### Your comprehensive tool for startup analysis and insights")

# Sidebar for Navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "About", "Contact"],
        icons=["house", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    # File uploader for the PDF document
    st.markdown("#### Upload your Pitch Deck or Resume")
    pdf_document = st.file_uploader("Upload PDF", type="pdf", help="Please upload a PDF document")

    # Input field for the website URL
    st.markdown("#### Enter the Company Website URL")
    url_input = st.text_input("Company Website URL", help="Please enter the URL of the company website")

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
    submit1 = st.button("Analyze Pitch Deck")

    if submit1:
        if pdf_document is not None and url_input:
            st.subheader("Analysis Result")

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
                process=Process.sequential,
                rpm=5000
            )

            # Kickoff the crew with the provided inputs
            result = crew.kickoff(inputs={"prompt": full_text, "URL": url_input})

            # Display the result
            result_display = f"## Here is the Final Result \n\n {result}"
            st.write(result_display)
        else:
            st.write("Please upload a PDF and enter a valid URL to start the analysis.")

elif selected == "About":
    st.markdown("### About Startup Analyst")
    st.write("Startup Analyst is designed to help users get comprehensive analysis and insights about startups from various reliable sources. Using advanced AI agents, it gathers and summarizes data to provide a detailed report and a concise summary.")

elif selected == "Contact":
    st.markdown("### Contact Us")
    st.write("For any inquiries, please reach out to us at: startup.analyst@example.com")

# Footer
st.markdown("---")
st.markdown("© 2024 Startup Analyst. All rights reserved.")