# Filename............: error.py
# Creation Date.......: 12.11.2021
# Description.........: An standardized way to handle and display error

import inspect
import time
import json

from modules.format.string import fit

class Error:

    # error-code format: 0xaabbc
    #                      | | |
    #                      | | - c display the error number in the subcategory
    #                      | --- bb displays the subcategory
    #                      ----- aa displays the category

    errors = {
        '0x01xxx': {
            'category': 'System Errors',
            '0x01011':  'Error Code does not exist'
        },
        '0x02xxx': {
            'category': 'IO Errors',
            '0x02011':  'File does not exist.',
            '0x02012':  'File could not be opened.',
            '0x02022':  'Folder does not exist.'
        },
        '0x03xxx': {
            'category': 'Config Errors',
            '0x03011':  'Setting could not be found in config',
            '0x03012':  'Setting can not be empty',
            '0x03013':  'Setting return_type is of an unknown type'
        }
    }

    this_error = ''

    traceback = []

    def __init__(self, errorcode = None, function_name = None) -> None:
        if errorcode is None:
            return
        
        cache = errorcode[0:4] + 'xxx'
        if cache in self.errors:
            if errorcode in self.errors[cache]:
                self.this_error = errorcode
            else:
                self.this_error = '0x01011'
        
            self.add_traceback({
                'function':     function_name,
                'error_code':   errorcode,
                'error_msg':    self.get_error_message()
            })
    
    def get_error_message(self):
        cache = self.this_error[0:4] + 'xxx'
        return self.this_error + ': ' + self.errors[cache][self.this_error]
    
    def add_traceback_fn(self, function_name : str):
        self.add_traceback({
            'function':     function_name,
            'depends_on':   self.traceback[-1]['error_code'] if 'error_code' in self.traceback[-1] else self.traceback[-1]['depends_on']
        })

    def add_traceback(self, entry : dict):
        entry['sys_time'] = time.ctime()

        self.traceback.append(entry)
    
    def print_traceback(self):
        
        for trace in range(len(self.traceback)):
            print(
                fit(f'Trace: {fit(trace, 3, ' ', False)}', 26, ' ', False) +
                ' [TRC]', self.traceback[trace]['function']
            )
    
    def is_error(self, obj):
        return isinstance(obj, Error)
