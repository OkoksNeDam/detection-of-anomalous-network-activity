import csv
import os
from typing import Type

from starlette.responses import StreamingResponse
from tqdm import tqdm
import pandas as pd
import io

from services.flow_file_processor_service import FlowFileProcessorService


class FlowDirectoryProcessorService:
    """
    Класс для обработки каждого файла из выбранной директории.
    Обработка осуществляется с помощью flow_processor,
    который вытаскивает данные из файла в виде tuple.
    """
    def __init__(self, directory_path: str, flow_processor: Type[FlowFileProcessorService]):
        self.__directory_path = directory_path
        self.__flow_processor = flow_processor
        self.__flows_data = []

    def process(self):
        """
        Обработка каждого файла с помощью flow_processor и сохранение данных в массив.
        """
        for filename in tqdm(os.listdir(self.__directory_path)):
            filepath = os.path.join(self.__directory_path, filename)
            if os.path.isfile(filepath) and not filename.startswith('.'):
                # Создание инстанса класса flow_processor.
                flow_processor = self.__flow_processor(filepath=filepath)
                # Обработка текущего файла и получени из него данных.
                flow_data = flow_processor.process()
                # Добавление новых данных в массив.
                self.__flows_data += [flow_data]

    def get_pandas_flows_data(self):
        return pd.DataFrame(self.__flows_data, columns=self.__flow_processor.FEATURE_LIST)

    def save_csv(self, filepath: str):
        """
        Сохранение полученного массива данных в csv файл.
        :param filepath: путь до создаваемого csv файла.
        """
        dataframe = self.get_pandas_flows_data()
        buffer = io.BytesIO()
        dataframe.to_csv(buffer, index=False)
        buffer.seek(0)

        # Возвращаем CSV файл как StreamingResponse
        return StreamingResponse(content=buffer,
                                 media_type="text/csv",
                                 headers={"Content-Disposition": f"attachment; filename={filepath}"})