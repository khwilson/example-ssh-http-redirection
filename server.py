from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/")
async def post_root(request: Request):
    all_body = []
    async for chunk in request.stream():
        all_body.append(chunk.decode("utf8"))

    return {"Hi": "".join(all_body)}
