from functools import reduce


class HueCommand:
  @staticmethod
  def get_by_unique_id(unique_id: str, items: list) -> list:
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == unique_id,
        items))[0]

  @staticmethod
  def _process(value):
    print(value)

  @staticmethod
  def _mapper(path: str, value_type):
    return lambda value: value_type(reduce(lambda p, field: p[field], path.split("."), value))

  @staticmethod
  def name():
    pass

  def exec(self):
    pass
