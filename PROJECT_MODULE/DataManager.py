import numpy as np
import pandas as pd

class DataManager:

    '''
    For now, a crude version of a data manager. Wraps data to allow for saving/loading.
    *temporary feature*, will be replaced when I add more types of data.
    '''

    def __init__(self, path: str, data: pd.DataFrame) -> None:
        self.path = path
        self.data = data

    def save(self) -> None:
        compact_data = self.data.reset_index()
        npy_to_save = np.append( pd.DataFrame.to_numpy(compact_data), [list(compact_data.columns)], axis=0 )
        np.save(file=self.path, arr=npy_to_save, allow_pickle=False)

    def load(self) -> None:
        self.data = pd.DataFrame(np.load(file=self.path + '.npy', allow_pickle=False))
        self.data.columns = self.data.iloc[-1]
        self.data.drop(self.data.tail(1).index, inplace=True)
        self.data = self.data.astype('float')
        self.data.set_index("open time", inplace=True)

    def update(self, new_data) -> None:
        self.data = new_data