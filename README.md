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

## **🛠️ Installation, Hosting ComfyUI on Google Colab & Cloudflare**
### **Use The Above Colab Simply Run It Straight Forward.**

### 🎉 **Now your ComfyUI is live on the internet!** 🚀
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
│── comfyui_colab_file.ipynb  # Colab File
│── tutorial.json            # Example workflow JSON
│── README.md                # This file
│── .gitignore               # Git ignored files
```

---

## **📜 License**
This project is licensed under the **Maniya Gang**.

---

## **💡 Contributors**
- 🚀 **Manish Dhaye** - *Lead Developer*  
- 🎨 **Coming Soon** - *Docs & Testing*  

Feel free to **fork this project** and contribute! 🎯

---
## **🌟 Star this Repo!**
If you found this useful, **please give this repo a ⭐ on GitHub!**  
👇 Click below to star:  
[![GitHub Stars](https://img.shields.io/github/stars/your-username/comfyui-api?style=social)](https://github.com/your-username/comfyui-api)

---
