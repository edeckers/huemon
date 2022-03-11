# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
from pathlib import Path


def get_root_module_path():
    return Path(sys.modules["__main__"].__file__).parent


def create_local_path(relative_path: str):
    return str(os.path.join(get_root_module_path().absolute(), relative_path))
