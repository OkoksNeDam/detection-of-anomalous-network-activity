import torch
from torch.utils.data import Dataset


class PandasDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        # Получаем строку по индексу
        row = self.dataframe[idx]
        # Преобразуем данные в тензоры (например, если у вас есть признаки и метки)
        # Предположим, что последний столбец - это метка
        features = torch.tensor(row, dtype=torch.float32)  # Признаки
        return features
