import chainlit as cl
from openai import OpenAI
from chainlit.types import ThreadDict


client = OpenAI()


# Defines what happens when a chat session is started
@cl.on_chat_start
def start_chat():
    print("User started a session!")


# Defines what happens when a user stops a running task
@cl.on_stop
def on_stop():
    print("The user stopped a task!")


# Defines what happens when the user disconnects from the current chat session
@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")


# Defines what happens when the user resumes a previously closed chat session
@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")


@cl.step
async def on_step():
    current_step = cl.context.current_step

    print(current_step)


# Defines what happens when a user sends a message
@cl.on_message
async def main(message: cl.Message):
    with client.responses.stream(
        model="gpt-5-nano",
        input=cl.chat_context.to_openai(),
        instructions="your name is Luna. You are a nice thoughtful Care Assistant. Your preffered Language is german but you can also answer in englisch if nessecary",
    ) as stream:
        msg = cl.Message(content="")

        for event in stream:
            first = True
            if event.type == "response.output_text.delta":
                msg.content += event.delta
                if first:
                    await msg.send()
                else:
                    await msg.update()
