# 🚀 ComfyUI API - Flask Integration with Google Colab & Cloudflare  
![ComfyUI API Workflow](https://github.com/Man-isH-07/ComfyUI_API_Endpoints/blob/main/assets/comfyui-banner.gif)

### **🔗 Automate Stable Diffusion Image Generation using Flask & ComfyUI**
🚀 This project integrates **ComfyUI (Stable Diffusion)** with **Flask API**, hosted via **Google Colab + Cloudflare**.  
It enables **real-time AI image generation**, queueing, and retrieval **via API endpoints**.

---

## **📌 Features**
✅ **Deploy ComfyUI on Google Colab with Cloudflare**  
✅ **Flask API for Automated Image Generation**  
✅ **Queue Prompts, Track Progress, Fetch Images**  
✅ **Postman Testing Guide**  
✅ **Supports Image Uploading & Custom Prompts**  

![ComfyUI API in Action](https://github.com/Man-isH-07/ComfyUI_API_Endpoints/blob/main/assets/comfyui-demo.gif)

---

## **🛠️ Installation**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/comfyui-api.git
cd comfyui-api
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Flask Server**
```bash
python app.py
```
Your API will now be accessible at:  
🔗 **http://127.0.0.1:5000**

---

## **📡 Hosting ComfyUI on Google Colab & Cloudflare**
To run ComfyUI on **Google Colab**, follow these steps:

1. **Open Google Colab** → Create a new notebook  
2. **Run the following commands**:
   ```python
   !git clone https://github.com/comfyanonymous/ComfyUI.git
   %cd ComfyUI
   !pip install -r requirements.txt
   ```
3. **Start the ComfyUI Server**:
   ```python
   !python main.py
   ```
4. **Expose API via Cloudflare**:
   ```python
   !apt install cloudflared
   !cloudflared tunnel --url http://127.0.0.1:8188
   ```
5. Copy the generated **Cloudflare URL** (e.g., `https://your-cloudflare-link.trycloudflare.com`)

🎉 **Now your ComfyUI is live on the internet!** 🚀

---

## **🔗 API Endpoints**
| **Endpoint**          | **Method** | **Purpose** |
|----------------------|----------|------------|
| `/connect`         | `GET`    | Connects to WebSocket |
| `/queue_prompt`    | `POST`   | Queues a prompt |
| `/get_history`     | `GET`    | Fetches all past prompts |
| `/track_progress`  | `GET`    | Tracks only ongoing prompts |
| `/get_image`       | `GET`    | Fetches the generated image |
| `/generate_image`  | `POST`   | Full workflow (Queue → Track → Fetch Image) |
| `/upload_image`    | `POST`   | Uploads an input image |

---

## **📂 Project Structure**
```
comfyui-api/
│── assets/                 # Store animations/gifs for the README
│── app.py                  # Flask API code
│── requirements.txt         # Dependencies
│── tutorial.json            # Example workflow JSON
│── README.md                # This file
│── .gitignore               # Git ignored files
```

---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **💡 Contributors**
- 🚀 **Your Name** - *Lead Developer*  
- 🎨 **Contributor Name** - *Docs & Testing*  

Feel free to **fork this project** and contribute! 🎯

---
## **🌟 Star this Repo!**
If you found this useful, **please give this repo a ⭐ on GitHub!**  
👇 Click below to star:  
[![GitHub Stars](https://img.shields.io/github/stars/your-username/comfyui-api?style=social)](https://github.com/your-username/comfyui-api)

---
