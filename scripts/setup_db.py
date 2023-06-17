from shat_gpt.secrets import load_secrets
from shat_gpt.util import load_default_config, logger, logging_setup
import weaviate


def main():
    index_config = load_default_config().get("schemas").get("primary")["config"]

    secrets = load_secrets()
    auth = weaviate.AuthApiKey(secrets.weaviate_api_key)
    client = weaviate.Client(
        url=secrets.weaviate_url,
        auth_client_secret=auth,
    )

    index_name = index_config["class"]
    index_schema = {"classes": [index_config]}
    if client.schema.exists(index_name):
        client.schema.delete_class(index_name)
        print(f"Schema {index_name} exists, deleting.")

    print(f"Creating schema {index_name}.")
    client.schema.create(index_schema)

    if not client.schema.exists(index_name):
        print(f"Unable to create schema {index_name}, exiting.")
        exit(1)


if __name__ == "__main__":
    main()
