"""Optional Streamlit GUI for the PUCIT GPA/CGPA agent."""

import streamlit as st

from agent import create_gpa_agent


st.set_page_config(page_title="PUCIT GPA & CGPA Agent", page_icon="🎓")
st.title("PUCIT BS(CS) GPA & CGPA Agent")
st.caption("Calculations are performed by deterministic tools; the model does not do arithmetic.")

if "agent" not in st.session_state:
    st.session_state.agent = create_gpa_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if getattr(message, "type", None) not in {"human", "ai"}:
        continue
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message.text)

prompt = st.chat_input("Ask about your GPA or CGPA...")
if prompt:
    from langchain.messages import HumanMessage

    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages + [HumanMessage(content=prompt)]
    result = st.session_state.agent.invoke({"messages": history})
    st.session_state.messages = result["messages"]

    with st.chat_message("assistant"):
        st.markdown(st.session_state.messages[-1].text)
