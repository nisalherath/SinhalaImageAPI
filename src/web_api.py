from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from time import time
from word_utils import generate_word
from image_utils import create_image
from custom_user_utils import process_custom_word  # Import the new helper script

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_DIRECTORY = "static/images"
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

app.mount("/static", StaticFiles(directory="static"), name="static")

REQUESTS_LOG = {}
RATE_LIMIT = 5
TIME_WINDOW = 60

def is_rate_limited(client_ip):
    """Rate limiting function"""
    current_time = time()
    request_times = REQUESTS_LOG.get(client_ip, [])
    request_times = [t for t in request_times if current_time - t < TIME_WINDOW]
    REQUESTS_LOG[client_ip] = request_times

    if len(request_times) >= RATE_LIMIT:
        return True

    REQUESTS_LOG[client_ip].append(current_time)
    return False

@app.get("/generate")
async def generate_image(request: Request):
    """Generate a random Sinhala word and return the image URL"""
    client_ip = request.client.host
    logging.info(f"Request received from IP: {client_ip}")

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    try:
        word = generate_word()
        unique_filename = f"{word}_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(IMAGE_DIRECTORY, unique_filename)

        generated_image_path = create_image(word)
        if generated_image_path and os.path.exists(generated_image_path):
            os.rename(generated_image_path, image_path)
            image_url = f"/static/images/{unique_filename}"
            return {"image_url": image_url}
        else:
            raise HTTPException(status_code=500, detail="Failed to generate image.")

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.post("/generate_custom")
async def generate_custom_image(request: Request, word: str = Form(...)):
    """Generate an image for a user-provided three-letter word"""
    client_ip = request.client.host
    logging.info(f"Custom word request received from IP: {client_ip}, word: {word}")

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    try:
        image_url = process_custom_word(word)
        return {"image_url": image_url}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Error processing custom word '{word}': {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
