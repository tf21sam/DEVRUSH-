from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from langchain_community.document_loaders import UnstructuredURLLoader
import os

router = APIRouter()

@router.post("/process-url/")
async def process_url(url: str):
    try:
        # Load the URL content using UnstructuredURLLoader
        loader = UnstructuredURLLoader(urls=[url])
        documents = loader.load()

        # Combine all extracted content into a single text block
        content = " ".join([doc.page_content for doc in documents])

        # Optional: Save the content to a file
        os.makedirs("data", exist_ok=True)
        with open("data/processed_content.txt", "w", encoding="utf-8") as f:
            f.write(content)

        return {"message": "Content processed successfully", "content_preview": content[:500]}  # Return first 500 chars for preview

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the URL. Error: {str(e)}")
