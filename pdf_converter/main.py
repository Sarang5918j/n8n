from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from models import PDFRequest
from pdf_engine import html_to_pdf
from worker import send_callback

app = FastAPI(title="HTML to PDF Service", version="1.0")

@app.post("/convert")
async def convert_pdf(req: PDFRequest, background_tasks: BackgroundTasks):
    pdf_path = await html_to_pdf(
        html=req.html,
        print_background=req.print_background,
        wait_for_selector=req.wait_for_selector,
        scale=req.scale,
        viewport_width=req.viewport_width,
        viewport_height=req.viewport_height
    )

    # If callback provided → async webhook mode
    if req.callback_url:
        background_tasks.add_task(
            send_callback,
            str(req.callback_url),
            pdf_path,
            req.filename
        )
        return {
            "status": "processing",
            "message": "PDF is being generated and will be sent to callback URL"
        }

    # Otherwise return file directly (n8n compatible)
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=req.filename
    )