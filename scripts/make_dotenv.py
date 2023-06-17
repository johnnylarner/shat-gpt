from pathlib import Path

repo_root = Path(__file__).parent.parent


def main():
    env = repo_root / ".env"

    if env.exists():
        should_overwrite = input(
            "There is a .env file already, do you want to overwrite? y/n: "
        )
        if should_overwrite == "n":
            exit()

    with open(repo_root / ".env", "w") as f:
        weaviate_url = input("Please provide the Weaviate URL: ")
        weaviate_api_key = input("Please provide the Weaviate API key: ")
        openai_api_key = input("Please provide the OpenAI API key: ")

        pairs_to_write = {
            "WEAVIATE_URL": weaviate_url,
            "WEAVIATE_API_KEY": weaviate_api_key,
            "OPENAI_API_KEY": openai_api_key,
        }

        for key, value in pairs_to_write.items():
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
