import streamlit as st


def main():
    st.set_page_config(page_title='Session', page_icon='📋', layout='wide', initial_sidebar_state='auto')
    st.title("Streamlit Session State")
    st.write(st.session_state)


if __name__ == "__main__":
    main()
