import os
from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash",
                             verbose = True,
                             temperature = 0.5,
                             google_api_key = os.getenv("GOOGLE_API_KEY")
                             )
marketer=Agent(
    role="Market Research Analyst",
    goal="Find out how big is the demand for my products and suggest how to reach widest possible customer base",
    backstory="""You are an expert at understanding the market demand, target audience and competition.
    This is crucial for validating whether an idea fulfills a market need and has the potential to attract a wide audience
    You are good at coming up with ideas on how to appeal to widest possible audience""",
    verbose=True,
    llm=llm,
    allow_delegation=True,
    max_iter=10,
    tools=[tool]
)

technologist=Agent(
    role="Technology Expert",
    goal="Make assessment on how technologically feasible the company is and what type of technologies the company needs to adopt in order to succeed.",
    backstory="""You are a visionary in the realm of technology, with a deep understanding of 
    both current and future technologies and trends. Your expertise lies not just in knowing the technology but in foreseeing how it can be leveraged to solve real world problems and drive business innovation
    You have a knack for understanding which technological solutions best fit different business models and needs ensuringthat companies stay ahead of their competitors and emerge as market leaders
    Your insights are crucial in in aligning technology with business strategies, ensuring that the tech adoption not only enhances operational efficiency but also provides a competitive edge in the market""",
    verbose=True,
    allow_delegation=True,
    max_iter=10,
    llm=llm,
    tools=[tool]
)
consultant=Agent(
    role="Business Development Consultant",
    goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long term sustainability and profitability",
    backstory="""You are a seasoned professional with expertise in shaping business startegies. Your insights are essential for tunring innovative ideas into viable, scalable and successful business models.
    You have a keen understanding of various industries and are adept at identifying and developing potential revenue streams.
    Your experience in scalability ensures that a business can grow without compromising with its values or operational efficiency. Your
    advice is not just about immediate gains but about building a resilient and adaptable business that can thrive in a changing market.
    """,
    verbose=True,
    allow_delegation=False,
    max_iter=10,
    llm=llm,
)

task1=Task(
    description="Analyze the market demand for business idea: {topic} in India as well as the rest of the world."
                "Specify the size of target market, customer demographics, user persona and existing competitors"
                "Write a detailed report with descriptions of what the ideal customer must look like, and how to reach the "
                "wildest possible audience. The report has to be concise  with atleast 10 bullet points and it has to address "
                "the most important ideas when it comes to marketing this type of business ",
    agent=marketer,
    expected_output="create a 1000 word report giving details about the market analysis",
    tools=[tool]
)
task2=Task(
    description="Analyze how can we incorporate technology in the business idea : {topic} to provide the most optimised and seemless experience to user"
    "and to solve the problem more efficiently"
    "The solution should be most efficient and feasible technologically"
    "write atleast 10 bullet points and the report must be concise and must address the most important aspects and ares when it comes to this kind of tech business",
    agent=technologist,
    expected_output="curate a 1000 word report suggesting the tech solutions and steps to implement them",
    tools=[tool]
)

task3=Task(
    description="Analyse and summarise marketing and technological report and write a detailed business plan with description of how"
                "to make a sustainable and profitable business for {topic} so that this business is scalable, profitable and sustainable"
                "The report has to be concise with atleast 10 bullet points covering the most important aspects and areas for this business, format the output as a markdown file ",
    agent=consultant,
    expected_output="Prepare a detailed report summarising the complete B-Plan that can act as a handbook to build a successful business on the idea: {topic}",
    output_file='B-Plan.md'
)

crew=Crew(
    agents=[marketer, technologist, consultant],
    tasks=[task1,task2,task3],
    process=Process.sequential,
)

result=crew.kickoff(inputs={'topic':'A B2B marketplace for ELectronic Waste connecting ewaste recyclers with sellers of e waste'})
print(result)

