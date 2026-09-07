import asyncio

from database import db
from app.services.openai_service import ask_openai_async

from datetime import datetime, timezone


async def process_multiple_inputs(user_inputs):
    try:
        tasks = [
            ask_openai_async(user_input)
            for user_input in user_inputs
        ]

        responses = await asyncio.gather(*tasks)

        for user_input, response in zip(user_inputs, responses):
            db.history.insert_one({
                "userInput": user_input,
                "response": response,
                "createdAt": datetime.now(timezone.utc)
            })

        return responses

    except Exception as error:
        print("Error:", error)
        raise