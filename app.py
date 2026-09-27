import streamlit as st
from langchain.messages import HumanMessage, AIMessage

from agent import create_gpa_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PUCIT GPA & CGPA Agent",
    page_icon="🎓",
    layout="centered",
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_message_text(message) -> str:
    """
    Extract visible text from a LangChain message.

    Some AI messages are only tool-call messages and therefore
    contain no visible text. Those messages should not be shown
    as empty chat bubbles in the Streamlit interface.
    """

    content = getattr(message, "content", "")

    # Normal text message
    if isinstance(content, str):
        return content.strip()

    # Some LangChain versions can return content blocks
    if isinstance(content, list):

        text_parts = []

        for block in content:

            # Example:
            # "Hello"
            if isinstance(block, str):
                text_parts.append(block)

            # Example:
            # {"type": "text", "text": "Hello"}
            elif isinstance(block, dict):

                if block.get("type") == "text":
                    text_parts.append(
                        str(block.get("text", ""))
                    )

        return "\n".join(text_parts).strip()

    return ""


# ============================================================
# SESSION STATE
# ============================================================

# Create the agent only once.
# This prevents a new agent from being created every time
# Streamlit reruns the application.
if "agent" not in st.session_state:
    st.session_state.agent = create_gpa_agent()


# Store the complete LangChain conversation history.
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.title("🎓 PUCIT GPA & CGPA Agent")

st.caption(
    "Ask about semester GPA, CGPA projections, "
    "or the GPA required to reach a target CGPA."
)


# ============================================================
# DISPLAY CONVERSATION
# ============================================================

for message in st.session_state.messages:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    if isinstance(message, HumanMessage):

        text = get_message_text(message)

        # Only display if there is actually some text.
        if text:

            with st.chat_message("user"):
                st.markdown(text)


    # --------------------------------------------------------
    # ASSISTANT MESSAGE
    # --------------------------------------------------------

    elif isinstance(message, AIMessage):

        text = get_message_text(message)

        # IMPORTANT:
        #
        # The agent can create AI messages that contain only
        # tool calls and have empty content.
        #
        # We keep those messages in conversation history,
        # but DO NOT display them as empty chat bubbles.
        if text:

            with st.chat_message("assistant"):
                st.markdown(text)


# ============================================================
# USER INPUT
# ============================================================

user_text = st.chat_input(
    "Ask about your GPA or CGPA..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_text:

    # --------------------------------------------------------
    # Create the user's LangChain message
    # --------------------------------------------------------

    user_message = HumanMessage(
        content=user_text
    )


    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Send the COMPLETE previous conversation + new message
    # to the agent.
    # --------------------------------------------------------

    messages = (
        st.session_state.messages
        + [user_message]
    )


    # --------------------------------------------------------
    # Run the agent
    # --------------------------------------------------------

    result = st.session_state.agent.invoke(
        {
            "messages": messages
        }
    )


    # --------------------------------------------------------
    # SAVE THE COMPLETE AGENT HISTORY
    #
    # DO NOT filter this.
    #
    # Tool-call messages are needed internally by the agent.
    # We only filter them when DISPLAYING them above.
    # --------------------------------------------------------

    st.session_state.messages = result["messages"]


    # --------------------------------------------------------
    # Rerun Streamlit so the new messages appear immediately.
    # --------------------------------------------------------

    st.rerun()