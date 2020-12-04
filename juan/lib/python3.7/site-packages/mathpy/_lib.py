"""
Private module containing functions used throughout package.

"""

import numpy as np
import pandas as pd


def _create_array(x):
    if x is None:
        return None

    if isinstance(x, np.ndarray) is False:
        if isinstance(x, pd.DataFrame):
            cols = x.columns
            xn = x.as_matrix()
        elif isinstance(x, pd.Series):
            cols = x.name
            xn = x.to_frame().as_matrix()
        elif isinstance(x, list):
            xn = np.array(x).T
            cols = None
        elif isinstance(x, dict):
            cols = ','.join(list(x.keys))
            _xn = np.column_stack(x.values())
            xn = np.array(_xn)
        else:
            xn = np.array(x)
            cols = None
    else:
        xn = x
        cols = None

    return (xn, cols)
