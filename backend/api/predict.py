from fastapi import APIRouter

from models.request import PredictRequest
from models.response import PredictResponse
from scraper.fetcher import fetch_html
from scraper.parser import parse_html
from scraper.extractor import extract_info

router = APIRouter()


@router.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    html = fetch_html(request.url)
    soup = parse_html(html)
    info = extract_info(soup)
    
    return PredictResponse(info=info)