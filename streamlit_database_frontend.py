import streamlit as st
from langgraph_database_backend import chatbot, llm, retrieve_all_thread
from langchain_core.messages import HumanMessage
import uuid


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAVEN AI",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background: #0b0f14;
        color: #f5f7fa;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #10151c;
        border-right: 1px solid #202832;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-brand {
        padding: 10px 12px 25px 12px;
    }

    .sidebar-brand-title {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #ffffff;
        margin-bottom: 3px;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #7f8a98;
        letter-spacing: 0.5px;
    }

    .conversation-title {
        font-size: 11px;
        font-weight: 600;
        color: #697586;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 25px;
        margin-bottom: 10px;
        padding-left: 8px;
    }

    /* =========================
       SIDEBAR BUTTONS
       ========================= */

    section[data-testid="stSidebar"] button {
        border-radius: 9px;
        border: 1px solid transparent;
        background: transparent;
        color: #cbd5e1;
        text-align: left;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #1a212b;
        border-color: #293441;
        color: white;
    }

    /* =========================
       MAIN CONTENT
       ========================= */

    .main-container {
        max-width: 900px;
        margin: auto;
        padding-top: 35px;
    }

    .raven-header {
        text-align: center;
        margin-bottom: 40px;
    }

    .raven-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .raven-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    .raven-subtitle {
        color: #7f8a98;
        font-size: 14px;
        margin-top: 5px;
    }

    /* =========================
       CHAT MESSAGES
       ========================= */

    div[data-testid="stChatMessage"] {
        background: transparent;
        padding: 12px 0;
    }

    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        font-size: 15px;
        line-height: 1.65;
    }

    /* =========================
       CHAT INPUT
       ========================= */

    div[data-testid="stChatInput"] {
        background: #111720;
        border: 1px solid #293441;
        border-radius: 16px;
    }

    div[data-testid="stChatInput"] textarea {
        color: #ffffff;
        background: transparent;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #697586;
    }

    /* =========================
       EMPTY STATE
       ========================= */

    .empty-state {
        text-align: center;
        margin-top: 17vh;
    }

    .empty-icon {
        font-size: 55px;
        margin-bottom: 10px;
    }

    .empty-title {
        font-size: 27px;
        font-weight: 650;
        color: #ffffff;
    }

    .empty-description {
        color: #7f8a98;
        font-size: 14px;
        margin-top: 8px;
    }

    /* =========================
       DIVIDER
       ========================= */

    .divider {
        height: 1px;
        background: #202832;
        margin: 15px 0;
    }

    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #505b69;
        font-size: 11px;
        margin-top: 35px;
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_thread_id():
    return str(uuid.uuid4())


def generate_chat_title(user_input):

    prompt = f"""
    Generate a short and meaningful title for this conversation.

    User's first message:
    {user_input}

    Rules:
    - Maximum 4 words
    - Keep it concise
    - No quotation marks
    - Describe the main topic
    """

    response = llm.invoke(prompt)

    return response.content.strip()


def add_thread(thread_id, title="New Chat"):

    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = title


def reset_chat():

    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []

    add_thread(thread_id, "New Chat")


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={
            'configurable': {
                'thread_id': thread_id
            }
        }
    )

    return state.values.get('messages', [])


# ============================================================
# SESSION STATE
# ============================================================

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {
        t: f"Chat {t}"
        for t in retrieve_all_thread()
    }


# Add current thread
add_thread(
    st.session_state['thread_id'],
    "New Chat"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🪶 RAVEN</div>
            <div class="sidebar-brand-subtitle">
                Your intelligent AI assistant
            </div>
        </div>
    """, unsafe_allow_html=True)


    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):

        reset_chat()
        st.rerun()


    st.markdown(
        '<div class="conversation-title">Conversations</div>',
        unsafe_allow_html=True
    )


    # Display conversations
    for thread_id, chat_title in reversed(
        list(st.session_state['chat_threads'].items())
    ):

        if st.button(
            f"💬  {chat_title}",
            key=f"thread_{thread_id}",
            use_container_width=True
        ):

            st.session_state['thread_id'] = thread_id

            messages = load_conversation(thread_id)

            temp_messages = []

            for msg in messages:

                if isinstance(msg, HumanMessage):
                    role = 'user'
                else:
                    role = 'assistant'

                temp_messages.append({
                    'role': role,
                    'content': msg.content
                })

            st.session_state['message_history'] = temp_messages

            st.rerun()


    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-brand-subtitle">Powered by LangGraph + Groq</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MAIN CONTAINER
# ============================================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True
)


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state['message_history']:

    st.html("""
        <div class="empty-state">
            <div class="empty-icon">🪶</div>

            <div class="empty-title">
                How can I help you?
            </div>

            <div class="empty-description">
                Ask me anything. Your conversations are saved automatically.
            </div>
        </div>
    """)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state['message_history']:

    with st.chat_message(message['role']):

        st.markdown(message['content'])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Message RAVEN..."
)


CONFIG = {
    'configurable': {
        'thread_id': st.session_state['thread_id']
    }
}


# ============================================================
# CHAT PROCESSING
# ============================================================

if user_input:

    current_thread_id = st.session_state['thread_id']


    # --------------------------------------------------------
    # Generate title for FIRST message
    # --------------------------------------------------------

    if (
        st.session_state['chat_threads'][current_thread_id]
        == "New Chat"
    ):

        chat_title = generate_chat_title(user_input)

        st.session_state['chat_threads'][
            current_thread_id
        ] = chat_title


    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message('user'):

        st.markdown(user_input)


    # --------------------------------------------------------
    # Stream assistant response
    # --------------------------------------------------------

    with st.chat_message('assistant'):

        ai_message = st.write_stream(

            message_chunk.content

            for message_chunk, metadata in chatbot.stream(

                {
                    'messages': [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },

                config=CONFIG,

                stream_mode='messages'
            )

            if message_chunk.content
        )


    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_message
    })


st.markdown(
    '<div class="footer">RAVEN AI · Intelligent conversations</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)