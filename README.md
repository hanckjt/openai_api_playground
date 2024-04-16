# OpenAI API Playground

<img src="https://github.com/hanckjt/openai_api_playground/assets/16874002/ce6eff49-51a9-45ed-936e-70fb3e12137e" width="60%">

The reason why I developed this online application is because I enjoy researching various new LLMs, including open source and closed source online.
However, after deploying the server, I often have to test it. I searched online for a long time but couldn't find a good one, so I wrote one myself with streamlit.
You can play any API server that compatible with OpenAI API, hoping to help friends with similar needs.

Try it on streamlit cloud: [https://openai-api-playground.streamlit.app/](https://openai-api-playground.streamlit.app/)

![91bf86c9b3830da22b9a396f7614edd](https://github.com/hanckjt/openai_api_playground/assets/16874002/0090d833-2e87-4d24-8e00-589d78954a60)
![a20236222dca67f84e9a610091912de](https://github.com/hanckjt/openai_api_playground/assets/16874002/7e3d8ea5-8e5b-471a-bbd5-997829d41c4e)
![bc273669795010b976d3cb9d7a94505](https://github.com/hanckjt/openai_api_playground/assets/16874002/063bc804-d0ab-4ecf-ad91-a02eb49bd735)

## Feature List:

- [X] Set API server URL and KEY
- [X] List all models on the server and informations
- [X] Specify a model and set its parameters
- [X] Support for stream or non-stream mode
- [X] Test the connection latency of the API server
- [X] Test the token generation speed of the model with concurrency
- [X] View the complete session state content of Streamlit
- [ ] Support multimodal model, including images, audio or video
- [ ] Conduct Q&A interactions using uploaded text files as a knowledge base
- [ ] Support for online content search for reference

## Usage Instructions:

### 1. Download the Repository:

```bash
   git clone https://github.com/hanckjt/openai_api_playground.git
   cd openai_api_playground
```

### 2. Run the Script:

   Linux:

```bash
   chmod +x run.sh
   ./run.sh
```

   Windows:

```bash
   run.bat
```
