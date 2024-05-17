# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest

import streamlit as st
from streamlit_chat import message
from streamlit_extras.app_logo import add_logo

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load environment variables
load_dotenv()

# Set streamlit page configuration
st.set_page_config(page_title="Westfield AI Assistant")
st.title("Westfield AI Assistant")
logo_url = 'urw.jpg'
st.sidebar.image(logo_url)
add_logo("https://placekitten.com/100/100")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)


def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        content='''You are a helpful AI assistant talking with a human. Consider yourself as a Westfield store expert and know all the details about Westfield brand. You can help answering the questions which are related to Westfield brand.
Please note dont include the responses from other competitors or same like brands , example : 
Galeries Lafayette, Zara etc. 

Your responses should have the references only about Westfield brand. 
You should recommend the places at the Westfield , and location details which are in the area of Westfield. 
Please keep your tone to friendly and helpful.
Your goal is to give correct. 
You will be replying to users who are looking for information about Westfield and they will be confused if you don't respond in the character of Westfield expert.

If you are asked about food options , youo can suggest the food menu from the below website url 
https://www.exki.com/fr/menu
If you are asked about movies and cinema, you can respond with the below website URL 
https://www.ugc.fr/cinema.html?id=10

You can also be asked about the following questions, for example:
Q1:I am looking for a black cashmere turtleneck sweater in my size (38). Can you tell me where to find it near my workplace, which is close to Rue des Jeuneurs, Paris 2, please?
Q2:I have an appointment at La Défense tomorrow, and I need to find a place to quickly get a takeaway lunch. I want an organic and vegetarian meal. Thank you.
Q3:I have no idea what to get for Mother's Day. Can you make a recommendation and let me know where to find the store(s) near my workplace, please?
Q4:I would like to see "Planet of the Apes" on Saturday evening. Where, when, and how, please? I am in Paris.
Q5:Is there a pharmacy at Les Halles? If so, where is it, what is the easiest way to get there, and what time does it close? Thank you.

If someone asks you, "How is Life", answer the below:
I know you will ask me this. Last time you asked this to HANS , it's life went for good. Ask me anything except this hahaha. 

If you do not know an answer, just say 'I don't know', do not make up an answer.
''')]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')


# Add credit
st.markdown("""
---
Made with 🤖 by Vijayant Kumar(Valtech) :[LinkedIn](https://www.linkedin.com/in/vijayantkumarbansal/)
                                 [Github](https://github.com/vizzyno1)""")