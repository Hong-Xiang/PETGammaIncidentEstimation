from dxl.learn.dataset import DataColumns
from engine import get_or_create_session
import tqdm
import numpy as np
from query import capacity

dataset_path = '../../../data/gamma.db'


class PhotonDataColumns(DataColumns):
    def _process(self, data):
        create_all(data)

    @property
    def columns(self):
        return ['hits']

    def capacity(self):
        return capacity()
    
    def __iter__(self):
        return 