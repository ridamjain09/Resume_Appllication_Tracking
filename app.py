from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])


def get_gemini_respone(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text 

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        firstpage = images[0] #Content of entire images

        #convert to bytes 
        img_byte_arr = io.BytesIO()
        firstpage.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                'mime_type':'image/jpeg',
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#Streamlit application 
st.set_page_config(page_title="Resume Application Tracker ")
st.header("ATS Tracking System ")
input_text = st.text_area("Job Description ",key="input")
upload_file = st.file_uploader("Upload your resume(PDF)....",type=['pdf'])


if upload_file is not None:
    st.write("PDF uploaded successfully")

#Creating Buttons for getting output from resume 

submit1 = st.button("Tell me about the resume")

submit2 = st.button("How can I improve my skills")

submit3 = st.button("Tell me about the percentage match with Job Description")


#Lets write the input prompt 
input_prompt1 = """

You are a experienced Human Resource Manager with tech experience in Data Science,Full Stack,Data Engineering,Devops and Data Analyst,
your task is to review the provided resume against the job description for these profiles.
Please share your professional Evaluation on whether the candidates profile align with the role.
Highlight the strenth and Weakness of the applicant in relation to specified job role

"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of Data Science,Full Stack,Data Engineering,Devops and deep ATS functionality, Data Analyst
Your task is to evaluate the resume against the provided job description, Give me the percentage of match if the resume matches with the Job description
and also provide me the missing keywords in the resume which are required for the Job Description
"""

if submit1:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_respone(input_prompt1,pdf_content,input_text)
        st.subheader('The response is ')
        st.write(response)
        st.balloons()
    else:
        st.write("Please uplaod the resume")
elif submit2:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_respone(input_prompt1,pdf_content,input_text)
        st.subheader('The response is ')
        st.write(response)
        st.balloons()
elif submit3:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_respone(input_prompt2,pdf_content,input_text)
        st.subheader('The response is ')
        st.write(response)
        st.balloons()
else:
    st.write("Please click on the button to get the response")


