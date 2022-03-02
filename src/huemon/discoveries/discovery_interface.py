# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import json
from functools import reduce


class Discovery:
    @staticmethod
    def _item_to_discovery(item: dict):
        return {
            "{#NAME}": item["name"],
            "{#UNIQUE_ID}": item["uniqueid"],
        }

    @staticmethod
    def _has_state_field(field: str):
        return (
            lambda item: "state" in item
            and field in item["state"]
            and "recycle" not in item
        )

    @staticmethod
    def _print_array_as_discovery(items):
        print(
            json.dumps(
                {
                    "data": reduce(
                        lambda p, item: [*p, Discovery._item_to_discovery(item)],
                        items,
                        [],
                    )
                }
            )
        )

    @staticmethod
    def name():
        pass

    def exec(self, arguments=None):
        pass
