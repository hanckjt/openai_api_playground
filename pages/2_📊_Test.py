import streamlit as st
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from comm_lib import *


def ask_openai(client, model, question):
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": question}]
    response = client.chat.completions.create(messages=messages, model=model, max_tokens=512, stream=False)

    return response


async def get_responses(client, model, questions):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, ask_openai, client, model, question) for question in questions]
        return await asyncio.gather(*futures)


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
        cols = st.columns(2)
        prompt = cols[0].text_input('Prompt', 'Tell me a short joke.')
        concurrency = cols[1].number_input('Concurrency', 1, 100, 1)
        prompts = [prompt] * concurrency
        openai_client = get_openai_client()
        if st.button('Test Speed'):
            with st.chat_message('user'):
                st.markdown(prompt)
            with st.spinner('Testing...'):
                start_time = time.time()
                try:
                    responses = asyncio.run(get_responses(openai_client, model, prompts))
                except Exception as e:
                    st.error(e)
                    return
            end_time = time.time()
            completion_tokens = 0
            for i, response in enumerate(responses):
                with st.chat_message('assistant'):
                    st.write(f'[{i+1}]: {response.choices[0].message.content}')
                completion_tokens += response.usage.completion_tokens
            speed = completion_tokens / (end_time - start_time)
            st.write(f'Speed: {speed:.2f} tokens/s')
            # with st.expander('Response'):
            #     st.write(response)


if __name__ == "__main__":
    main()
