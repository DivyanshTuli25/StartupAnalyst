import streamlit as st
import os
from crewai import Crew, Process, Agent, Task
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
import fitz
from collections import Counter
from streamlit_option_menu import option_menu

# Setup API keys and models
os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(temperature=0.2, model_name="llama3-70b-8192")

# Initialize the tool for internet searching capabilities
search_tool = SerperDevTool()

# Page Configuration
st.set_page_config(page_title="Startup Analyst", page_icon="💬", layout="wide")

# Sidebar for Navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "About", "Mission & Vision", "Contact"],
        icons=["house", "info-circle", "bullseye", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    # Title and Description
    st.title("💬 Startup Analyst")
    st.markdown("### Your comprehensive tool for startup analysis and insights")

    # File uploader for the PDF document
    pdf_document = st.file_uploader("Upload Resume", type="pdf", help="Please upload a PDF")

    # Input field for the website URL
    url_input = st.text_input("Enter Company Website URL", help="Please enter the URL of the company website")

    # Define agents and tasks for the first part of the analysis
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
        max_iter=2
    )

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
        max_iter=5
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
        max_iter=5
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
        max_iter=5
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
        max_iter=5
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

            # Define the tasks for the first part
            site_research_task = Task(
                description="Extract comprehensive information about the company from the provided {URL}. Focus on the company's history, mission, vision, products, services, market presence, competitors, and any other relevant data.",
                expected_output='Detailed company information extracted from the site. Extract the sector in which company is working, short overview about what the company is doing.',
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

            # Define the crew for the first part
            crew = Crew(
                agents=[site_info, market_research_agent, business_model_agent, technology_agent, revenue_model_agent],
                tasks=[site_research_task, market_research_task, business_model_task, technology_task,
                       revenue_model_task],
                process=Process.sequential,
                rpm=5000
            )

            # Kickoff the crew with the provided inputs
            result = crew.kickoff(inputs={"prompt": full_text, "URL": url_input})

            # Display the result
            st.write(result)

            # Using the output from the first snippet as input for the second snippet
            st.session_state["first_result"] = result
        else:
            st.write("Please upload a PDF and enter a valid URL to start the analysis.")

    # Define agents and tasks for the second part of the analysis
    marketer = Agent(
        role="Market Research Analyst",
        goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
        backstory=(
            "You are an expert at understanding the market demand, target audience and competition. "
            "This is crucial for validating whether an idea fulfills a market need and has the potential to attract a wide audience. "
            "You are good at coming up with ideas on how to appeal to the widest possible audience."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=True,
        max_iter=10,
        tools=[search_tool],
    )

    technologist = Agent(
        role="Technology Expert",
        goal="Make an assessment on how technologically feasible the company is and what type of technologies the company needs to adopt in order to succeed.",
        backstory=(
            "You are a visionary in the realm of technology, with a deep understanding of both current and future technologies and trends. "
            "Your expertise lies not just in knowing the technology but in foreseeing how it can be leveraged to solve real world problems and drive business innovation. "
            "You have a knack for understanding which technological solutions best fit different business models and needs, ensuring that companies stay ahead of their competitors and emerge as market leaders. "
            "Your insights are crucial in aligning technology with business strategies, ensuring that the tech adoption not only enhances operational efficiency but also provides a competitive edge in the market."
        ),
        verbose=True,
        allow_delegation=True,
        max_iter=10,
        llm=llm,
        tools=[search_tool]
    )

    consultant = Agent(
        role="Business Development Consultant",
        goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long-term sustainability and profitability. Suggest ways to improve the business model.",
        backstory=(
            "You are a seasoned professional with expertise in shaping business strategies. "
            "Your insights are essential for turning innovative ideas into viable, scalable, and successful business models. "
            "You have a keen understanding of various industries and are adept at identifying and developing potential revenue streams. "
            "Your experience in scalability ensures that a business can grow without compromising its values or operational efficiency. "
            "Your advice is not just about immediate gains but about building a resilient and adaptable business that can thrive in a changing market. "
            "Provide constructive criticism to the user to improve the business model."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=10,
        llm=llm,
    )

    # Button to trigger the second part of the analysis
    submit2 = st.button("Analyze Further")

    if submit2:
        if "first_result" in st.session_state:
            result = st.session_state["first_result"]
            task1 = Task(
                description=f"Analyze the market demand for business idea: {result} in India as well as the rest of the world."
                            "Specify the size of the target market, customer demographics, user persona, and existing competitors. "
                            "Write a detailed report with descriptions of what the ideal customer must look like, and how to reach the widest possible audience. "
                            "The report has to be concise with at least 10 bullet points and it has to address the most important ideas when it comes to marketing this type of business.",
                agent=marketer,
                expected_output="create a 1000 word report giving details about the market analysis",
                tools=[search_tool]
            )
            task2 = Task(
                description=f"Analyze how we can incorporate technology in the business idea: {result} to provide the most optimized and seamless experience to the user "
                            "and to solve the problem more efficiently. "
                            "The solution should be the most efficient and feasible technologically. "
                            "Write at least 10 bullet points and the report must be concise and must address the most important aspects and areas when it comes to this kind of tech business.",
                agent=technologist,
                expected_output="curate a 1000 word report suggesting the tech solutions and steps to implement them",
                tools=[search_tool]
            )
            task3 = Task(
                description="Analyze and summarize marketing and technological report and write a detailed business plan with a description of how "
                            f"to make a sustainable and profitable business for {result} so that this business is scalable, profitable, and sustainable. "
                            "The report has to be concise with at least 10 bullet points covering the most important aspects and areas for this business, format the output as a markdown file.",
                agent=consultant,
                expected_output=f"Provide constructive criticism to the user by suggesting improvements in the B-Plan to ensure long-term business sustainability and profitability based on: {result}",
                output_file='B-Plan.md'
            )

            crew = Crew(
                agents=[marketer, technologist, consultant],
                tasks=[task1, task2, task3],
                process=Process.sequential,
            )
            final = crew.kickoff()

            result2 = f"## Here is the Final Result \n\n {final}"
            st.write(result2)
        else:
            st.write("Please run the first analysis to get the initial results.")

elif selected == "About":
    st.title("About Startup Analyst")
    st.markdown("""
    ### Welcome to Startup Analyst!
    Our mission is to provide comprehensive insights and analysis for startups, helping you make informed decisions and optimize your business strategies. We leverage the power of AI and advanced analytical tools to deliver precise and actionable information.
    """)

elif selected == "Mission & Vision":
    st.title("Our Mission & Vision")
    st.markdown("""
    ### Mission
    To empower startups with accurate and insightful analysis that drives growth and success.

    ### Vision
    To be the leading platform for startup analysis, providing unparalleled support and resources for entrepreneurs worldwide.
    """)

elif selected == "Contact":
    st.title("Contact Us")
    st.markdown("""
    ### We'd love to hear from you!
    If you have any questions or feedback, please reach out to us at [email@example.com](mailto:email@example.com).
    """)