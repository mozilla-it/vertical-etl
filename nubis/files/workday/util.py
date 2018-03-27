def convert_value(val):
    # Need to escape for CSV format
    # literral '\' => '\\'
    # litteral ',' => '\,'
    if isinstance(val, (str, unicode)):
        val = val.replace('\\', '\\\\').replace(',', '\\,')

    if isinstance(val, unicode):
        return val.encode('utf-8')
    else:
        return str(val).encode('utf-8')

import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import shutil
def cleanup(tmp_dir):
    try:
        os.remove(tmp_dir)
    except OSError as exc:
        raise
