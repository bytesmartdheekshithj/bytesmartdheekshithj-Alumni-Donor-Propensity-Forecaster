import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    PORT = int(os.getenv("PORT", "5000"))
    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        "/app/model/alumni_donor_model_pipeline.pkl",
    )
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    HIGH_THRESHOLD = float(os.getenv("HIGH_THRESHOLD", "70"))
    MEDIUM_THRESHOLD = float(os.getenv("MEDIUM_THRESHOLD", "40"))