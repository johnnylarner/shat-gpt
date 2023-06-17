import polars as pl


def main():
    messages = pl.read_csv("data/messages.csv")
    print(messages)


if __name__ == "__main__":
    main()
