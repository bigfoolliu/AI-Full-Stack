#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: bigfoolliu

from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
