from pathlib import Path

import polars as pl

REPO_ROOT = Path(__file__).parent.parent

STANDARDIZED_SCHEMA = {
    "__Source": "source",
    "User_ID": "user_id",
    "Channel_Name": "channel_name",
    "Message_Timestamp": "message_timestamp",
    "Thread_Timstamp": "thread_timstamp",
    "Channel_ID": "channel_id",
    "__Text": "text",
}


def main():
    raw_messages = pl.read_csv(REPO_ROOT / "data/messages.csv")
    messages = raw_messages.rename(STANDARDIZED_SCHEMA)

    print(messages)


if __name__ == "__main__":
    main()
