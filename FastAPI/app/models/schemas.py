from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class PromptNode(BaseModel):
    inputs: Dict[str, Any]  # Allow any input structure
    class_type: str
    _meta: Dict[str, str]

class ComfyUIPrompt(BaseModel):
    prompt: Dict[str, PromptNode]
    client_id: str
    server_address: str

class HistoryResponse(BaseModel):
    all_prompts: Dict[str, Dict]

class ProgressResponse(BaseModel):
    status: str
    message: str

class ImageResponse(BaseModel):
    filename: str
    image_data: bytes