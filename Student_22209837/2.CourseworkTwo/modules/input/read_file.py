"""

UCL -- Institute of Finance & Technology
Author  : Luca Cocconcelli
Lecture : 2022-11-17
Topic   : Main.py
Project : MongoDB Trades uploader
Desc    : Class to find, read and return latest file in specific directory.
          Please, note, file conventions expects datetime stamp as %Y%m%d%H%M%S
          before '.' file name extension. This is used to sort latest file.


"""

import os
from datetime import datetime

from modules.utils.info_logger import print_info_log
from modules.input.avro_input import AvroFileOperations
from modules.input.csv_input import CsvFileOperations
from modules.input.parquet_input import ParquetFileOperations
from static.RNDTRADE import generate_parquet_schema


class ReadInputFiles:
    """
    Arguments:
        file_path (str): Path to the trade file repository
        signature: file name convention
        log_file (str): latest file read and loaded

    Public methods:
        read_csv_dictionary: returns list of ordered dictionaries.
    -----
    Usage
        class_reader = ReadInputFiles(conf['params']['OutputFile'])
        class_reader.get_latest_input_file()

    """

    def __init__(self, file_config, log_file='./static/file_load_logger.txt'):
        self.file_path = file_config['DataLake']
        self.log_file = log_file
        self.file_config = file_config
        self.file_name, self.file_type = self.get_latest_input_file()

    def _get_input_files_ctl(self):
        file_list = os.listdir(self.file_path)
        ctl_list = [ctl for ctl in file_list if ctl.split('.')[1] == 'ctl']

        if not ctl_list:
            raise ValueError('Empty list')

        sorted_ctl = sorted(ctl_list, key=lambda filename: datetime.strptime(filename[-18:-4], '%Y%m%d%H%M%S'),
                            reverse=True)
        return sorted_ctl

    def _write_log_file(self, file_name):
        with open('./static/file_load_logger.txt', 'w') as f:
            f.write(file_name)

    def _read_logged_file(self):
        """reads logged files, if not exists returns mock-up"""
        if not os.path.exists(self.log_file):
            # creates mockup if not exists
            return 'BondTrades_XXXXXXXXXXX.XYZ'

        with open(self.log_file) as f:
            lines = f.readlines()
        return lines[0]

    def get_latest_input_file(self):
        '''finds latest file with data and file type extension'''
        ctl_files = self._get_input_files_ctl()
        latest_ctl = ctl_files[0]
        # add here check if same of last logged file
        ctl_path = os.path.join(self.file_path, latest_ctl)

        if os.path.exists(ctl_path.replace('ctl', 'csv')):
            return latest_ctl.replace('ctl', 'csv'), 'csv'
        elif os.path.exists(ctl_path.replace('ctl', 'avro')):
            return latest_ctl.replace('ctl', 'avro'), 'avro'
        elif os.path.exists(ctl_path.replace('ctl', 'parquet')):
            return latest_ctl.replace('ctl', 'parquet'), 'parquet'
        else:
            raise TypeError('file not found based on conditions file extension needs to be avro, csv parquet')

    @staticmethod
    def _select_read_class(file_type):
        '''Abstraction method to select the write output class'''
        class_select = {
            'parquet': ParquetFileOperations,
            'avro': AvroFileOperations,
            'csv': CsvFileOperations
        }
        return class_select[file_type]

    def _set_file_schema(self, file_type):
        if file_type == 'avro':
            return self.file_config['AvroSchema']
        elif file_type == 'csv':
            return self.file_config['ColumnNames']
        elif file_type == 'parquet':
            return generate_parquet_schema()
        else:
            raise TypeError('Not implemented write output format ')

    def read_dictionary(self):
        class_reader = self._select_read_class(self.file_type)
        file_schema = self._set_file_schema(self.file_type)
        full_path = os.path.join(self.file_path, self.file_name)
        read_file = class_reader(file_schema)
        return read_file.read_table(full_path)

    def __repr__(self) -> str:
        f'Data reader : instance of class for file {self.file_name}'
