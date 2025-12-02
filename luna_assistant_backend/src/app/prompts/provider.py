from langsmith import Client

client = Client()


async def _pull_system_prompt() -> str:
    global client
    prompt = client.pull_prompt("luna-chatbot-p-system")
    return prompt[0].prompt.template
