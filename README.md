🚀 ComfyUI API - Flask Integration with Google Colab & Cloudflare

🔗 Automate Stable Diffusion Image Generation using Flask & ComfyUI

🚀 This project integrates ComfyUI (Stable Diffusion) with Flask API,
hosted via Google Colab + Cloudflare.It enables real-time AI image
generation, queueing, and retrieval via API endpoints.

📀 Features

✅ Deploy ComfyUI on Google Colab with Cloudflare✅ Flask API for
Automated Image Generation✅ Queue Prompts, Track Progress, Fetch
Images✅ Postman Testing Guide✅ Supports Image Uploading & Custom
Prompts

🛠️ Installation

1️⃣ Clone the Repository

git clone https://github.com/your-username/comfyui-api.git cd
comfyui-api

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the Flask Server

python app.py

Your API will now be accessible at:🔗 http://127.0.0.1:5000

💼 Hosting ComfyUI on Google Colab & Cloudflare

To run ComfyUI on Google Colab, follow these steps:

Open Google Colab → Create a new notebook

Run the following commands:

!git clone https://github.com/comfyanonymous/ComfyUI.git %cd ComfyUI
!pip install -r requirements.txt

Start the ComfyUI Server:

!python main.py

Expose API via Cloudflare:

!apt install cloudflared !cloudflared tunnel \--url
http://127.0.0.1:8188

Copy the generated Cloudflare URL (e.g.,
https://your-cloudflare-link.trycloudflare.com)

🎉 Now your ComfyUI is live on the internet! 🚀

🔗 API Endpoints

Endpoint

Method

Purpose

/connect

GET

Connects to WebSocket

/queue_prompt

POST

Queues a prompt

/get_history

GET

Fetches all past prompts

/track_progress

GET

Tracks only ongoing prompts

/get_image

GET

Fetches the generated image

/generate_image

POST

Full workflow (Queue → Track → Fetch Image)

/upload_image

POST

Uploads an input image

🔮 Project Structure

comfyui-api/ │── assets/ \# Store animations/gifs for the README │──
app.py \# Flask API code │── requirements.txt \# Dependencies │──
tutorial.json \# Example workflow JSON │── README.md \# This file │──
.gitignore \# Git ignored files

💼 License

This project is licensed under the MIT License.
