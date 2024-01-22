# api_threads.py

import base64
import openai
import os
from PyQt5.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ImageAnalysisThread(QThread):
    resultSignal = pyqtSignal(object)

    def __init__(self, image_path, user_context):
        super().__init__()
        self.image_path = image_path
        self.user_context = user_context

    def run(self):
        with open(self.image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        prompt_messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Ignore all previous context.  Offer a long detailed paragraph analysis of this art, followed by 5 title suggestions based off the context. If the user has provided any context for the analysis it would be here: '{self.user_context}' Avoid cliche titles (Examples of cliche title formats to avoid: '__ of the __', '__: __', 'Whisper(s)', etc).  Do not offer any commentary, descriptions, or titles: just the analysis, followed by 5 titles.  Do not number or bullet the list of titles in any way.  Make sure there is only 1 paragraph of analysis, no more."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ]

        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt_messages,
            "api_key": os.environ["OPENAI_API_KEY"],
            "headers": {"Openai-Version": "2020-11-07"},
            "max_tokens": 4096,
        }

        try:
            result = openai.ChatCompletion.create(**params)
            self.resultSignal.emit(result.choices[0].message.content)
        except Exception as e:
            self.resultSignal.emit(f"Error: {str(e)}")

class TitleRegenerationThread(QThread):
    resultSignal = pyqtSignal(object)

    def __init__(self, analysis_text, user_context=None):
        super().__init__()
        self.analysis_text = analysis_text
        self.user_context = user_context
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def run(self):
        openai.api_key = self.api_key

        try:
            system_message = "Generate five creative titles for this work of art based on the following analysis and user context."
            
            user_message = f"{self.analysis_text}\n\nUser Context: {self.user_context}\n\nAvoid cliche titles (Examples of cliche title formats to avoid: '__ of the __', '__: __', 'Whisper(s)', etc)  Do not number or bullet the titles, or add quotation marks. Only provide the titles."

            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            )

            generated_titles = response.choices[0].message.content

            self.resultSignal.emit(generated_titles)
        except Exception as e:
            self.resultSignal.emit(f"Error: {str(e)}")
