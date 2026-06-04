from pydantic import BaseModel, HttpUrl
from typing import Optional

class PDFRequest(BaseModel):
    html: str
    filename: Optional[str] = "output.pdf"
    callback_url: Optional[HttpUrl] = None
    wait_for_selector: Optional[str] = None
    print_background: bool = True
    scale: Optional[float] = 1.0
    viewport_width: Optional[int] = 1280
    viewport_height: Optional[int] = 800