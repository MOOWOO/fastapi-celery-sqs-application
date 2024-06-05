import asyncio
import os
from celery.utils.log import get_task_logger
from openai import OpenAI
from .celery_app import celery_app
from celery import shared_task
from tasks.m import call

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

logger = get_task_logger(__name__)
call()

@celery_app.task
def long_task(word: str) -> dict:
    logger.info("long_task called")
    asyncio.run(long_async_task())
    return {'result': word}

async def long_async_task():
    for i in range(10):
        await asyncio.sleep(1)

# OPEN AI DEFAULT - generate_text
@celery_app.task
def generate_text(prompt: str):
  completion = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
      ],
      temperature=0,
      max_tokens=128
  )
  #logger.info(completion)
  return completion.choices[0].message.content

# OPEN AI DEFAULT - generate_image
@celery_app.task
def generate_image(prompt, image_size, image_width):
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size=image_size+"x"+image_width,
      quality="standard",
      n=1,
    )
    image_url = response.data[0].url
    return image_url

# Assistant - Web_search
# from phi.assistant import Assistant
# from phi.tools.duckduckgo import DuckDuckGo

# assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
# assistant.print_response("Whats happening in France?", markdown=True)