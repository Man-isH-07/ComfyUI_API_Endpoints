# app/api/routes.py
import uuid
import json
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from app.services.comfyui import queue_prompt, track_progress, get_image
from app.models.schemas import ComfyUIPrompt, HistoryResponse, ProgressResponse, ImageResponse
import logging
import io
import requests
import os

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Visit /docs# for the frontend"}

@router.get("/connect")
async def connect():
    """Establish a WebSocket connection to ComfyUI."""
    try:
        server_address = "portfolio-correct-healthcare-actress.trycloudflare.com"
        client_id = str(uuid.uuid4())
        return {
            "message": "WebSocket connection established",
            "client_id": client_id,
            "server_address": server_address
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/queue_prompt")
async def queue_prompt_route(prompt_data: ComfyUIPrompt = None, request: Request = None):
    """API route to queue a prompt."""
    try:
        if not prompt_data:
            tutorial_path = "tutorial.json"
            if os.path.exists(tutorial_path):
                with open(tutorial_path, "r") as file:
                    data = json.load(file)
                    prompt_data = ComfyUIPrompt(
                        prompt=data["prompt"],
                        client_id=data["client_id"],
                        server_address=data["server_address"]
                    )
            else:
                raise HTTPException(status_code=400, detail="No request data and tutorial.json not found")

        server_address = prompt_data.server_address
        client_id = prompt_data.client_id
        prompt = {key: value.dict() for key, value in prompt_data.prompt.items()}

        if not prompt or not client_id or not server_address:
            raise HTTPException(status_code=400, detail="Missing required parameters")

        response = queue_prompt(server_address, client_id, prompt)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_history")
async def get_history(server_address: str = Query(...)):
    """Fetches all previously queued prompts and their status."""
    try:
        response = requests.get(f"http://{server_address}/history")
        response.raise_for_status()
        return HistoryResponse(all_prompts=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track_progress/{prompt_id}")
async def track_progress_route(prompt_id: str, server_address: str = Query(...)):
    """Tracks the progress of an ongoing prompt until completion."""
    try:
        progress = track_progress(server_address, prompt_id)
        if "error" in progress:
            raise HTTPException(status_code=500, detail=progress["error"])
        return ProgressResponse(status="completed", message=f"Prompt {prompt_id} completed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_image")
async def get_image_route(filename: str = Query(...), server_address: str = Query(...)):
    """API route to fetch a generated image."""
    try:
        logger.info(f"Received GET request for image: filename={filename}, server_address={server_address}")
        image_data = get_image(server_address, filename)
        if "error" in image_data:
            logger.error(f"Error from get_image function: {image_data['error']}")
            raise HTTPException(status_code=500, detail=image_data["error"])
        logger.info(f"Successfully retrieved image data, returning StreamingResponse with filename: {image_data['filename']}")
        return StreamingResponse(
            io.BytesIO(image_data["image_data"]),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={image_data['filename']}"}
        )
    except HTTPException as e:
        logger.error(f"HTTP Exception in get_image route: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_image route: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch image: {str(e)}")

@router.post("/generate_image")
async def generate_image(prompt_data: ComfyUIPrompt = None, request: Request = None):
    """Handles full process: Queue Prompt → Track Progress → Get Image."""
    try:
        if not prompt_data:
            tutorial_path = "tutorial.json"
            if os.path.exists(tutorial_path):
                with open(tutorial_path, "r") as file:
                    data = json.load(file)
                    prompt_data = ComfyUIPrompt(
                        prompt=data["prompt"],
                        client_id=data["client_id"],
                        server_address=data["server_address"]
                    )
            else:
                raise HTTPException(status_code=400, detail="No request data and tutorial.json not found")

        prompt = {key: value.dict() for key, value in prompt_data.prompt.items()}
        queue_response = queue_prompt(prompt_data.server_address, prompt_data.client_id, prompt)
        prompt_id = queue_response.get("prompt_id")
        if not prompt_id:
            raise HTTPException(status_code=500, detail="Failed to get prompt_id")

        logger.info(f"Tracking progress for Prompt ID: {prompt_id}")
        track_status = track_progress(prompt_data.server_address, prompt_id)
        if "error" in track_status:
            raise HTTPException(status_code=500, detail=track_status["error"])

        filename = track_status[prompt_id]["outputs"]["9"]["images"][0]["filename"]
        image_data = get_image(prompt_data.server_address, filename)
        if "error" in image_data:
            raise HTTPException(status_code=500, detail=image_data["error"])
        logger.info(f"Returning image with filename: {image_data['filename']}")
        return StreamingResponse(
            io.BytesIO(image_data["image_data"]),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={image_data['filename']}"}
        )
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/upload_image")
async def upload_image(request: Request):
    """Uploads an image to the ComfyUI server."""
    try:
        form_data = await request.form()
        server_address = form_data.get("server_address")
        filename = form_data.get("filename")
        folder_type = form_data.get("folder_type", "input")
        image_type = form_data.get("image_type", "image")
        overwrite = form_data.get("overwrite", "false").lower() == "true"
        image_file = form_data.get("image")

        if not server_address or not filename or not image_file:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Missing required parameters",
                    "server_address": server_address,
                    "filename": filename,
                    "folder_type": folder_type,
                    "image_type": image_type,
                    "overwrite": overwrite,
                    "files_received": list(form_data.keys())
                }
            )

        if not allowed_file(filename):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG, GIF, BMP, TIFF, and WEBP are allowed.")

        files = {"image": (filename, await image_file.read(), f"image/{filename.rsplit('.', 1)[1].lower()}")}
        data = {"type": folder_type, "overwrite": str(overwrite).lower()}

        url = f"http://{server_address}/upload/{image_type}"
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))