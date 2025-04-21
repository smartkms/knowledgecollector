import os
import subprocess
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import Response

from uv_minimal_example.models.example_data import ExampleData

# Load environment variables
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

# Initialize the FastAPI app
app = FastAPI()

@app.post("/returnData")
def return_data(example_data: ExampleData):
    """
    Return some random data.

    :param example_data: Example data
    :return: Some useless data
    """
    return {
	"data": "string"
    }


@app.get(
    "health",
    response_class=Response,
    responses={500: {"description": "Internal Server Error"}},
)
def get_health_status():
    """
    Get health status of the application.
    """
    return Response(status_code=200)
