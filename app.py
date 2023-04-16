import os
import openai
import calendar
import pandas as pd
import streamlit as st
from streamlit_extras import buy_me_a_coffee
from datetime import date
from streamlit.components.v1 import html

# Check if we're running on Heroku
if 'DYNO' in os.environ:
    # Load Heroku environment variables
    openai.api_key = os.environ.get('OPENAI_APIKEY')
else:
    # Load local environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_APIKEY')

# Load the celebrities.csv file
celebrities_df = pd.read_csv("data/celebrities.csv")

def get_options_from_file(filename):
    # Get the path to the data folder
    data_folder = "data"

    # Join the folder path and the filename
    file_path = os.path.join(data_folder, filename)

    with open(file_path, "r") as file:
        options = [line.strip() for line in file]
    return options

def get_input(label, filename=None):
    if filename:
        options = get_options_from_file(filename)
        options.insert(0, '')  # Add an empty option at the beginning of the list
        return st.selectbox(label, options)
    else:
        return st.text_input(label)


def get_celebrity_trivia(day, month):
    celebs = celebrities_df[(celebrities_df["day"] == day) & (celebrities_df["month"] == month)].sort_values(by="birth_year", ascending=False).head(3)
    trivia_list = []
    for _, celeb in celebs.iterrows():
        status = "still alive" if celeb["alive"] else f"died in {celeb['death_year']}"
        trivia_list.append(f"{celeb['name']} (born {celeb['birth_year']}, {status}): {celeb['trivia']}")
    trivia_str = "; ".join(trivia_list)
    return trivia_str

def max_days_for_month(month, year):
    if month == 2:
        if year is not None and calendar.isleap(year):
            return 29
        else:
            return 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

st.set_page_config(
    page_title="Moodify My Wish",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

modified_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # footer:before {
            #     content:'Made with ❤️ by Jasmin & Powered by OpenAI'; 
            #     visibility: visible;
            #     display: block;
            #     bottom: 0;
            #     text-align: center;
            #     width: 100%;
            #     padding: 5px;
            #     font-size: 16px;
            # }
        </style>
"""

st.markdown(modified_streamlit_style, unsafe_allow_html=True)

buy_me_a_coffee.button(username="jasminshah", floating=True, width=300, text="Buy me a hot chocolate")

# Use st.sidebar to place the input widgets in the left pane
with st.sidebar:

    # Add an input field for selecting the occasion
    occasion = get_input("*What's the occasion?", "occasions.txt")

    # If the occasion is a birthday or anniversary, we ask for the date
    if occasion in ["Birthday", "Anniversary", "Wedding"]:
        # Create a list of month names
        month_names = [calendar.month_name[i] for i in range(1, 13)]

        # Use st.selectbox to choose the recipient's event month (1-12) by name
        event_month = st.selectbox("*Choose the month", month_names, index=0)

        # Get the month number corresponding to the selected month name
        event_month_number = month_names.index(event_month) + 1

        event_year_label = "Wedding Year" if occasion == "Anniversary" else "Birth Year" if occasion == "Birthday" else "Event Year"
        include_event_year = st.checkbox(f"Know their {event_year_label.lower()}?")
        if include_event_year:
            event_year = st.number_input(f"Enter the {event_year_label.lower()}", min_value=1900, max_value=date.today().year, value=1900, step=1, format='%d')
        else:
            event_year = None

        max_days = max_days_for_month(event_month_number, event_year)

        # Use st.selectbox to choose the recipient's event day based on the valid days for the selected month and year
        event_day = st.number_input("*Pick the day", min_value=1, max_value=max_days, value=1, step=1, format='%d')
    else:
        event_month = None
        event_day = None
        event_year = None

    emotion = get_input("*Choose the message mood:", "moods.txt")
    relation = get_input("*What's your relation to them?", "relations.txt")
    message_size = st.selectbox("*Choose message size:", ['S', 'M', 'L'])

    # Create a row with 3 columns to center the button
    col1, col2, col3 = st.columns([1, 2, 1])

    # Create a button in the middle column
    with col2:
        generate_button = st.button("Moodify My Wish 🎉")

    # st.header("Customize Your Wish!")
    with st.expander("Add your personal touch"):
        name = get_input("What's their name?")
        profession = get_input("What do they do?", "professions.txt")
        hobby = get_input("What's their hobby?", "hobbies.txt")
        accomplishment = get_input("Did they achieve something recently?")
        goal = get_input("What's their goal or ambition?")
        anecdote = get_input("Share a fun memory or anecdote")
        quote = get_input("Do they have a favorite quote?")
        recent_event = get_input("What was their recent experience?")
        challenge = get_input("Are they facing any challenges?")

# Keep the generated message display in the main area (right pane)
if generate_button:
    if (occasion in ["Birthday", "Anniversary", "Wedding"] and event_month and event_day) or (occasion not in ["Birthday", "Anniversary", "Wedding"]) and emotion and relation:
        with st.spinner(f"Crafting your {occasion.lower()} message..."):
            if occasion in ["Birthday", "Anniversary"]:
                trivia = get_celebrity_trivia(event_day, event_month_number)
                trivia_line = f"Some trivia of the famous people that share the same {occasion.lower()} date: {trivia}."
            else:
                trivia_line = ""

            system_message = f"You are ChatGPT, a large language model trained by OpenAI. Your task is to generate a great {occasion.lower()} message for people based on their relation, personal information and other relevant details. More focus {occasion.lower()} and less on other information."

            if occasion in ["Birthday", "Anniversary"]:
                event_date = date(date.today().year, event_month_number, event_day)
                event_date_line = f"{occasion} date is : {event_date.strftime('%m-%d')}."
            else:
                event_date_line = ""

            if occasion in ["Birthday", "Anniversary"] and event_year:
                event_age = date.today().year - event_year
                age_line = f"Recipient is celebrating their {event_age} years of {occasion.lower()}."
            else:
                age_line = ""

            user_message = [
                f"Generate a {occasion.lower()} message for my {relation}.",
                f"Mood of the message should be {emotion}.",
                event_date_line,
                trivia_line,
                age_line,
            ]

            # Add optional fields to the user message
            if name:
                user_message.append(f"Recipient's name is {name}.")
            if profession:
                user_message.append(f"Recipient's profession is {profession}.")
            if hobby:
                user_message.append(f"Recipient's hobby is {hobby}.")
            if accomplishment:
                user_message.append(f"Recipient's recent accomplishment: {accomplishment}.")
            if goal:
                user_message.append(f"Recipient's goal or ambition: {goal}.")
            if anecdote:
                user_message.append(f"Personal anecdote or memory: {anecdote}.")
            if quote:
                user_message.append(f"Recipient's favorite quote: {quote}.")
            if recent_event:
                user_message.append(f"Recent event or experience: {recent_event}.")
            if challenge:
                user_message.append(f"Challenge the recipient is facing: {challenge}.")
            if message_size == "S":
                user_message.append("Keep the message short")
            if message_size == "M":
                user_message.append("Keep the message medium size")
            if message_size == "L":
                user_message.append("Make the message long")

            user_message = " ".join(user_message)

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                n=1,
                temperature=0.7,
            )

            message = response.choices[0].message['content'].strip().lstrip(". ").rstrip()

        st.write(f"💌 **Your {occasion.lower()} message:**")
        st.markdown(f"\n{message}\n")
    else:
        st.error("Please fill in the mandatory (*) fields.")
