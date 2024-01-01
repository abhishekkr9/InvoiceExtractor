from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()

        image_parts = [{
            'mime_type': uploaded_file.type,
            'data': bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError('No File uploaded')

st.set_page_config(page_title='Invoice Extract')
st.header('Gemini LLM Application Invoice Extract')
input = st.text_input('Input', key='input')
uploaded_file = st.file_uploader('Choose a document to extract', type=['jpg', 'jpeg', 'png'])
image = ''
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('Tell me about the invoice')

input_prompt = '''You are an expert in understanding invoices. We 
will upload an image as invoices and you will have to answer any questions
based on the uploaded invoice image'''

if submit:
    image_data = input_image_details(uploaded_file )
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader('Response')
    st.write(response)