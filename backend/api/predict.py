from fastapi import APIRouter
from fastapi.responses import Response

from models.request import PredictRequest
from scraper.fetcher import fetch_html

router = APIRouter()


@router.post("/predict")
def predict(request: PredictRequest):

    html = fetch_html(request.url)

    headers = {
        "Content-Disposition": 'attachment; filename="race.html"'
    }

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers=headers
    )}