from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from services.formatter import render_report_html
from weasyprint import HTML
import io

router = APIRouter()

@router.post("/api/download/pdf")
async def download_pdf(request: Request):
    try:
        data = await request.json()
        html = render_report_html(data)
        pdf_io = io.BytesIO()
        HTML(string=html).write_pdf(target=pdf_io)
        pdf_io.seek(0)
        return StreamingResponse(
            content=pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=intrix_report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 