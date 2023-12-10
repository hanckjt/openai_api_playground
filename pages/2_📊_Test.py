import streamlit as st
import time
from comm_lib import *

def main():
    st.set_page_config(page_title='Test', page_icon='📊', layout='wide', initial_sidebar_state='auto')
    model = get_app_setting('model')
    if not model:
        st.error('Please set the right API settings first.')
        return
    st.title(f'API Test: {model}')
    
    with st.container(border=True):
        st.write('Base URL Latency')
        cols = st.columns([0.6, 0.2, 0.2])
        base_url = cols[0].text_input('Base URL', get_app_setting('base_url', 'https://api.openai.com/v1'), key='base_url')
        if cols[1].button('Connect Latency'):
            latency = test_speed_with_system_proxy(base_url)
            cols[2].write(f'Latency: {latency:.2f} ms')

    with st.container(border=True):
        st.write('Tokens Generate Speed: Temperature=0.0')
        if st.button('Test Speed'):
            prompt = 'Count from 1 to 20, just numbers, no words.'
            with st.chat_message('user'):
                st.markdown(prompt)
            with st.spinner('Testing...'):
                start_time = time.time()
                try:
                    response = openai_chat_completion([{'role': 'user', 'content': prompt}], model, False, 128, 0)
                except Exception as e:
                    st.error(e)
                    return
            end_time = time.time()
            with st.chat_message('assistant'):
                st.write(response.choices[0].message.content)
            tokens = response.usage.completion_tokens
            speed = tokens / (end_time - start_time)
            st.write(f'Speed: {speed:.2f} tokens/s')
            with st.expander('Response'):
                st.write(response)


if __name__ == "__main__":
    main()
