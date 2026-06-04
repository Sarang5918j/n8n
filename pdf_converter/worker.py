import httpx
import os

async def send_callback(callback_url: str, file_path: str, filename: str):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/pdf")}

            async with httpx.AsyncClient(timeout=60) as client:
                await client.post(
                    callback_url,
                    files=files,
                    data={"status": "success"}
                )
    except Exception as e:
        # log error (replace with real logging)
        print("Callback failed:", str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)