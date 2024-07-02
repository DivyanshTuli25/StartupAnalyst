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

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()

os.environ ["GROQ_API_KEY"] = 'GROQ_API_KEY'
llm = ChatGroq(temperature = 0.2,model_name="llama3-70b-8192")


avators = {"Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
           "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"}


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


researcher_agent = Agent(
    name="Researcher Agent",
    role="Researcher",
    goal="Search data from specified websites",
    backstory="An experienced researcher adept at finding information from the web about {prompt}.",
    verbose=True,
    llm=llm,  # Specify the LLM you want to use
    allow_delegation=False,
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

st.title("💬 Startup Analyst")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What are you planning to build"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Define the tasks
    search_task = Task(
        description=f"Search data about the topic - {prompt} from the following websites: https://yourstory.com/ , https://keevurds.com/ , https://inc42.com/ , https://www.startupindia.gov.in/ , https://www.indianweb2.com/ , https://www.techcircle.in/ , https://entrackr.com/ , https://officechai.com/ , https://economictimes.indiatimes.com/ ",
        agent=researcher_agent,
        expected_output="a detailed multi page report from all the sited containing all relevant data regarding the {prompt} it should have facts, figures and data related."
    )

    summarize_task = Task(
        description="Summarize the researched content based on the user's query",
        agent=writer_agent,
        expected_output="a short and crisp summarised result answering the user query backed with facts, figures and data"
    )

    crew = Crew(
        agents=[researcher_agent, writer_agent],
        tasks=[search_task, summarize_task],
        process=Process.sequential,
    )
    final = crew.kickoff()

    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)


