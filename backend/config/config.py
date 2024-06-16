import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    GROQ_MODEL_LLAMA3_8B = os.getenv("GROQ_MODEL_LLAMA3_8B")
    GROQ_MODEL_LLAMA3_70B = os.getenv("GROQ_MODEL_LLAMA3_70B")
    GROQ_MODEL_MIXTRAL_8X7B = os.getenv("GROQ_MODEL_MIXTRAL_8X7B")
    GROQ_MODEL_GEMMA_7B_IT = os.getenv("GROQ_MODEL_GEMMA_7B_IT")
    DEFAULT_USER = os.getenv("DEFAULT_USER")

    @staticmethod
    def validate():
        required_vars = [
            "MONGODB_URI",
            "MONGODB_DB_NAME",
            "GROQ_MODEL_LLAMA3_8B",
            "GROQ_MODEL_LLAMA3_70B",
            "GROQ_MODEL_MIXTRAL_8X7B",
            "GROQ_MODEL_GEMMA_7B_IT",
            "DEFAULT_USER",
        ]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(
                    f"The environment variable {var} is not set or invalid."
                )
