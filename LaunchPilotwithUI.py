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

    # Input field for the location
    location_input = st.text_input("Enter Business Location", help="Please enter the location of the business")

    # Define agents and tasks for the first part of the analysis
    site_info = Agent(
        role='Company Research Specialist',
        goal='Extract comprehensive information about the company from the given {URL} and provide insights to other agents to improve their analysis.',
        verbose=True,
        backstory=(
            "You are an expert in conducting thorough research on companies. Your skills allow you to delve deep into the provided websites to extract vital information about the company's business overview, mission, vision, products, services, market presence, competitors, and other relevant data. Your detailed findings help other agents enhance their understanding and analysis of the company's overview, business model, market strategy, technology use, and revenue streams."
        ),
        llm=llm,
        allow_delegation=True,
        tools=[search_tool],
        max_iter=5,
        max_rpm = 3000)

    market_research_agent = Agent(
        role='Market Research Analyst',
        goal='Extract detailed market size and market research information from the {prompt} for the location {location}.',
        verbose=True,
        memory=True,
        backstory=(
            "You are an expert in market analysis, skilled at identifying key market trends, target demographics, and market potential. Your insights help in understanding the market dynamics and positioning the business strategically."
        ),
        llm=llm,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000
    )

    business_model_agent = Agent(
        role='Business Analyst',
        goal='Extract detailed business model information from the {prompt}.',
        verbose=True,
        memory=True,
        backstory=(
            "You have a deep understanding of business models and are adept at dissecting them from various business documents. Your analysis helps in comprehending how the business operates, its value proposition, and its key activities."
        ),
        llm=llm,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000
    )

    technology_agent = Agent(
        role='Technology Specialist',
        goal='Extract detailed information on the technology stack from the {prompt}.',
        verbose=True,
        memory=True,
        backstory=(
            "With a keen eye for technological details, you excel at uncovering the specifics of technologies used in various contexts. Your insights are crucial for understanding the technological backbone of the business."
        ),
        llm=llm,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000
    )

    revenue_model_agent = Agent(
        role='Financial Analyst',
        goal='Extract detailed revenue model information from the {prompt}.',
        verbose=True,
        memory=True,
        backstory=(
            "You specialize in financial analysis and have a knack for identifying revenue models in business documents. Your insights help in understanding how the business generates revenue, including pricing strategies and revenue streams."
        ),
        llm=llm,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000)

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
        if pdf_document is not None and url_input and location_input:
            st.subheader("The response is")

            # Define the tasks for the first part
            site_research_task = Task(
                description="Extract comprehensive information about the company from the provided {URL}. Focus on the company's business overview, mission, vision, products, services, market presence, competitors, and other relevant data.",
                expected_output='Detailed company information extracted from the site, including the sector in which the company is working and a short overview of the company’s operations.',
                agent=site_info,
                tools=[search_tool]
            )

            market_research_task = Task(
                description=(
                    "Extract the market size and market research information from the provided {prompt} for the location {location}. "
                    "Focus on identifying key market trends, target demographics, and market potential."
                ),
                expected_output='A summary of the market size and market research findings, including segmentation of market, demographics and trends.',
                agent=market_research_agent,
            )

            business_model_task = Task(
                description=(
                    "Extract the business model information from the provided {prompt}. "
                    "Focus on how the business operates, its value proposition, and its key activities."
                ),
                expected_output='A detailed description of the business model, including key activities and value proposition.',
                agent=business_model_agent,
            )

            technology_task = Task(
                description=(
                    "Extract the technology stack information from the provided {prompt}. "
                    "Focus on the main technologies employed and their applications."
                ),
                expected_output='A summary of the technologies used in the business, including key technologies and their applications.',
                agent=technology_agent,
            )

            revenue_model_task = Task(
                description=(
                    "Extract the revenue model information from the provided {prompt}. "
                    "Focus on how the business generates revenue, including pricing strategies and revenue streams."
                ),
                expected_output='A comprehensive overview of the revenue model, including pricing strategies and revenue streams.',
                agent=revenue_model_agent,
            )

            # Define the crew for the first part
            crew = Crew(
                agents=[site_info, market_research_agent, business_model_agent, revenue_model_agent, technology_agent],
                tasks=[site_research_task, market_research_task, business_model_task, revenue_model_task, technology_task],
                process=Process.sequential,
                rpm=5000
            )

            # Kickoff the crew with the provided inputs
            result = crew.kickoff(inputs={"prompt": full_text, "URL": url_input, "location": location_input})

            # Display the result
            st.write(result)

            # Using the output from the first snippet as input for the second snippet
            st.session_state["first_result"] = result
        else:
            st.write("Please upload a PDF, enter a valid URL, and enter a location to start the analysis.")

    # Define agents and tasks for the second part of the analysis
    marketer = Agent(
        role="Market Research Analyst",
        goal="Analyze the market demand for the business idea in {location_input} and suggest strategies to reach the widest possible customer base.",
        backstory=(
            "You are an expert at understanding market demand, target audience, and competition. Your insights are crucial for validating whether an idea fulfills a market need and has the potential to attract a wide audience. You excel at devising strategies to appeal to the widest possible audience."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000,
        tools=[search_tool],
    )

    technologist = Agent(
        role="Technology Expert",
        goal="Assess the technological feasibility of the business idea and recommend technologies to adopt for success.",
        backstory=(
            "You are a visionary in the realm of technology, with a deep understanding of current and future technologies and trends. Your expertise lies in foreseeing how technology can be leveraged to solve real-world problems and drive business innovation. You ensure that technology adoption enhances operational efficiency and provides a competitive edge."
        ),
        verbose=True,
        allow_delegation=True,
        max_iter=5,
        max_rpm=3000,
        llm=llm,
        tools=[search_tool]
    )

    consultant = Agent(
        role="Business Development Consultant",
        goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long-term sustainability and profitability.",
        backstory=(
            "You are a seasoned professional with expertise in shaping business strategies. Your insights are essential for turning innovative ideas into viable, scalable, and successful business models. You excel at identifying and developing potential revenue streams and ensuring scalability without compromising operational efficiency."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_rpm=3000,
        llm=llm,
    )

    # Button to trigger the second part of the analysis
    submit2 = st.button("Analyze Further")

    if submit2:
        if "first_result" in st.session_state:
            result = st.session_state["first_result"]
            task1 = Task(
                description=f"Analyze the market demand for the business idea: {result} in {location_input}. "
                            "Specify the size of the target market, customer demographics, user persona, and existing competitors. "
                            "Write a detailed report with descriptions of the ideal customer, and strategies to reach the widest possible audience. "
                            "The report should be concise with at least 10 bullet points addressing the most important marketing aspects.",
                agent=marketer,
                expected_output="A 1000-word report providing detailed market analysis.",
                tools=[search_tool]
            )
            task2 = Task(
                description=f"Analyze the technological aspects of the business idea: {result} to provide the most optimized and seamless user experience. "
                            "The solution should be technologically efficient and feasible. "
                            "Write at least 10 bullet points in a concise report addressing the key technological aspects.",
                agent=technologist,
                expected_output="A 1000-word report suggesting technological solutions and steps to implement them.",
                tools=[search_tool]
            )
            task3 = Task(
                description="Analyze and summarize the marketing and technological reports to create a detailed business plan. "
                            f"Ensure the business model for {result} is scalable, profitable, and sustainable. "
                            "The report should be concise with at least 10 bullet points covering the most important business aspects. Format the output as a markdown file.",
                agent=consultant,
                expected_output="Constructive criticism and suggestions for improving the business plan to ensure long-term sustainability and profitability based on the analysis.",
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