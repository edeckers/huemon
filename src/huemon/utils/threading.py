# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.


from fcntl import LOCK_EX, LOCK_NB, flock

from huemon.infrastructure.logger_factory import create_logger

LOG = create_logger()


def run_locked(lock_file, fn_call):
    with open(lock_file, "w") as f_lock:
        try:
            flock(f_lock.fileno(), LOCK_EX | LOCK_NB)
            LOG.debug("Acquired lock successfully (file=%s)", lock_file)

            return fn_call()
        except BlockingIOError:
            LOG.debug("Failed to acquire lock (file=%s)", lock_file)
        except Exception as error:  # pylint: disable=broad-except
            LOG.debug(
                "Something unexpected went wrong while acquiring lock (file=%s, error=%s)",
                lock_file,
                error,
            )

    return None
