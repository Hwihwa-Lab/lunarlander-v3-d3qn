"""
FastAPI Server with WebSocket for Lunar Lander Training & Dashboard.
"""

import asyncio
import os
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from training_manager import TrainingManager, BEST_MODEL_PATH

app = FastAPI(title="Lunar Lander Mission Control", version="2.0")

# Create and configure training manager
manager = TrainingManager()

# Static directories
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    manager.set_event_loop(loop)
    print("[Server] Startup complete. Event loop set.")


@app.get("/")
async def get_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/stats")
async def get_stats():
    return JSONResponse(manager.get_summary_stats())


@app.get("/api/history")
async def get_history():
    return JSONResponse({
        "rewards": manager.rewards_history,
        "moving_avg": manager.moving_avg_history,
        "epsilon": manager.epsilon_history,
        "loss": manager.loss_history,
    })


@app.post("/api/load_best")
async def load_best_checkpoint():
    success = manager.load_best_model()
    return JSONResponse({"status": "loaded" if success else "failed"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Ensure current running event loop is registered
    loop = asyncio.get_running_loop()
    manager.set_event_loop(loop)
    manager.add_subscriber(websocket)
    print(f"[WS] Client connected. Total subscribers: {len(manager.subscribers)}")
    
    # Send initial state and full history
    await websocket.send_json({
        "type": "init",
        "stats": manager.get_summary_stats(),
        "history": {
            "rewards": manager.rewards_history,
            "moving_avg": manager.moving_avg_history,
            "epsilon": manager.epsilon_history,
            "loss": manager.loss_history,
        }
    })

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            print(f"[WS] Received command: {command}, payload: {data}")

            if command == "start":
                manager.start_training()
            elif command == "pause":
                manager.pause_training()
            elif command == "resume":
                manager.resume_training()
            elif command == "stop":
                manager.stop_training()
            elif command == "reset":
                manager.reset_training()
            elif command == "set_mode":
                mode = data.get("mode", "training")
                manager.set_mode(mode)
            elif command == "set_speed":
                speed = float(data.get("speed", 1.0))
                manager.set_speed(speed)
            elif command == "load_best":
                manager.load_best_model()
            elif command == "showcase":
                manager.start_showcase()
            elif command == "manual_start":
                manager.start_manual_mode()
            elif command == "manual_action":
                action = int(data.get("action", 0))
                manager.set_manual_action(action)
            elif command == "get_stats":
                await websocket.send_json({
                    "type": "stats",
                    "stats": manager.get_summary_stats()
                })

    except WebSocketDisconnect:
        manager.remove_subscriber(websocket)
        print("[WS] Client disconnected.")
    except Exception as e:
        manager.remove_subscriber(websocket)
        print(f"[WS] Error: {e}")


def run_server(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run("server:app", host=host, port=port, reload=False, log_level="info")


if __name__ == "__main__":
    run_server()
