from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
import os
import uuid
import logging
from time import time
from word_utils import generate_word
from image_utils import create_image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Allow CORS for the React app (by default, React runs on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Ensure the image directory exists
IMAGE_DIRECTORY = "static/images"  # Update to a static directory for public access
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rate limiter setup
REQUESTS_LOG = {}  # Stores request timestamps per IP
RATE_LIMIT = 5  # Max requests per minute
TIME_WINDOW = 60  # In seconds

def is_rate_limited(client_ip):
    """Basic rate-limiting function to prevent spam requests"""
    current_time = time()
    request_times = REQUESTS_LOG.get(client_ip, [])

    # Remove outdated requests from the log
    request_times = [t for t in request_times if current_time - t < TIME_WINDOW]
    REQUESTS_LOG[client_ip] = request_times

    if len(request_times) >= RATE_LIMIT:
        return True

    REQUESTS_LOG[client_ip].append(current_time)
    return False

@app.get("/generate")
async def generate_image(request: Request):
    """Generate a Sinhala word and return the image URL"""
    client_ip = request.client.host  # Get user IP address
    logging.info(f"Request received from IP: {client_ip}")

    if is_rate_limited(client_ip):
        logging.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    try:
        word = generate_word()
        unique_filename = f"{word}_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(IMAGE_DIRECTORY, unique_filename)

        generated_image_path = create_image(word)
        if generated_image_path and os.path.exists(generated_image_path):
            os.rename(generated_image_path, image_path)
            logging.info(f"Generated image for word '{word}': {image_path}")

            # Return the URL of the generated image
            image_url = f"/static/images/{unique_filename}"
            return {"image_url": image_url}
        else:
            logging.error("Failed to generate image.")
            raise HTTPException(status_code=500, detail="Failed to generate image.")

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
