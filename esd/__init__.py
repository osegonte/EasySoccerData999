"""
# EasySoccerData

A Python easy-to-use library for for fetching live football/soccer stats from multiple online sources/apis.

Note! This package is not affiliated with any of the sources used to extract data.

.. include:: ../READMEdoc.md
   :start-line: 17
"""

from .sofascore import SofascoreClient
from .promiedos import PromiedosClient
from .fbref import FBrefClient


__all__ = [
    "SofascoreClient",
    "PromiedosClient",
    "FBrefClient",
]

__version__ = "0.0.5"
__description__ = (
    "A simple python package for extracting real-time soccer data "
    "from diverse online sources, providing essential statistics and insights."
)
__author__ = "Manuel Cabral"
__title__ = "EasySoccerData"
__license__ = "GPL-3.0"
