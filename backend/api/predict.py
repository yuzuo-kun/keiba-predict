from fastapi import APIRouter

from analyzer.calculator import calculate
from models.request import PredictRequest
from models.response import PredictResponse
from scraper.extractor import extract_info
from scraper.fetcher import fetch_html
from scraper.parser import parse_html

router = APIRouter()


@router.post("/predict")
def predict(request: PredictRequest):

    html = fetch_html(request.url)
    soup = parse_html(html)
    info = extract_info(soup)

    distance = calculate(info)

    return PredictResponse(
        info=info,
        distance=distance
    )