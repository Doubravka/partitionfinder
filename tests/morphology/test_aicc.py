import os

import pytest

from partfinder import alignment, analysis_method, config, main, scheme, util


def test_aicc():
    """This test should pass"""

    HERE = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(HERE, "aicctest")
    main.call_main(
        "morphology", '--no-ml-tree --min-subset-size 1 --raxml "%s"' % full_path
    )
    new_file = os.path.join(full_path, "analysis/best_scheme.txt")
    txt = open(new_file)
    file_obj = txt.readlines()
    for x in file_obj:
        x = x.strip()
        if "Scheme AICc" in x:
            line = x.split(":")
            numspace = line[1]
            num = numspace.strip()
            num = float(num)
            num = int(num)
            assert num == 722
