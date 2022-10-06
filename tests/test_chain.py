"""
Test file for GenerateFile.
"""
import os
import sys
import pytest
import numpy as np
import pandas as pd
from src.chain import Chain
import random


def test_init_generate_lef() -> None:
    """
    Test if the initialisation of GenerateLef works.
    """
    assert Chain()


def test_distance_matrix() -> None:
    """
    Test the distance matrix value returned.
    """
    n = 10
    locations = [(k, k) for k in range(n)]
    matrix = Chain.get_dist_matrix(locations)
    assert [0]*n == [matrix[k][k] for k in range(n)]
    assert matrix[0][1] == np.sqrt(2)
    assert str(matrix[3][9])[:4] == str(np.sqrt(72))[:4]
    assert str(matrix[8][2])[:4] == str(np.sqrt(72))[:4]


def test_routing() -> None:
    """
    Test if the routing contain all data in the order.
    """
    n_pins = 5
    n_macros = 10
    df = pd.DataFrame([
        {
            'x': random.random(),
            'y': random.random(),
            'macro': k // n_macros,
            'pin': k % n_pins
        } for k in range(n_pins*n_macros)
    ])
    start_index, end_index = 0, 1
    df = Chain.route(df=df, start=start_index, end=end_index)
    assert 'order' in df.head()
    print(df['order'])
    print(np.arange(1, len(df), 1))
    assert sorted(list(df['order'])) == [k for k in range(n_pins*n_macros)]
