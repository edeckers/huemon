# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.


import json
import os
import tempfile


def cache_output_to_temp(cache_file_path, fn_call):
    tmp_fd, tmp_file_path = tempfile.mkstemp()
    with open(tmp_file_path, "w") as f_tmp:
        f_tmp.write(json.dumps(fn_call()))

    os.close(tmp_fd)

    os.rename(tmp_file_path, cache_file_path)

    with open(cache_file_path) as f_json:
        return json.loads(f_json.read())
