from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from mistralai import Mistral
from dotenv import load_dotenv
from app.config import settings


router = APIRouter(
    prefix="/ai_devops_assistant",
    tags=["AI DevOps Assistant"]
)

templates = Jinja2Templates(directory="templates")

api_key = settings.mistral_api_key
model_name = settings.mistral_model
temperature = settings.temperature


@router.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, intent: str = Form(...), target_format: str = Form(...)):
    prompt = f"""
        You are a DevOps engineer. Convert the following instruction into a valid {target_format} configuration file.

        Instruction:
        "{intent}"

        Respond with only the valid {target_format} code — no explanation or extra text.
    """

    try:
        with Mistral(api_key=settings.mistral_api_key) as mistral:
            res = mistral.chat.complete(
                model=settings.mistral_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.temperature,
                max_tokens=2500
            )

        iac_result = res.choices[0].message.content.strip()

    except Exception as e:
        iac_result = f"LLM request failed: {e}"

    # Store in session
    request.session["iac_result"] = iac_result
    request.session["intent"] = intent
    request.session["target_format"] = target_format

    # Redirect to GET /result
    return RedirectResponse(url="/ai_devops_assistant/result", status_code=303)

@router.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    iac_result = request.session.get("iac_result")
    intent = request.session.get("intent")
    target_format = request.session.get("target_format")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "iac_result": iac_result,
            "intent": intent,
            "target_format": target_format
        }
    )