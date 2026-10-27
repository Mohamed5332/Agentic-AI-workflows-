import streamlit as st 
from Basic_Chatbot import workflow , memory_config
from langchain_core.messages import AIMessage , HumanMessage , BaseMessage

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages : 
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input(placeholder = "write your message...")


if user_input:
    with st.chat_message('user'):
        st.write(user_input)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(token.content for (token , meta_data) in workflow.stream(input = {'messages' : [HumanMessage(content = user_input.strip())]}
                                                                              , config= memory_config
                                                                              , stream_mode='messages') if token.content)


    st.session_state.messages.append({'role' : 'user', 'content' : user_input.strip()})
    st.session_state.messages.append({'role' : 'assistant', 'content' : ai_message})    
    