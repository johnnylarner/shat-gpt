# script to query data from Weaviate DB.
# Run: python scripts/query_db.py | jq

import json
import os
from dotenv import load_dotenv
import weaviate

load_dotenv()
WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY = os.environ["WEAVIATE_API_KEY"]

# provide class name, e.g. 'LangChain_(...)'
CLASS_NAME = "TextItem"  # 35f2... is class name of our dummy index
auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)

# Instantiate the client with the auth config
client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=auth_config)


# from https://weaviate.io/developers/weaviate/manage-data/read-all-objects
def get_batch_with_cursor(
    client, class_name, class_properties, batch_size=100, cursor=None
):
    query = (
        client.query.get(class_name, class_properties)
        .with_additional(["id"])
        .with_limit(batch_size)
    )

    if cursor is not None:
        return query.with_after(cursor).do()
    else:
        return query.do()


# get all objects from given class
response = get_batch_with_cursor(client, CLASS_NAME, ["text"])
print(json.dumps(response, indent=4))
