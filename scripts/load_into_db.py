from pathlib import Path
import time

import weaviate
from shat_gpt.secrets import load_secrets
from shat_gpt.util import load_default_config

import polars as pl

REPO_ROOT = Path(__file__).parent.parent

STANDARDIZED_MESSAGE_SCHEMA = {
    "__Source": "source",
    "User_ID": "user_id",
    "Channel_Name": "channel_name",
    "Message_Timestamp": "message_timestamp",
    "Thread_Timstamp": "thread_timstamp",
    "Channel_ID": "channel_id",
    "__Text": "text",
}

STANDARDIZED_CHAT_SCHEMA = {
    "chat_text": "text",
}


def add_original_text_field(df: pl.DataFrame, origin: str) -> pl.DataFrame:
    return df.with_columns((pl.lit(origin)).alias("origin"))


def add_meta_data_columns_if_not_exist(
    df: pl.DataFrame, meta_cols: list[str]
) -> pl.DataFrame:
    for column in meta_cols:
        if column not in df.columns:
            df = df.with_columns(pl.lit(None).cast(str).alias(column))
    return df


def select_columns_alphabetically(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(sorted(df.columns))


def main():
    schemas = load_default_config().get("schemas")
    primary_schema = schemas.get("primary")
    meta_data_cols = primary_schema.get("meta_data_fields")

    raw_messages = pl.read_csv(REPO_ROOT / "data/messages.csv")
    messages = raw_messages.rename(STANDARDIZED_MESSAGE_SCHEMA)
    messages = add_original_text_field(messages, "messages")
    messages = add_meta_data_columns_if_not_exist(messages, meta_data_cols)
    messages = select_columns_alphabetically(messages)

    raw_chats = pl.read_csv(REPO_ROOT / "data/chats.csv")
    chats = raw_chats.rename(STANDARDIZED_CHAT_SCHEMA)
    chats = add_original_text_field(chats, "chats")
    chats = chats.drop("")
    chats = add_meta_data_columns_if_not_exist(chats, meta_data_cols)
    chats = select_columns_alphabetically(chats)

    all_data = pl.concat([messages, chats])
    all_data.write_parquet(REPO_ROOT / "data/all_data.parquet")
    all_data = pl.read_parquet(REPO_ROOT / "data/all_data.parquet")

    print(all_data)

    secrets = load_secrets()
    auth = weaviate.AuthApiKey(secrets.weaviate_api_key)
    client = weaviate.Client(
        url=secrets.weaviate_url,
        auth_client_secret=auth,
        additional_headers={"X-Cohere-Api-Key": secrets.cohere_api_key},
    )

    for row in all_data.head(10_000).iter_rows(named=True):
        try:
            print("Sending object")
            client.data_object.create(row, "TextItem")
            time.sleep(0.6)
        except weaviate.exceptions.UnexpectedStatusCodeException:
            print("Rate limit reached, sleeping for 10 secs.")
            time.sleep(10)
            client.data_object.create(row, "TextItem")


if __name__ == "__main__":
    main()
