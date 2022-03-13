# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from functools import reduce

from huemon.api.api_interface import ApiInterface
from huemon.processors.processor_interface import ProcessorInterface


class HueCommand:
    def __init__(self, config: dict, api: ApiInterface, processor: ProcessorInterface):
        self.config = config
        self.api = api
        self.processor = processor

    @staticmethod
    def get_by_unique_id(unique_id: str, items: list) -> list:
        return list(
            filter(
                lambda info: "uniqueid" in info and info["uniqueid"] == unique_id, items
            )
        )[0]

    @staticmethod
    def _mapper(path: str, value_type):
        return lambda value: value_type(
            reduce(lambda p, field: p[field], path.split("."), value)
        )

    @staticmethod
    def name():
        pass

    def _process(self, value):
        self.processor.process(value)

    def exec(self, arguments):
        pass
