from pathlib import Path

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


META_DATA_FIELD = (
    "source",
    "user_id",
    "message_timestamp",
    "thread_timstamp",
    "channel_id",
    "thread_id",
)

EMBEDDING_FIELDS = (
    "channel_name",
    "text",
)


def add_original_text_field(df: pl.DataFrame, origin: str) -> pl.DataFrame:
    return df.with_columns((pl.lit(origin)).alias("origin"))


def add_meta_data_columns_if_not_exist(df: pl.DataFrame) -> pl.DataFrame:
    for column in META_DATA_FIELD:
        if column not in df.columns:
            df = df.with_columns(pl.lit(None).cast(str).alias(column))
    return df


def select_columns_alphabetically(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(sorted(df.columns))


def main():
    raw_messages = pl.read_csv(REPO_ROOT / "data/messages.csv")
    messages = raw_messages.rename(STANDARDIZED_MESSAGE_SCHEMA)
    messages = add_original_text_field(messages, "messages")
    messages = add_meta_data_columns_if_not_exist(messages)
    messages = select_columns_alphabetically(messages)

    raw_chats = pl.read_csv(REPO_ROOT / "data/chats.csv")
    chats = raw_chats.rename(STANDARDIZED_CHAT_SCHEMA)
    chats = add_original_text_field(chats, "chats")
    chats = chats.drop("")
    chats = add_meta_data_columns_if_not_exist(chats)
    chats = select_columns_alphabetically(chats)

    all_data = pl.concat([messages, chats])
    all_data.write_parquet(REPO_ROOT / "data/all_data.parquet")
    all_data = pl.read_parquet(REPO_ROOT / "data/all_data.parquet")

    print(all_data)


if __name__ == "__main__":
    main()
