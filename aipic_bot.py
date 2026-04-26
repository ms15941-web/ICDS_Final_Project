import requests
from io import BytesIO
from PIL import Image, ImageTk

class AIPicBot:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"

    def generate_url(self, prompt):
        safe_prompt = prompt.replace(" ", "%20")
        return f"{self.base_url}{safe_prompt}"

    def fetch_image(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img_data = response.content
                image = Image.open(BytesIO(img_data))
                image.thumbnail((300, 300))
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error downloading image: {e}")
        return None