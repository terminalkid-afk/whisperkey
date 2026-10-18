import os
import requests
from tqdm import tqdm

class ModelManager:
    """Handles downloading and verifying Whisper models."""
    
    MODELS = {
        "tiny.en": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin",
        "base.en": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin",
        "small.en": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin",
    }

    @staticmethod
    def ensure_model(model_name: str):
        """Downloads the model if it doesn't exist in the assets folder."""
        if model_name not in ModelManager.MODELS:
            raise ValueError(f"Unsupported model: {model_name}")

        url = ModelManager.MODELS[model_name]
        filename = f"ggml-{model_name}.bin"
        path = os.path.join("assets", filename)

        if os.path.exists(path):
            return path

        print(f"Downloading {model_name} model... this may take a minute.")
        os.makedirs("assets", exist_ok=True)
        
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(path, 'wb') as f, tqdm(
            desc=model_name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        
        return path
