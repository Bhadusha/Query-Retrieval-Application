import speech_recognition as sr
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Streamlit
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

# Load environment variables
load_dotenv()  # Load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize speech recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()


# Function to capture speech input and convert to text
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    # Adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        st.write("Please Speak. I'm Listening ....")
        audio = recognizer.listen(source)

    # Initialize response
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # Try recognizing the speech in the recording
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# Function to get response from Gemini
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text


# Function to read SQL query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# Prompt template
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science";\nExample 3 - average mark of all students?, the SQL
    command will be something like this SELECT AVG(MARKS) FROM STUDENT;
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit UI to capture speech or text input
st.write("Choose how you want to provide your input:")

option = st.radio("Input Method:", ('Microphone', 'Text'))


if option == 'Microphone':
    with st.spinner("Listening for your query..."):
        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            # Store the transcription in session state
            st.session_state["question"] = guess["transcription"]
            st.write(f"You said: {st.session_state['question']}")

            # Directly generate the SQL query without needing a submit button
            question = st.session_state["question"]
            response = get_gemini_response(question, prompt)
            st.write("Generated SQL Query:", response)
            results = read_sql_query(response, "student.db")
            st.subheader("The Response is:")
            for row in results:
                st.write(row)

elif option == 'Text':
    # Continue to use the text input and submit button approach for text input
    question = st.text_input("Type your SQL query question:", key="input")
    submit = st.button("Ask the question")

    # If submit is clicked
    if submit:
        st.session_state["question"] = question
        response = get_gemini_response(st.session_state["question"], prompt)
        st.write("Generated SQL Query:", response)
        results = read_sql_query(response, "student.db")
        st.subheader("The Response is:")
        for row in results:
            st.write(row)

