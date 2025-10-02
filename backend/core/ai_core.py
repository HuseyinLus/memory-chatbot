import re
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

def clean_text(text: str):
    return re.sub(r"<thunk>.*?<think>", "", text, flags=re.DOTALL)

memory = MemorySaver()

model = ChatOllama(model="mistral")
chat_agent = create_react_agent(
    model=model,
    tools=[],
    name="chat_agent",
    checkpointer=memory
)

def ask(question: str, thread_id: int = 1) -> str:
    result = chat_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}}
    )
    return clean_text(result["messages"][-1].content)
