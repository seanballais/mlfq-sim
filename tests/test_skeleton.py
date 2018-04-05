#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mlfq_sim.skeleton import fib

__author__ = "Sean Francis N. Ballais"
__copyright__ = "Sean Francis N. Ballais"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
