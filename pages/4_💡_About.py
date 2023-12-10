import streamlit as st


def main():
    st.set_page_config(page_title='About', page_icon='💡', layout='wide', initial_sidebar_state='auto')
    st.title("About")
    st.write(
        '''
The reason why I developed this online application is because I enjoy researching various new LLMs, 
including open source and closed source online. However, after deploying the server, 
I often have to test it. I searched online for a long time but couldn't find a good one, 
so I wrote one myself with streamlit, you can play any API server that compatible with OpenAI API,
hoping to help friends with similar needs.
        '''
    )
    st.write('Github: https://github.com/hanckjt/openai_api_playground')


if __name__ == "__main__":
    main()
