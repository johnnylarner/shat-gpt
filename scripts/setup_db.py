from shat_gpt.secrets import load_secrets
import weaviate


def main():
    secrets = load_secrets()
    auth = weaviate.AuthApiKey(secrets.weaviate_api_key)
    client = weaviate.Client(
        url=secrets.weaviate_url,
        auth_client_secret=auth,
    )

    schema = client.schema.get()  # Get the schema to test connection
    print(schema)


if __name__ == "__main__":
    main()
