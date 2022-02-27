from functools import reduce
import json


class Discovery:
  def _item_to_discovery(item):
    return {
        "{#NAME}": item["name"],
        "{#UNIQUE_ID}": item["uniqueid"],
    }

  def _has_state_field(field: str):
    return lambda item: \
        "state" in item and \
        field in item["state"] and \
        "recycle" not in item

  def _print_array_as_discovery(items):
    print(json.dumps({"data": reduce(
        lambda p, item: [*p, Discovery._item_to_discovery(item)],
        items,
        [])}))

  def name():
    pass

  def exec(self, arguments=None):
    pass
