import streamlit as st
from langgraph_database_backend import chatbot, llm
from langchain_core.messages import HumanMessage
import uuid


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
    st.session_state['chat_threads'] = {}


# Add current thread
add_thread(
    st.session_state['thread_id'],
    "New Chat"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title('RAVEN')


if st.sidebar.button('➕ New Chat'):
    reset_chat()
    st.rerun()


st.sidebar.header('My Conversations')


# Display conversations
for thread_id, chat_title in reversed(
    list(st.session_state['chat_threads'].items())
):

    if st.sidebar.button(
        chat_title,
        key=f"thread_{thread_id}"
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


# ============================================================
# DISPLAY CURRENT CHAT HISTORY
# ============================================================

for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.text(message['content'])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input('Type here')


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
        st.text(user_input)


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

#TEST
CONFIG = {'configurable': {'thread_id': 'thread-2'}}
response = chatbot.invoke({'messages': [HumanMessage(content='what is my name?')]}, config=CONFIG)

print(response)