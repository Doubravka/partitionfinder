import os
import shlex

import pytest

from partfinder import (
    alignment,
    analysis_method,
    config,
    main,
    reporter,
    results,
    scheme,
    util,
)


def test_bin():
    """This test should pass"""
    HERE = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(HERE, "binary")
    main.call_main(
        "morphology", '--no-ml-tree --min-subset-size 1 --raxml "%s"' % full_path
    )
