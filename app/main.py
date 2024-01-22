from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from chatgpt import generate_gpt3_response
from pydantic import BaseModel

class UserInput(BaseModel):
    user_input: str

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_to_home():
    return "/home"

@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    title = "Persona AI"
    description = "Build and interact with personalized AI personas. Create your custom models and explore the capabilities of persona-based AI."
    return templates.TemplateResponse("home.html", {"request": request, "title": title, "description": description})

@app.get("/form", response_class=HTMLResponse)
def read_root(request: Request, response_text: str = ""):
    return templates.TemplateResponse("form.html", {"request": request, "response_text": response_text})

@app.post("/form", response_class=HTMLResponse)
async def process_form(request: Request, large_input: str = Form(...), dropdown: str = Form(...), small_input: str = Form(...)):
    response_text = f"Large Input: {large_input}<br>Dropdown: {dropdown}<br>Small Input: {small_input}"
    return templates.TemplateResponse("form.html", {"request": request, "response_text": response_text})

@app.post("/chatbot", response_class=JSONResponse)
async def chatbot_interaction(user_input: UserInput):
    # Use the user input to generate a response from GPT-3
    gpt3_response = generate_gpt3_response(user_input.user_input)

    return {"response": gpt3_response}

@app.get("/chatbot", response_class=HTMLResponse)
def read_chatbot(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

