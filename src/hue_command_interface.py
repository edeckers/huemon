from functools import reduce


class HueCommand:
  def get_by_unique_id(unique_id: str, items: list) -> list:
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == unique_id,
        items))[0]

  def _process(value):
    print(value)

  def _mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def name(self):
    pass

  def exec(self):
    pass
