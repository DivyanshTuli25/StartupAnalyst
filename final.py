import streamlit as st
from streamlit_option_menu import option_menu
import subprocess

# Define functions to run each file
def run_file1():
    subprocess.run(["streamlit", "run", "startup_hack.py"])


def run_file2():
    subprocess.run(["streamlit", "run", "Launchpilot2.py"])

# Streamlit UI
st.set_page_config(page_title="Startup Analyst", page_icon=":robot_face:", layout="wide")

# CSS to set background image
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://t4.ftcdn.net/jpg/02/28/95/71/240_F_228957151_YEMbK50JJ0t1fpPC0P8ngAuEdkMdnFtC.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("### Your comprehensive tool for startup analysis and insights")

st.markdown("#### Facts and Data about Startups in India")
st.markdown("""
   - **Number of Startups in India:** Over 50,000 startups as of 2023
   - **MSME IPO Size:** The average IPO size for MSMEs in India has been growing, with many raising substantial capital.
   """)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "About", "Contact Us", "Startup News", "Startup Analyst"],
        icons=["house", "info", "envelope", "play", "play"],
        menu_icon="cast",
        default_index=0,
    )

# Home page
if selected == "Home":
    st.title("Welcome to Startup AI Dashboard")
    st.write("Select one of the options from the sidebar to run the corresponding module or to learn more about us.")

# About page
elif selected == "About":
    st.title("About Crew AI")
    st.write("""
        Crew AI is a platform designed to provide AI-powered solutions for your business needs.
        We offer various modules to assist with lead generation, social media content creation, and more.
        Our goal is to streamline your workflow and enhance productivity using advanced AI technologies.
    """)

# Contact Us page
elif selected == "Contact Us":
    st.title("Contact Us")
    st.write("""
        We'd love to hear from you! Feel free to reach out to us with any questions or feedback.

        **Email:** reway.ewm@gmail.com
        **Phone:** +91 7290908877 || +91 9899115560
    """)

# Run Startup News
elif selected == "Startup News":
    st.title("Run Startup News Module")
    run_file1()
    st.write("Startup News module is running...")

# Run Startup Analyst
elif selected == "Startup Analyst":
    st.title("Run Startup Analyst Module")
    run_file2()
    st.write("Startup Analyst module is running...")

st.markdown("---")
st.markdown("© 2024 Startup Analyst. All rights reserved.")
