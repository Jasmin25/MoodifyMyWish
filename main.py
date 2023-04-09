from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Check if we're running on Heroku
if 'DYNO' in os.environ:
    # Load Heroku environment variables
    openai.api_key = os.environ.get('OPENAI_APIKEY')
else:
    # Load local environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_APIKEY')

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate/")
async def generate_message(emotion: str = Form(...), birthday: str = Form(...)):
    prompt = f"Write a {emotion} birthday message for someone born on {birthday}. Include trivia about famous people born on this date."
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=50, n=1, stop=None, temperature=0.7)

    message = response.choices[0].text.strip()
    return HTMLResponse(f"<html><body><h1>Birthday Message</h1><p>{message}</p><a href='/'>Generate another message</a></body></html>")
