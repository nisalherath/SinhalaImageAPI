<hr>

<div align="center">

# Random 3-Letter Sinhala Word Generator API
  <a href="https://nisal.lk/word-generation" target="_blank" rel="noopener noreferrer">
    <img src="https://sinhala-api.vercel.app/api/SinhalaAPI" width="350" height="200" style="border-radius: 15px;" alt="Visit Nisal.lk" />
  </a>
</div>
<br><br><br>

This custom API generates random 3-letter Sinhala words and converts them into images dynamically. Built with Python and FastAPI, it creates unique images for each word and provides direct access to them. To ensure smooth performance and prevent spam, the API includes rate limiting. It also supports CORS, making it easy to integrate with frontend applications like React.

<br><br><br>

# Table of Contents 📑  
<hr>

- [Project Overview](#project-overview-)  
- [Setting Up the API](#-setting-up-the-api)  
  - [Install FastAPI and Uvicorn](#1%EF%B8%8F⃣-install-fastapi-and-uvicorn)  
  - [Create a Basic FastAPI App](#2%EF%B8%8F⃣-create-a-basic-fastapi-app)  
  - [Run the API](#3%EF%B8%8F⃣-run-the-api)  
- [Handling CORS for Frontend Integration](#-handling-cors-for-frontend-integration)  
  - [Install CORS Middleware](#1%EF%B8%8F⃣-install-cors-middleware)  
  - [Add CORS Support in `main.py`](#2%EF%B8%8F⃣-add-cors-support-in-mainpy)  
  - [Restart and Test](#3%EF%B8%8F⃣-restart-and-test)
- [File Structure](#file-structure-)
- [Generating Words and Images](#-generating-words-and-images)  
  - [Word Generation Process](#-word-generation-process)  
  - [Image Generation (Using GTK4 for Better Rendering)](#%EF%B8%8F-image-generation-using-gtk4-for-better-rendering)  
- [Api Setup & Endpoints](#-api-setup--endpoints)  
- [Installation & Setup](#-installation--setup)  
- [What’s Next?](#-whats-next)  
- [License](#license-)  

<br>

# Project Overview 🛞
- Generates random 3-letter Sinhala words.
- Converts words into dynamically created images.
- Built with **FastAPI** for high performance.
- Implements **rate limiting** to prevent spam.
- Supports **CORS** for seamless frontend integration.
- Serves generated images via a public directory.

<br><br><br>

---
# Example API Setup for Beginners

## 🔧 Setting Up the API

### 1️⃣ Install FastAPI and Uvicorn
To get started, install FastAPI and Uvicorn, which is an ASGI server to run the API:

```sh
pip install fastapi uvicorn
```

### 2️⃣ Create a Basic FastAPI App
Create a file named `main.py` and add the following code:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

### 3️⃣ Run the API
Use the following command to run your API:

```sh
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser or test it with:

```sh
curl http://127.0.0.1:8000
```

The `--reload` flag enables automatic reloading whenever you make code changes.

<br><br><br>

---

## 🌐 Handling CORS for Frontend Integration
If you're integrating this API with a frontend (e.g., a React app), you'll need to handle CORS.

### 1️⃣ Install CORS Middleware
```sh
pip install fastapi[all]
```

### 2️⃣ Add CORS Support in `main.py`
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nisal.lk/"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3️⃣ Restart and Test
```sh
uvicorn main:app --reload
```

<br><br><br><br><br><br>

<div align="center"> 

---
# My API setup for
## `This Repo`

</div>

---

## File Structure 📖

`The project directory is structured as follows:`



### Project Folder (src)

| **File/Folder**      | **Description**                                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **font/**            | Contains the Fonts needed for the Image Processing. (`NotoSansSinhala-Regular.ttf`).                                        |
| **watermark/**       | Contains the watermarks needed for the Image Post Processing. (`Watermark.png`).                                            |
| **word_utils.py**    | Generates a Random 3 letter word Based on the Logic that is Implemented in this.                                            |
| **image_utils.py**   | Gets the random word generated from `image_utils.py` and process it as an Image by adding a Background Color & a Watermark. |
| **web_api.py**       | All the API call handling ans CORS handling happens in this file. (Your `main` File)                                        |
| **requirements.txt** | A file listing all the dependencies (such as `Pillow`, `fastapi` & `uvicorn`.) needed to run the project.                   |
| **README.md**        | Documentation for the project, including installation and usage instructions.                                               |


<br><br><br>
<hr>

# 🎨 Generating Words and Images

`This API dynamically generates 3-letter Sinhala words and converts them into images.`

---


## 🔠 Word Generation Process

<div align="center">
<img src="https://res.cloudinary.com/dlnhogbjy/image/upload/v1740543269/Word_Utils_zxxezv.webp"  />
</div>

| Process Step                   | Description  |
|--------------------------------|-------------|
| **Sinhala Consonants & Vowels** | The words follow structured combinations: <br> - The first letter is a consonant. <br> - The second letter may be a consonant followed by a vowel sign. <br> - The third letter is a consonant, optionally with a vowel sign. |
| **Two-Letter Combinations**     | Introduces realistic word structures. |
| **Word Validation**             | Ensures generated words are valid in Sinhala. |


<br><br><br>

---

## 🖼️ Image Generation (Using GTK4 for Better Rendering)

<div align="center">
<img src="https://res.cloudinary.com/dlnhogbjy/image/upload/v1740543269/Word_Utils_zxxezv.webp"  />
</div>

`The API uses Python's **PIL (Pillow)** library to generate word images.`


| Process Step            | Description                                                           |
|-------------------------|-----------------------------------------------------------------------|
| **Background Creation** | A vibrant gradient background is generated for each image.            |
| **Text Rendering**      | The word is positioned centrally for clear visibility.                |
| **Watermarking**        | Adds a watermark and version text to maintain authenticity.           |
| **Final Image Output**  | The image is saved as a high-quality JPEG file in a public directory. |

<br><br><br>

---

# 🔛 Api Setup & Endpoints

## Code Overview of `web_api.py`

| **Feature**            | **Description**                                                                                                                        |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| **FastAPI Setup**      | The FastAPI app is configured to handle incoming requests, generate Sinhala words, and create images.                                  |
|                        | **CORS Middleware** is added to allow requests from any origin, typically used for handling React frontend requests.                   |
|                        | The app serves static files, such as the generated images, from the `static/images` directory.                                         |
| **Image Generation**   | A random Sinhala word is generated using the `generate_word()` function.                                                               |
|                        | The word is passed to the `create_image()` function, which generates an image and saves it with a unique filename.                     |
|                        | The generated image is renamed and stored in the `static/images` directory.                                                            |
| **Rate Limiting**      | The service limits the number of requests a client can make in one minute to prevent abuse.                                            |
|                        | If a client exceeds the rate limit, they will receive a `429` status code with a message to try again later.                           |
| **Routes / Endpoints** | **`/generate`**: The main endpoint that generates a random Sinhala word, creates an image, and returns the URL of the generated image. |


---
# 🚀 Installation & Setup

1. Clone the repository:

```

git clone https://github.com/nisalherath/SinhalaImageAPI.git

```

2. Install dependencies:

```

pip install -r requirements.txt

```

3. Run the FastAPI app

```

python3 web_api.py

```



---

## 🔗 What's Next?
Now that your FastAPI project is up and running, you can:
- Add more endpoints.
- Implement database support.
- Further optimize image generation.
- Deploy the API for public use.

<br>

---

## License 😽😽

This project is licensed under the [MIT License](LICENSE).

### Copyright (c) 2025 Nisal Herath

<hr>



<div align="center">

`This repository is maintained by Nisal Herath. All rights reserved.`
<br>
`By using this code, you agree to the terms outlined in the LICENSE file.`


### [nisal@nisal.lk](mailto:anushka@nisal.lk)

### [nisal.lk](https://nisal.lk)
</div>
