from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from src.app.prompts import SYSTEM_PROMPT
from src.app.models import get_llm
# config is centralized here at first


# prompts and variables
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{question}")
])

#Modell 
llm = get_llm()

# Output parser
parser = StrOutputParser()

# link the chains LCEL Pipeline
qa_chain = prompt | llm | parser


