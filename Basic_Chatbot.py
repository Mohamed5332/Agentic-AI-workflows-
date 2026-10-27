from langgraph.graph import StateGraph , START , END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict ,Annotated
from langchain_core.messages import AIMessage , HumanMessage , BaseMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os


load_dotenv()


llm_config = {'llm' : ChatGroq(model = 'openai/gpt-oss-120b' , api_key = os.getenv(key = 'Groq_api_key') , temperature = 0.5, verbose = False)}
memory_config = {
    "configurable": {
        "thread_id": "1"
    }
}
checkpoint = InMemorySaver()


class Messages_state(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]


def chatbot(state : Messages_state) -> Messages_state:
    prompt = PromptTemplate(
    template="""You are a helpful AI assistant.
    Answer clearly and accurately using the conversation history.
    If context is missing, ask for clarification.

    History: {chat_history}
    User: {user_input}
    Assistant:""",
        input_variables=["chat_history", "user_input"]
    )

    ready_prompt = prompt.invoke(input={
        'chat_history': state['messages'], 
        'user_input': state['messages'][-1]
    })

    response = llm_config['llm'].invoke(input = ready_prompt , config = memory_config)

    return {'messages' : [response]}


graph = StateGraph(state_schema = Messages_state)


graph.add_node('chatbot' , chatbot)

graph.add_edge(START , 'chatbot')
graph.add_edge('chatbot' , END)

workflow = graph.compile(checkpointer= checkpoint)