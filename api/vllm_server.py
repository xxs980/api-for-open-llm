import sys
import os

import torch
print("Cuda support:", torch.cuda.is_available(),":", torch.cuda.device_count(), "devices")

sys.path.insert(0, ".")
print(__file__)
print(os.path.abspath(__file__))  # 获取当前文件的绝对路径
print(os.path.dirname(os.path.abspath(__file__)))  # 去掉文件名，返回目录
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 返回上2级目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import config
from api.models import EMBEDDED_MODEL, VLLM_ENGINE
from api.routes import model_router, embedding_router
from api.vllm_routes import chat_router, completion_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = config.API_PREFIX
app.include_router(model_router, prefix=prefix, tags=["model"])
if EMBEDDED_MODEL is not None:
    app.include_router(embedding_router, prefix=prefix, tags=["Embedding"])
if VLLM_ENGINE is not None:
    app.include_router(chat_router, prefix=prefix, tags=["Chat"])
    app.include_router(completion_router, prefix=prefix, tags=["Completion"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")
