import streamlit as st
import os
import google.generativeai as genai
import pathlib
import textwrap
from PIL import Image


GOOGLE_API_KEY = "AIzaSyAO_h3uP2pf8ofupMCscDBXnmxWJuE5EbM"

from dotenv import load_dotenv
load_dotenv() # loading environment variables

genai.configure(api_key=GOOGLE_API_KEY)

#Function ot load Gemini Pro model and get responses

pro_model = genai.GenerativeModel("gemini-pro")
pro_vision_model = genai.GenerativeModel("gemini-pro-vision")


@st.cache_data
def get_gemini_response(question):
    response = pro_model.generate_content(question)
    return response.text

@st.cache_data
def get_gemini_vision_response(input, _image):
    if input != "":
        # Assuming pro_vision_model is correctly defined elsewhere
        response = pro_vision_model.generate_content([input, _image])
    else:
        response = pro_vision_model.generate_content(_image)
    return response.text

# Set page configuration
st.set_page_config(page_title="Gemini PRO Model QnA")

# Sidebar
st.sidebar.title("Model Selection")
selected_model = st.sidebar.selectbox(
    "Which Model would you like to select",
    ("Gemini Pro Model", "Gemini Pro Vision Model")
)
# Toggle switch for st.cache
use_cache = st.sidebar.checkbox("log data", value=True)

# Display different content based on the selected model
if selected_model == "Gemini Pro Model":
    st.header("Gemini Pro LLM Application")
    input_question = st.text_input("Prompt Here : ", key="input")
    
    submit_button = st.button("Ask the Question", )
    
    if submit_button:
        if use_cache:
            response = get_gemini_response(input_question)
        else:
            # If st.cache is turned off, execute the function without caching
            response = get_gemini_response(input_question)
        st.subheader("The Response is")
        st.write(response)

elif selected_model == "Gemini Pro Vision Model":
    st.header("Gemini Pro Vision LLM Application")
    input_question = st.text_input("Prompt Here : ", key="input")
    
    uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "png", "jpeg"])
    image = ""
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
 
    submit_button = st.button("Illustrate the Image")
        
    if submit_button:
        if use_cache:
            response = get_gemini_vision_response(input_question, _image=image)
        else:
            # If st.cache is turned off, execute the function without caching
            response = get_gemini_response(input_question, _image=image)
        st.subheader("The Response is")
        st.write(response)
