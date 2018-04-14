# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'mlfq-sim'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:  # pragma: no cover
    # Can't unit test this for now since I do not know how to temporarily
    # remove a distribution during runtime. Help. Also, is this even
    # worth it?
    __version__ = 'unknown'
