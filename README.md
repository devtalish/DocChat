<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/BackyardML/DocChat/b3098fdcde3da5ef916d89cc0bea4be90de545dd/docchat.svg" width="600"/>
    <br>
<p>

DocChat is a Python application that allows users to interact with documents using natural language. It leverages LangChain, Gradio, and the OpenAI API to create a chat interface for document-based conversations.

## Installation

To get started with DocChat, follow these steps:

1. Clone the repository to your local machine:
   ```commandline
   git clone https://github.com/BackyardML/DocChat.git
   ```
2. Change the directory to the project folder:
   ```commandline
   cd DocChat
   ```
3. Install Poetry (if you haven't already):
   ```commandline
   pip install poetry
   ```
4. Install project dependencies using Poetry:
   ```commandline
   poetry install
   ```
5. Obtain an API key from [OpenAI](https://openai.com/).
6. Configure `DOCCHAT_USERNAME` and `DOCCHAT_PASSWORD` in the environment before starting the app. These credentials protect the Gradio interface.

## Usage

### Running DocChat

You can run DocChat by executing the app.py script:

```commandline
poetry run python app.py
```

This will start a Gradio web application with a chat interface that you can access through your web browser.

### Interacting with DocChat

1. Launch the Gradio application by running the app.py script.
2. Sign in with the configured DocChat credentials.
3. Enter your OpenAI API key in the password-masked "OpenAI API Key" textbox.
4. Upload one or more PDF or TXT documents using the file uploader.
5. Click the "Run" button to create a chatbot for the uploaded documents.
6. Start chatting with the documents by typing messages in the "Message" textbox.
7. To clear the chat history, click the "Clear" button.

## Contact

If you have any questions or need assistance, feel free to contact me at patrik@backyardml.se
