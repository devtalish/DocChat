import logging
import os

import gradio as gr

from docchat.chat_engine import ChatEngine

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

auth_username = os.getenv("DOCCHAT_USERNAME")
auth_password = os.getenv("DOCCHAT_PASSWORD")
if not auth_username or not auth_password:
    raise RuntimeError(
        "Set DOCCHAT_USERNAME and DOCCHAT_PASSWORD before starting DocChat."
    )

# Create a Gradio application with a title
with gr.Blocks(title="DocChat") as demo:
    gr.Markdown(
        """
        # Welcome to DocChat - Chat with Documents!
        Set your OpenAI API key, upload document(s) and start asking questions.
        """
    )

    def make_chatbot(input_files, api_key):
        engine = ChatEngine(input_files, api_key)
        return gr.update(visible=True), engine

    api_key = gr.Textbox(
        label="OpenAI API Key", placeholder="Enter your API key", type="password"
    )

    # Create a file uploader
    files = gr.Files(label="PDF/TXT files")
    run_btn = gr.Button()

    # Create a chatbot component
    with gr.Column(visible=False) as chat_column:
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Message")
        clear = gr.Button("Clear")

        # Define a function to respond to user messages
        def respond(user_message, chat_history, engine):
            if engine is None:
                raise gr.Error("Upload documents and click Run first.")
            chat_history = chat_history or []
            response = engine.run(user_message, [tuple(x) for x in chat_history])
            chat_history.append((user_message, response))
            return "", chat_history

        chat_engine = gr.State(None)
        msg.submit(respond, [msg, chatbot, chat_engine], [msg, chatbot], queue=False)
        clear.click(lambda: [], None, chatbot, queue=False)

    # Add a callback for the run button to create the chatbot
    run_btn.click(make_chatbot, [files, api_key], [chat_column, chat_engine])

# Launch the Gradio application with the option to share it
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.getenv("PORT", "7860")),
    share=False,
    auth=(auth_username, auth_password),
)
