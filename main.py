from fastapi import FastAPI, HTTPException
import httpx
from typing import Union
from googletrans import Translator

app = FastAPI()
translator = Translator()


@app.get("/fetch-posts/")
async def fetch_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# -----------------------
def translate_data(data: Union[dict, list, str], translator: Translator) -> Union[dict, list, str]:
    if isinstance(data, dict):
        return {key: translate_data(value, translator) for key, value in data.items()}
    elif isinstance(data, list):
        return [translate_data(item, translator) for item in data]
    elif isinstance(data, str):
        return translator.translate(data)
    else:
        return data
    
