import os 
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from agent.models import CodeGeneration

load_dotenv()  # Load environment variables from .env file

SYSTEM_PROMPT = """You are a Python code generation assistant. Respond with ONLY a JSON object \
matching this exact shape, no markdown fences, no extra text:
{"reasoning": "<brief approach>", "code": "<complete runnable python code>"}"""

def get_client()-> OpenAI:
    return OpenAI(
         base_url=os.getenv("OPENAI_BASE_URL"),
         api_key=os.getenv("OPENAI_API_KEY")
    )

def generate_code(client: OpenAI,model:str,message:list[dict])-> CodeGeneration:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *message],
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content

    try:
        return CodeGeneration.model_validate_json(raw)
    except ValidationError as e:
        raise ValueError(f"Invalid response format: {raw}") from e