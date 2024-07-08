# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
import os
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
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
    # Initialize the tool for internet searching capabilities
    tool = SerperDevTool()

    os.environ["GROQ_API_KEY"] = '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'
    llm = ChatGroq(temperature=0.2, model_name="llama3-8b-8192")

    avators = {
        "Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
        "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"
    }

    researcher_agent = Agent(
        name="Researcher Agent",
        role="Researcher",
        goal="Search data from specified websites",
        backstory="An experienced researcher adept at finding information from the web about {prompt}.",
        verbose=True,
        llm=llm,  # Specify the LLM you want to use
        allow_delegation=False,
        tool=tool,
        # This agent needs the browser tool to search the web
    )

    # Define the Writer Agent
    writer_agent = Agent(
        name="Writer Agent",
        role="Writer",
        goal="Summarize the researched content based on the user's query about {prompt}",
        backstory="A talented writer skilled at summarizing complex information.",
        verbose=True,
        llm=llm,  # Specify the LLM you want to use
        allow_delegation=False,
        tools=[]
    )

    st.markdown("#### Interactive Chat")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What are you planning to build?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Enter your startup idea or question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Define the tasks
        search_task = Task(
            description=f"Search data about the topic - {prompt} from the following websites: https://yourstory.com/ , https://keevurds.com/ , https://inc42.com/ , https://www.startupindia.gov.in/ , https://www.indianweb2.com/ , https://www.techcircle.in/ , https://entrackr.com/ , https://officechai.com/ , https://economictimes.indiatimes.com/ ",
            agent=researcher_agent,
            expected_output="a detailed multi-page report from all the sites containing all relevant data regarding the {prompt}. It should have facts, figures, and data related."
        )

        summarize_task = Task(
            description="Summarize the researched content based on the user's query",
            agent=writer_agent,
            expected_output="A short and crisp summarized result answering the user's query backed with facts, figures, and data."
        )

        crew = Crew(
            agents=[researcher_agent, writer_agent],
            tasks=[search_task, summarize_task],
            process=Process.sequential,
        )
        final = crew.kickoff()

        result = f"## Here is the Final Result \n\n {final}"

        # Display result in beautiful format
        st.markdown("## Analysis Result")
        companies = final.split('\n\n')  # Split the final result by double newlines to separate companies
        for company in companies:
            with st.container():
                st.markdown(f"### {company.split(':')[0]}")  # Display company name as header
                st.markdown(f"*Details:* {company.split(':')[0]}")  # Display company details

elif selected == "About":
    st.markdown("### About Startup Analyst")
    st.write("Startup Analyst is designed to help users get comprehensive analysis and insights about startups from various reliable sources. Using advanced AI agents, it gathers and summarizes data to provide a detailed report and a concise summary.")

elif selected == "Contact":
    st.markdown("### Contact Us")
    st.write("For any inquiries, please reach out to us at: startup.analyst@example.com")

# Footer
st.markdown("---")
st.markdown("© 2024 Startup Analyst. All rights reserved.")