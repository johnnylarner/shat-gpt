from pathlib import Path

import polars as pl

REPO_ROOT = Path(__file__).parent.parent


def main():
    messages = pl.read_csv(REPO_ROOT / "data/messages.csv")
    print(messages)


if __name__ == "__main__":
    main()
