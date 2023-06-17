from shat_gpt.secrets import load_secrets
from shat_gpt.util import load_default_config
import weaviate

CLASS_NAME = "TextItem"
CLASS = {
    "class": CLASS_NAME,
    "description": "A class called document",
    "vectorizer": "text2vec-cohere",
    "moduleConfig": {  # specify the vectorizer and model type you're using
        "text2vec-cohere": {
            "model": "multilingual-22-12",  # defaults to multilingual-22-12 if not set
            "truncate": "RIGHT",  # defaults to RIGHT if not set
        }
    },
    "properties": [
        {
            "name": "channel_name",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-cohere": {"skip": False, "vectorizePropertyName": True}
            },
        },
        {
            "name": "text",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-cohere": {"skip": False, "vectorizePropertyName": True}
            },
        },
        {
            "name": "source",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
        {
            "name": "user_id",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
        {
            "name": "message_timestamp",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
        {
            "name": "thread_timstamp",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
        {
            "name": "channel_id",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
        {
            "name": "thread_id",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-cohere": {"skip": True}},
        },
    ],
}


def main():
    secrets = load_secrets()

    auth = weaviate.AuthApiKey(secrets.weaviate_api_key)
    client = weaviate.Client(
        url=secrets.weaviate_url,
        auth_client_secret=auth,
        additional_headers={"X-Cohere-Api-Key": secrets.cohere_api_key},
    )

    if client.schema.exists(CLASS_NAME):
        client.schema.delete_class(CLASS_NAME)
        print(f"Schema {CLASS_NAME} exists, deleting.")

    client.schema.create_class(CLASS)
    print(client.schema.get(CLASS_NAME))


if __name__ == "__main__":
    main()
