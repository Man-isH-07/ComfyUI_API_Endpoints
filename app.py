import json
from flask import Flask, request, jsonify, send_file
import uuid
import websocket
import requests
import time
import io

app = Flask(__name__)

# Establish WebSocket Connection
@app.route('/connect', methods=['GET'])
def connect():
    """Establish a WebSocket connection to ComfyUI."""
    try:
        server_address = "situations-designing-submitting-utah.trycloudflare.com"
        client_id = str(uuid.uuid4())

        ws = websocket.WebSocket()
        ws.connect(f"wss://{server_address}/ws?clientId={client_id}")

        return jsonify({
            "message": "WebSocket connection established",
            "client_id": client_id,
            "server_address": server_address
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Queue a Prompt
@app.route('/queue_prompt', methods=['POST'])
def queue_prompt_route():
    """API route to queue a prompt."""
    try:
        data = request.get_json()
        server_address = data.get("server_address")
        client_id = data.get("client_id")
        prompt = data.get("prompt")

        if not prompt or not client_id or not server_address:
            return jsonify({"error": "Missing required parameters"}), 400

        response = queue_prompt(server_address, client_id, prompt)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def queue_prompt(server_address, client_id, prompt):
    """Sends a workflow JSON prompt to ComfyUI."""
    try:
        payload = {"prompt": prompt, "client_id": client_id}

        response = requests.post(
            f"http://{server_address}/prompt",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Fetch Generation History
@app.route('/get_history', methods=['GET'])
def get_history():
    """Fetches all previously queued prompts and their status."""
    try:
        server_address = request.args.get("server_address")

        if not server_address:
            return jsonify({"error": "Missing required parameters"}), 400

        response = requests.get(f"http://{server_address}/history")

        try:
            history_data = response.json()
            return jsonify({"all_prompts": history_data}), response.status_code
        except requests.exceptions.JSONDecodeError:
            return jsonify({"error": "Invalid JSON response", "response_text": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# track progress
@app.route('/track_progress/<prompt_id>', methods=['GET'])
def track_progress_route(prompt_id):
    """Tracks the progress of an ongoing prompt until completion."""
    try:
        server_address = request.args.get("server_address")

        if not server_address:
            return jsonify({"error": "Missing required parameters"}), 400

        counter = 1  
        while True:
            response = requests.get(f"http://{server_address}/history/{prompt_id}")

            try:
                history_data = response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Invalid JSON response from `/history`")
                return {"error": "Invalid JSON response", "response_text": response.text}

            print(f"Debug: Full history response → {json.dumps(history_data, indent=2)}")

            if prompt_id not in history_data:
                print(f"Waiting... {counter} seconds (Prompt ID {prompt_id} not found yet)")
                counter += 1
                time.sleep(1)
                continue

            status = history_data[prompt_id].get("status", {}).get("completed", False)
            if status:
                print(f"Image generation completed in {counter} seconds!")
                return jsonify({
                    "status": "completed",
                    "message": f"Prompt {prompt_id} completed in {counter} seconds"
                })

            print(f"Still processing... {counter} seconds elapsed")
            counter += 1
            time.sleep(1)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def track_progress(server_address, prompt_id):
    """Tracks progress of an ongoing prompt until completion."""
    try:
        counter = 1  
        while True:
            response = requests.get(f"http://{server_address}/history/{prompt_id}")

            try:
                history_data = response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Invalid JSON response from `/history`")
                return {"error": "Invalid JSON response", "response_text": response.text}

            print(f"Debug: Full history response → {json.dumps(history_data, indent=2)}")

            if prompt_id not in history_data:
                print(f"Waiting... {counter} seconds (Prompt ID {prompt_id} not found yet)")
                counter += 1
                time.sleep(1)
                continue

            status = history_data[prompt_id].get("status", {}).get("completed", False)
            if status:
                print(f"Image generation completed in {counter} seconds!")
                return history_data

            print(f"Still processing... {counter} seconds elapsed")
            counter += 1
            time.sleep(1)

    except Exception as e:
        return {"error": str(e)}


# Fetch Generated Image
@app.route('/get_image', methods=['GET'])
def get_image_route():
    """API route to fetch a generated image."""
    try:
        filename = request.args.get("filename")
        server_address = request.args.get("server_address")

        if not filename or not server_address:
            return jsonify({"error": "Missing filename or server_address"}), 400

        return get_image(server_address, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_image(server_address, filename):
    """Fetches the generated image from ComfyUI."""
    try:
        params = {"filename": filename, "subfolder": "", "type": "output"}
        response = requests.get(f"http://{server_address}/view", params=params)

        if response.status_code == 200:
            return send_file(
                io.BytesIO(response.content),
                mimetype="image/png",
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({"error": "Image not found"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Full Workflow in One API Call
@app.route('/generate_image', methods=['POST'])
def generate_image():
    """Handles full process: Queue Prompt → Track Progress → Get Image."""
    try:
        if request.data:
            data = request.get_json()
        else:
            with open("tutorial.json", "r") as file:
                data = json.load(file)

        server_address = data.get("server_address")
        client_id = data.get("client_id")
        prompt = data.get("prompt")

        if not prompt or not client_id or not server_address:
            return jsonify({"error": "Missing required parameters"}), 400

        queue_response = queue_prompt(server_address, client_id, prompt)
        prompt_id = queue_response.get("prompt_id")

        if not prompt_id:
            return jsonify({"error": "Failed to get prompt_id", "queue_response": queue_response}), 500

        print(f"Tracking progress for Prompt ID: {prompt_id}")

        track_status = track_progress(server_address, prompt_id)

        if "error" in track_status:
            return jsonify(track_status), 500

        print(f"Image generation completed: {prompt_id}")

        filename = track_status[prompt_id]["outputs"]["9"]["images"][0]["filename"]

        return get_image(server_address, filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Upload image
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"} 

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Uploads an image to the ComfyUI server."""
    try:
        print("Received FORM data:", request.form)
        print("Received FILES:", request.files)

        server_address = request.form.get("server_address")
        filename = request.form.get("filename")
        folder_type = request.form.get("folder_type", "input")
        image_type = request.form.get("image_type", "image")
        overwrite = request.form.get("overwrite", "false").lower() == "true"

        if not server_address or not filename or 'image' not in request.files:
            return jsonify({
                "error": "Missing required parameters",
                "server_address": server_address,
                "filename": filename,
                "folder_type": folder_type,
                "image_type": image_type,
                "overwrite": overwrite,
                "files_received": list(request.files.keys())
            }), 400

        file = request.files['image']

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG, GIF, BMP, TIFF, and WEBP are allowed."}), 400

        files = {
            "image": (filename, file, f"image/{filename.rsplit('.', 1)[1].lower()}")
        }
        data = {
            "type": folder_type,
            "overwrite": str(overwrite).lower()
        }

        url = f"http://{server_address}/upload/{image_type}"
        response = requests.post(url, files=files, data=data)

        return response.json()  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
