import os
from zipfile import ZipFile

import pytest

from partfinder import analysis, config, main, util

HERE = os.path.abspath(os.path.dirname(__file__))


def test_grand():
    full_path = os.path.join(HERE, "Grande_2013")
    with pytest.raises(util.PartitionFinderError):
        main.call_main("DNA", '--no-ml-tree --raxml "%s"' % full_path)
