"""This is a module that creates personalized messages
based on the occasion, relation, and other details."""

import os
import calendar
from datetime import date
import openai
import pandas as pd
import streamlit as st
from streamlit_extras import buy_me_a_coffee

# Check if we're running on Heroku
if "DYNO" in os.environ:
    # Load Heroku environment variables
    openai.api_key = os.environ.get("OPENAI_APIKEY")
else:
    # Load local environment variables from .env file
    from dotenv import load_dotenv

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_APIKEY")

# Load the celebrities.csv file
celebrities_df = pd.read_csv("data/celebrities.csv")


def get_options_from_file(filename):
    """Read the options from a given file."""
    # Get the path to the data folder
    data_folder = "data"

    # Join the folder path and the filename
    file_path = os.path.join(data_folder, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        options = [line.strip() for line in file]
    return options


def get_input(label, filename=None):
    """Get input from the user based on the given label and filename."""
    if filename:
        options = get_options_from_file(filename)
        options.insert(
            0, ""
        )  # Add an empty option at the beginning of the list
        return st.selectbox(label, options)
    return st.text_input(label)


def get_celebrity_trivia(day, month, celebrities_df):
    """Get celebrity trivia for a given day and month."""
    celebs = (
        celebrities_df[
            (celebrities_df["day"] == day) & (celebrities_df["month"] == month)
        ]
        .sort_values(by="birth_year", ascending=False)
        .head(3)
    )
    trivia_list = []
    for _, celeb in celebs.iterrows():
        status = (
            "still alive"
            if celeb["alive"]
            else f"died in {int(celeb['death_year'])}"
        )
        trivia_list.append(
            f"{celeb['name']} (born {int(celeb['birth_year'])}, {status}):"
            f" {celeb['trivia']}"
        )
    trivia_str = "; ".join(trivia_list)
    return trivia_str


def max_days_for_month(month, year):
    """Return the maximum number of days for a given month and year."""
    if month == 2:
        if year is not None and calendar.isleap(year):
            return 29
        return 28
    if month in [4, 6, 9, 11]:
        return 30
    return 31


st.set_page_config(
    page_title="Moodify My Wish",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODIFIED_STREAMLIT_STYLE = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
"""

st.markdown(MODIFIED_STREAMLIT_STYLE, unsafe_allow_html=True)

buy_me_a_coffee.button(
    username="jasminshah",
    floating=True,
    width=300,
    text="Buy me a hot chocolate",
)

# Use st.sidebar to place the input widgets in the left pane
with st.sidebar:
    # Add an input field for selecting the occasion
    occasion = get_input("*What's the occasion?", "occasions.txt")

    # If the occasion is a birthday or anniversary, we ask for the date
    if occasion in ["Birthday", "Anniversary", "Wedding"]:
        # Create a list of month names
        month_names = [calendar.month_name[i] for i in range(1, 13)]

        # Use st.selectbox to choose the recipient's event month (1-12) by name
        EVENT_MONTH = st.selectbox("*Choose the month", month_names, index=0)

        # Get the month number corresponding to the selected month name
        EVENT_MONTH_NUMBER = month_names.index(EVENT_MONTH) + 1

        if occasion == "Anniversary":
            EVENT_YEAR_LABEL = "Wedding Year"
        elif occasion == "Birthday":
            EVENT_YEAR_LABEL = "Birth Year"
        else:
            EVENT_YEAR_LABEL = "Event Year"

        include_EVENT_YEAR = st.checkbox(
            f"Know their {EVENT_YEAR_LABEL.lower()}?"
        )
        if include_EVENT_YEAR:
            EVENT_YEAR = st.number_input(
                f"Enter the {EVENT_YEAR_LABEL.lower()}",
                min_value=1900,
                max_value=date.today().year,
                value=1900,
                step=1,
                format="%d",
            )
        else:
            EVENT_YEAR = None

        MAX_DAYS = max_days_for_month(EVENT_MONTH_NUMBER, EVENT_YEAR)

        # Use st.selectbox to choose the recipient's event day
        # based on the valid days for the selected month and year
        EVENT_DAY = st.number_input(
            "*Pick the day",
            min_value=1,
            max_value=MAX_DAYS,
            value=1,
            step=1,
            format="%d",
        )
    else:
        EVENT_MONTH = None
        EVENT_DAY = None
        EVENT_YEAR = None

    emotion = get_input("*Choose the message mood:", "moods.txt")
    relation = get_input("*What's your relation to them?", "relations.txt")
    message_size = st.selectbox("*Choose message size:", ["S", "M", "L"])

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
    # pylint: disable=too-many-boolean-expressions
    if (
        (
            occasion in ["Birthday", "Anniversary", "Wedding"]
            and EVENT_MONTH
            and EVENT_DAY
        )
        or (occasion not in ["Birthday", "Anniversary", "Wedding"])
        and emotion
        and relation
    ):
        with st.spinner(f"Crafting your {occasion.lower()} message..."):
            if occasion in ["Birthday", "Anniversary"]:
                TRIVIA = get_celebrity_trivia(EVENT_DAY, EVENT_MONTH_NUMBER, celebrities_df)
                TRIVIA_LINE = (
                    "Some TRIVIA of the famous people that share the same"
                    f" {occasion.lower()} date: {TRIVIA}."
                )
            else:
                TRIVIA_LINE = ""

            system_message = (
                "You are ChatGPT, a large language model trained by OpenAI."
                f" Your task is to generate a great {occasion.lower()} message"
                " for people based on their relation, personal information"
                " and other relevant details. More focus"
                f" {occasion.lower()} and less on other information."
            )

            if occasion in ["Birthday", "Anniversary"]:
                event_date = date(
                    date.today().year, EVENT_MONTH_NUMBER, EVENT_DAY
                )
                EVENT_DATE_LINE = (
                    f"{occasion} date is : {event_date.strftime('%m-%d')}."
                )
            else:
                EVENT_DATE_LINE = ""

            if occasion in ["Birthday", "Anniversary"] and EVENT_YEAR:
                event_age = date.today().year - EVENT_YEAR
                AGE_LINE = (
                    f"Recipient is celebrating their {event_age} years of"
                    f" {occasion.lower()}."
                )
            else:
                AGE_LINE = ""

            USER_MESSAGE = [
                f"Generate a {occasion.lower()} message for my {relation}.",
                f"Mood of the message should be {emotion}.",
                EVENT_DATE_LINE,
                TRIVIA_LINE,
                AGE_LINE,
            ]

            # Add optional fields to the user message
            if name:
                USER_MESSAGE.append(f"Recipient's name is {name}.")
            if profession:
                USER_MESSAGE.append(f"Recipient's profession is {profession}.")
            if hobby:
                USER_MESSAGE.append(f"Recipient's hobby is {hobby}.")
            if accomplishment:
                USER_MESSAGE.append(
                    f"Recipient's recent accomplishment: {accomplishment}."
                )
            if goal:
                USER_MESSAGE.append(f"Recipient's goal or ambition: {goal}.")
            if anecdote:
                USER_MESSAGE.append(
                    f"Personal anecdote or memory: {anecdote}."
                )
            if quote:
                USER_MESSAGE.append(f"Recipient's favorite quote: {quote}.")
            if recent_event:
                USER_MESSAGE.append(
                    f"Recent event or experience: {recent_event}."
                )
            if challenge:
                USER_MESSAGE.append(
                    f"Challenge the recipient is facing: {challenge}."
                )
            if message_size == "S":
                USER_MESSAGE.append("Keep the message short")
            if message_size == "M":
                USER_MESSAGE.append("Keep the message medium size")
            if message_size == "L":
                USER_MESSAGE.append("Make the message long")

            USER_MESSAGE = " ".join(USER_MESSAGE)

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": USER_MESSAGE},
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                n=1,
                temperature=0.7,
            )

            message = (
                response.choices[0]
                .message["content"]
                .strip()
                .lstrip(". ")
                .rstrip()
            )

        st.write(f"💌 **Your {occasion.lower()} message:**")
        st.markdown(f"\n{message}\n")
    else:
        st.error("Please fill in the mandatory (*) fields.")
