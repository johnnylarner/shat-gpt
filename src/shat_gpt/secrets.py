from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent


@dataclass
class Secrets:
    weaviate_url: str
    weaviate_api_key: str
    openai_api_key: str


def load_secrets() -> Secrets:
    """
    Load the secrets from the .env file

    :return: the secrets
    """
    from dotenv import dotenv_values

    env = dotenv_values(REPO_ROOT / ".env")
    return Secrets(
        weaviate_url=env["WEAVIATE_URL"],
        weaviate_api_key=env["WEAVIATE_API_KEY"],
        openai_api_key=env["OPENAI_API_KEY"],
    )
