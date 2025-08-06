import re
import streamlit as st
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Temizleme fonksiyonu
def cleant_text(text: str):
    return re.sub(r"<thunk>.*?<think>", "", text, flags=re.DOTALL)

# Başlık
st.title("🧠 Agent with Memory")

# Mesaj geçmişi
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Hafıza (MemorySaver)
if "memory" not in st.session_state:
    st.session_state["memory"] = MemorySaver()

# Model ve Agent tanımı
model = ChatOllama(model="mistral")
chat_agent = create_react_agent(
    model=model,
    tools=[],
    name="chat_agent",
    checkpointer=st.session_state.memory
)

# Mesajları göster
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Kullanıcı girişi
question = st.chat_input("Type your message...")

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Agent'ten cevap al
    result = chat_agent.invoke(
        {
            "messages": [{"role": "user", "content": question}]
        },
        config={"configurable": {"thread_id": 1}}
    )

    response = cleant_text(result["messages"][-1].content)

    # Cevabı göster
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
