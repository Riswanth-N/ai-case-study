import os

from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

async def ask_openai_async(user_input):
    from database import db

    prompt = db.prompts.find_one({
        "_id": "Education_Prompt"
    })

    if not prompt:
        raise ValueError("Education prompt not found")

    final_prompt = prompt["template"].replace(
        "{{userInput}}",
        user_input
    )

    response = await async_client.responses.create(
        model="gpt-5.6-luna",
        input=final_prompt
    )

    return response.output_text