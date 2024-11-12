import ray
import os
from ray import serve
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSeq2SeqLM  # Fixed capitalization here
)
from starlette.requests import Request
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the Ray cluster
try:
    ray.init(address="ray://localhost:10001")
    logger.info("Successfully connected to Ray cluster")
except Exception as e:
    logger.error(f"Error connecting to Ray cluster: {str(e)}")
    raise

# Give the cluster a moment to initialize
time.sleep(5)

# Start Ray Serve
try:
    serve.start(detached=True, http_options={"host": "0.0.0.0", "port": 8000})
    logger.info("Ray Serve started successfully")
except Exception as e:
    logger.error(f"Error starting Ray Serve: {str(e)}")
    raise

@serve.deployment(
    name="translator",
    route_prefix="/translate",
    ray_actor_options={"num_cpus": 1, "num_gpus": 0}
)
class Translator:
    def __init__(self):
        logger.info("Initializing Translator deployment")
        try:
            # Download model files first
            model_name = "t5-small"
            logger.info(f"Loading model: {model_name}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Create pipeline
            self.translator = pipeline(
                "translation_en_to_fr",
                model=self.model,
                tokenizer=self.tokenizer
            )
            logger.info("Model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise

    def translate(self, text: str) -> str:
        try:
            model_output = self.translator(text)
            translation = model_output[0]["translation_text"]
            return translation
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise

    async def __call__(self, http_request: Request) -> dict:
        try:
            english_text = await http_request.json()
            logger.info(f"Received translation request: {english_text}")
            translation = self.translate(english_text)
            logger.info(f"Translation completed: {translation}")
            return {"status": "success", "translation": translation}
        except Exception as e:
            logger.error(f"Request handling error: {str(e)}")
            return {"status": "error", "message": str(e)}

# Deploy the service
try:
    translator_deployment = Translator.bind()  # Create deployment
    serve.run(translator_deployment)          # Deploy the service
    logger.info("Successfully deployed translation service")
except Exception as e:
    logger.error(f"Error deploying service: {str(e)}")
    raise

if __name__ == "__main__":
    # Keep the script running
    while True:
        time.sleep(1)