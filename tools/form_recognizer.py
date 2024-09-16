import os

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Load Azure Form Recognizer credentials
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def analyze_image(image_path: str) -> str:
    """Analyze an image using Azure Form Recognizer and return the extracted text."""
    client = DocumentAnalysisClient(
        endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY),
    )

    with open(image_path, "rb") as image:
        poller = client.begin_analyze_document("prebuilt-read", image)
        result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    return extracted_text
