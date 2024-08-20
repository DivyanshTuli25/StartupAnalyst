

""" -------------------------------------------------------------------------------------------------------"""

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

# CSS to set background image and other styles
page_bg_img = '''
<style>
.stApp {
    background: url('https://w0.peakpx.com/wallpaper/1/675/HD-wallpaper-startup-concept-green-background-rocket-drawn-rocket-business-concepts-startup-rocket-startup-company-business-startup.jpg') no-repeat center center fixed;
    background-size: cover;
    height: 100vh;
    overflow: auto;
}
.title-container {
    background-color: rgba(255, 255, 255, 0.8); /* White with transparency */
    border-radius: 10px;
    padding: 20px;
    margin: auto;
    width: 60%; /* Adjust width as needed */
    text-align: center;
    color: black;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Optional shadow for depth */
}
input::placeholder {
    color: #f28f2c;
    opacity: 1;
}
.response-box {
    border: 2px solid #4B8BBE;
    border-radius: 10px;
    padding: 10px;
    background-color: rgba(249, 249, 249, 0.8);
}
.response-text {
    color: #2b2d42;
    font-size: 20px;
}
.submit-btn {
    background-color: #4B8BBE;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 16px;
}
.submit-btn:hover {
    background-color: #3a8cbf;
}
.content-box {
    background-color: rgba(255, 255, 255, 0.8); /* White with transparency */
    border-radius: 10px;
    padding: 20px;
    margin: 20px auto;
    color: black;
    width: 80%; /* Adjust width as needed */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Optional shadow for depth */
    text-align: center; /* Center-align the content */
}
h1, h2, h3 {
    color: #ff6700;
}
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
/* Sidebar header */
.css-1v3fvcr {
    color: white !important;
}
.st-emotion-cache-1sno8jx {
    color: black;
}
/* Sidebar text */
.css-10trblm {
    color: white !important;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<div class='title-container'><h1>Startup Analyst</h1><h3>Your comprehensive tool for startup analysis and insights</h3></div>", unsafe_allow_html=True)

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
    st.markdown("<div class='content-box'><h2>Welcome to Startup AI Dashboard</h2><p>Select one of the options from the sidebar to run the corresponding module or to learn more about us.</p></div>", unsafe_allow_html=True)

# About page
elif selected == "About":
    st.markdown("<div class='content-box'><h2>About Elion AI</h2><p>Elion AI is a platform designed to provide AI-powered solutions for your business needs. We offer various modules to assist with lead generation, social media content creation, and more. Our goal is to streamline your workflow and enhance productivity using advanced AI technologies.</p></div>", unsafe_allow_html=True)

# Contact Us page
elif selected == "Contact Us":
    st.markdown("<div class='content-box'><h2>Contact Us</h2><p>We'd love to hear from you! Feel free to reach out to us with any questions or feedback.</p><p>Email: reway.ewm@gmail.com</p><p>Phone: +91 7290908877 || +91 9899115560</p></div>", unsafe_allow_html=True)

# Run Startup News
elif selected == "Startup News":
    st.markdown("<div class='content-box'><h2>Run Startup News Module</h2><p>Startup News module is running...</p></div>", unsafe_allow_html=True)
    run_file1()

# Run Startup Analyst
elif selected == "Startup Analyst":
    st.markdown("<div class='content-box'><h2>Run Startup Analyst Module</h2><p>Startup Analyst module is running...</p></div>", unsafe_allow_html=True)
    run_file2()

st.markdown("---")
st.markdown("<div class='content-box'>© 2024 Startup Analyst. All rights reserved.</div>", unsafe_allow_html=True)
