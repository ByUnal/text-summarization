from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from typing import List

from get_model import get_prediction


class ArticleIn(BaseModel):
    articleUuid: str
    articleContent: str


class ArticleOut(BaseModel):
    articleUuid: str
    summarizedContent: str


class ResponseBody(BaseModel):
    body: List[ArticleOut]
    httpStatus: str


class EmptyArticleException(Exception):
    def __init__(self, message: str):
        self.message = message


app = FastAPI()


# TODO: Parse the exception message in order to take 'msg' only
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"exceptionDetail": {"errorCode": "AI_SUMMARIZATION_EXCEPTION",
                                                      "errorMessage": str(exc),
                                                      "service": "AI_SUMMARIZATION_SERVICE"},
                                  "httpStatus": "BAD_REQUEST"
                                  })
    )


@app.exception_handler(EmptyArticleException)
async def empty_article_exception_handler(request: Request, exc: EmptyArticleException):
    return JSONResponse(
        status_code=400,
        content={"exceptionDetail": {"errorCode": "AI_SUMMARIZATION_EXCEPTION",
                                     "errorMessage": exc.message,
                                     "service": "AI_SUMMARIZATION_SERVICE"},
                 "httpStatus": "BAD_REQUEST"
                 }
    )


@app.get("/")
async def status():
    return {"health_check": "OK", "httpStatus": 200}


@app.post("/summarize")
async def sentiment_analysis(article_obj: List[ArticleIn]):
    if not article_obj:
        raise EmptyArticleException(message="Fields cannot be empty")

    try:
        return {"body": get_prediction(article_obj),
                "httpStatus": "OK"}
    except Exception as e:
        raise EmptyArticleException(message=str(e))
