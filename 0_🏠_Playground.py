import streamlit as st
import pandas as pd
from comm_lib import *


@st.cache_data
def get_models_df():
    try:
        models = get_openai_client().models.list().model_dump()['data']
    except Exception as e:
        st.error(e)
        return None
    df = pd.DataFrame(models)
    if 'permission' in df.columns:
        permission_df = df['permission'].apply(lambda x: x[0]).apply(pd.Series)
        permission_df.drop(columns=['id', 'object', 'created'], inplace=True)
        df = pd.concat([df, permission_df], axis=1)
        df.drop(columns=['permission'], inplace=True)
    df['created'] = pd.to_datetime(df['created'], unit='s')
    return df


def show_models_page():
    st.title('Models List:')
    models_df = get_models_df()
    if models_df is None:
        st.warning('Please set API settings first.')
    else:
        st.dataframe(models_df)


def settings_page():
    st.title('Settings')
    with st.form(key='openai_api_settings_form'):
        base_url = st.text_input('Base URL', get_app_setting('base_url', 'https://api.openai.com/v1'), key='base_url')
        api_key = st.text_input('API Key', get_app_setting('api_key', 'YOUR_API_KEY'), type='password', key='api_key')
        if st.form_submit_button('Get Models') or not get_session_state('inited', False):
            clear_app_setting()
            set_openai_client(base_url, api_key)
            get_models_df.clear()
            reset_chat_history()
            set_session_state('inited', True)

    models_df = get_models_df()
    if models_df is not None:
        with st.form(key='model_settings_form'):
            models = models_df['id'].tolist()
            model_index = models.index(get_app_setting('model', models[0]))
            model = st.selectbox('Select Models', models, key='select_model', index=model_index)
            max_tokens = st.number_input('Max Tokens', 1, 200000, get_app_setting('max_tokens', 512), key='max_tokens')
            temperature = st.slider('Temperature', 0.0, 1.0, get_app_setting('temperature', 0.7), key='temperature')
            top_p = st.slider('Top P', 0.0, 1.0, get_app_setting('top_p', 1.0), key='top_p')
            timeout = st.slider('Time Out', 1, 60, get_app_setting('timeout', 10), key='timeout')
            system_prompt = st.text_input('System Prompt', get_app_setting('system_prompt', 'You are a hellpful assistant.'), key='system_prompt')
            stream = st.checkbox('Stream', get_app_setting('stream', True), key='stream')
            if st.form_submit_button('Confirm'):
                set_app_setting('model', model)
                set_app_setting('max_tokens', max_tokens)
                set_app_setting('temperature', temperature)
                set_app_setting('top_p', top_p)
                set_app_setting('timeout', timeout)
                set_app_setting('stream', stream)
                set_app_setting('system_prompt', system_prompt)

                reset_chat_history()
                st.toast('Model Settings Updated')


def main():
    st.set_page_config(page_title='OpenAI API Playground', page_icon=':robot_face:', layout='wide', initial_sidebar_state='auto')
    # hide streamlit footer
    # hide_streamlit_style = """
    #             <style>
    #             #MainMenu {visibility: hidden;}
    #             footer {visibility: hidden;}
    #             </style>
    #             """
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    settings_page()

    show_models_page()


if __name__ == '__main__':
    main()
