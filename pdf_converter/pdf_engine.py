from playwright.async_api import async_playwright
import tempfile
import uuid
import os

async def html_to_pdf(
    html: str,
    print_background=True,
    wait_for_selector=None,
    scale=1.0,
    viewport_width=1280,
    viewport_height=800
):
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"{uuid.uuid4()}.pdf")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = await browser.new_page()

        if viewport_width and viewport_height:
            await page.set_viewport_size({"width": viewport_width, "height": viewport_height})

        await page.emulate_media(media="screen")

        await page.set_content(html, wait_until="networkidle")

        if wait_for_selector:
            await page.wait_for_selector(wait_for_selector, timeout=15000)

        await page.pdf(
            path=file_path,
            format="A4",
            scale=scale,
            print_background=print_background,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )

        await browser.close()

    return file_path