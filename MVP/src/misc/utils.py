import json
from typing import Union


def pprint(results: Union[list, dict]) -> str:
    return json.dumps(results, indent=4, sort_keys=True)
