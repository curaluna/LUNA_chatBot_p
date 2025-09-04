import chainlit as cl
from openai import OpenAI

client = OpenAI()


cl.instrument_openai()


@cl.on_message
async def main(message: cl.Message):
    response = client.responses.create(
        model="gpt-5",
        input=cl.chat_context.to_openai(),
        instructions="Zour name is Luna, Ans you are a nice Care Assistant.",
    )
    res = response.output_text

    await cl.Message(content=res).send()
