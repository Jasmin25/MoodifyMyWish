# Moodify My Wish

[![Pylint](https://img.shields.io/badge/Pylint%20Score-9.5%2F10-green)](https://www.pylint.org/)
[![PEP8](https://img.shields.io/badge/PEP8%20Compliant-Yes-brightgreen)](https://www.python.org/dev/peps/pep-0008/)
[![Code Coverage](https://img.shields.io/badge/Code%20Coverage-95%25-yellow)](https://coverage.readthedocs.io/)

Moodify My Wish is a web application that generates personalized messages based on the occasion, relation, and other details. It is powered by OpenAI's GPT-3.5-turbo language model.

## Features

- Generate personalized messages for different occasions (e.g. Birthday, Anniversary, Wedding)
- Customize the message mood, relation, and size
- Incorporate additional personal details such as name, profession, hobby, accomplishments, and more
- Provide celebrity trivia for birthdays and anniversaries

## Live Demo

You can access the live demo of Moodify My Wish here: [https://moodifymywish.herokuapp.com/](https://moodifymywish.herokuapp.com/)

## Installation

1. Clone the repository:

```git clone https://github.com/Jasmin25/MoodifyMyWish.git```

2. Navigate to the project directory:

```cd MoodifyMyWish```

3. Create a virtual environment:

```python3 -m venv wish_env```

4. Activate the virtual environment:

- On Linux and macOS:

```source venv/bin/activate```

- On Windows:

```env\Scripts\activate```

5. Install the required packages:

```pip install -r requirements.txt```

6. Set up the environment variables:

- Copy the `.env.example` file and rename it to `.env`
- Fill in the required information (e.g. OpenAI API key)

7. Run the Streamlit app:

```streamlit run app.py```

The application will be available at http://localhost:8501

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Jasmin Shah - [Github](https://github.com/Jasmin25)