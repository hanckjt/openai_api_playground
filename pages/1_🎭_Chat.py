import streamlit as st
from comm_lib import *


def chat_page():
    model = get_app_setting('model')
    if not model:
        st.error('Please set the right API settings first.')
        return
    st.title(f'Chat: {model}')
    chat_tool = st.columns([0.6, 0.2, 0.2])
    uploaded_file = chat_tool[0].file_uploader('Upload File', key='upload_file')
    file_type = chat_tool[1].selectbox('File Type', ['Text', 'Image', 'Audio', 'Video'], key='file_type')
    if chat_tool[2].button('Clean History'):
        reset_chat_history()
    if chat_tool[2].button('Regenerate'):
        get_chat_history().pop()
        set_session_state('regenerate', True)

    for msg in get_chat_history():
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    need_regenerate = get_session_state('regenerate', False)
    user_input = st.chat_input('User Input', key='user_input')
    if user_input or need_regenerate:
        if need_regenerate:
            user_input = get_session_state('last_user_input', '')
        else:
            add_chat_history('user', user_input)
            with st.chat_message('user'):
                st.markdown(user_input)
        max_tokens = get_app_setting('max_tokens', 512)
        temperature = get_app_setting('temperature', 0.7)
        top_p = get_app_setting('top_p', 1.0)
        stream = get_app_setting('stream', True)
        timeout = get_app_setting('timeout', 10)
        with st.chat_message('assistant'):
            with st.spinner('Thinking...'):
                try:
                    response = openai_chat_completion(get_chat_history(), model, stream, max_tokens, temperature, top_p, timeout)
                except Exception as e:
                    st.error(e)
                    return
                if response:
                    if stream:
                        placeholder = st.empty()
                        streaming_text = ''
                        for chunk in response:
                            if chunk.choices[0].finish_reason == 'stop':
                                break
                            chunk_text = chunk.choices[0].delta.content
                            if chunk_text:
                                streaming_text += chunk_text
                                placeholder.markdown(streaming_text)
                        model_msg = streaming_text
                    else:
                        model_msg = response.choices[0].message.content
                        with st.chat_message('assistant'):
                            st.markdown(model_msg)

            set_session_state('last_user_input', user_input)
            if need_regenerate:
                set_session_state('regenerate', False)

            add_chat_history('assistant', model_msg)


def main():
    st.set_page_config(page_title='Chat', page_icon='🎭', layout='wide', initial_sidebar_state='auto')
    chat_page()


if __name__ == "__main__":
    main()
