import os
from zipfile import ZipFile

import pytest

from partfinder import analysis, config, main, util

HERE = os.path.abspath(os.path.dirname(__file__))


def test_1subset():
    full_path = os.path.join(HERE, "1subset")
    main.call_main("DNA", '--raxml --no-ml-tree "%s"' % full_path)
