from functools import reduce


class HueCommand:
  def _process(value):
    print(value)

  def _mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def name(self):
    pass

  def exec(self):
    pass
