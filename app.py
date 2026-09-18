import streamlit as st
from chatbot import get_response

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="centered",
)


# ------------------------------------------------------------------
# Response renderer — structured Pydantic output → Streamlit widgets
# ------------------------------------------------------------------
def render_response(response):
    category_icon = {
        "programming": "💻",
        "math":        "📐",
        "general":     "💬",
    }.get(response.category, "💬")

    st.markdown(f"{category_icon} `{response.category.upper()}`")
    st.markdown(response.answer)

    with st.expander("📝 Summary"):
        st.write(response.summary)

    with st.expander("🏷️ Keywords"):
        st.write("  ".join(f"`{kw}`" for kw in response.keywords))

    with st.expander("❓ Follow-up Questions"):
        for followup in response.follow_up_questions:
            st.write(f"- {followup}")


# ------------------------------------------------------------------
# Page header
# ------------------------------------------------------------------
st.title("🤖 LangChain Chatbot")
st.caption("Powered by RunnableBranch · RunnableParallel · Pydantic Structured Output")
st.divider()

# ------------------------------------------------------------------
# Session state — chat history
# Each entry: {"role": "user"|"assistant", "content": str, "response": ChatResponse|None}
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------
# Render existing chat history
# ------------------------------------------------------------------
for entry in st.session_state.messages:
    with st.chat_message(entry["role"]):
        if entry["role"] == "user":
            st.markdown(entry["content"])
        else:
            render_response(entry["response"])

# ------------------------------------------------------------------
# Chat input — at the bottom
# ------------------------------------------------------------------
user_input = st.chat_input("Ask me anything about programming, math, or anything else…")

if user_input:
    # 1. Show user bubble immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Save user message
    st.session_state.messages.append({
        "role":     "user",
        "content":  user_input,
        "response": None,
    })

    # 3. Call chatbot + show assistant bubble
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = get_response(user_input)
        render_response(response)

    # 4. Save assistant response
    st.session_state.messages.append({
        "role":     "assistant",
        "content":  None,
        "response": response,
    })
