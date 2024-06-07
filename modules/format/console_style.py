import os
import time
import json

from random import random, randint
from colorama import Fore, Back

from modules.config.config_handler import setting_load
from modules.format.io import cutoff_filename

def kiroku(information, tag='', print_output_path=False):
    '''
    Log different events while coloring the terminal, categorizing and saving the logs
    '''

    colors={
        'strtime': Fore.WHITE,
        'epotime': Fore.WHITE,
        'tag': Fore.YELLOW,
        'body': Fore.CYAN
    }

    console_obj = {
        'strtime': time.ctime(),
        'epotime': round(time.time()),
        'tag': tag,
        'body': information
    }
    
    # OTH = Other
    if console_obj['tag'] == '':
        console_obj['tag'] = 'OTH'
    # WRN = Warning
    elif console_obj['tag'] == 'WRN':
        colors['strtime']   = Fore.YELLOW
        colors['epotime']   = Fore.YELLOW
        colors['tag']   = Fore.YELLOW
        colors['body']  = Fore.YELLOW
    # INF = Information
    elif console_obj['tag'] == 'INF':
        colors['strtime']   = Fore.WHITE
        colors['epotime']   = Fore.WHITE
        colors['tag']   = Fore.YELLOW
        colors['body']  = Fore.CYAN
    # ERR = Error
    elif console_obj['tag'] == 'ERR':
        colors['strtime']   = Fore.RED
        colors['epotime']   = Fore.RED
        colors['tag']   = Fore.RED
        colors['body']  = Fore.LIGHTRED_EX

    console_obj['tag'] = console_obj['tag']

    if isinstance(information, str):
        console_obj['body'] = information
    elif isinstance(information, list):
        cache = ''

        for i in information:
            cache += i + ' '

        console_obj['body'] = cache
    else:
        # Error Handling
        return 'unsupported data type for information'

    if setting_load('style_function_kiroku_export_to_file', return_type='boolean', setting_type='style'):
        log_path = setting_load('style_function_kiroku_export_file_path', setting_type='style')
        log_path = log_path.replace('{year}', str(time.gmtime().tm_year))
        log_path = log_path.replace('{month}', str(time.gmtime().tm_mon))
        log_path = log_path.replace('{date}', str(time.gmtime().tm_year) + '-' + str(time.gmtime().tm_mon) + '-' + str(time.gmtime().tm_mday))

        if print_output_path:
            print(log_path, cutoff_filename(log_path))

        if not os.path.exists(cutoff_filename(log_path)):
            os.makedirs(cutoff_filename(log_path), exist_ok=True)

        cache_kiroku_logs = {}

        if os.path.exists(log_path):
            cache_kiroku_logs = json.loads(open(log_path).read())
        
        cache_kiroku_logs[console_obj['strtime'] + '_' + generate_id(16)] = {
            'strtime':  console_obj['strtime'],
            'epotime':  console_obj['epotime'],
            'tag':      console_obj['tag'],
            'body':     console_obj['body']
        }
        
        with open(log_path, 'w') as log_file:
            log_file.write(json.dumps(cache_kiroku_logs, indent = 2))
    
    # Printing to console
    cache_kiroku =  colors['strtime'] + '[' + console_obj['strtime'] + '] '
    cache_kiroku += colors['tag'] + '[' + console_obj['tag'] + '] '
    cache_kiroku += colors['body'] + console_obj['body'] + Fore.RESET + Back.RESET

    print(cache_kiroku)

    return cache_kiroku

def generate_id(length, pair_size = 4):
    'Generate a random id with a specific length and a pair_size.'

    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW1234567890'

    cache_id = ''

    for i in range(length):
        cache_id += chars[randint(0, len(chars) - 1)]

        if (i + 1) % pair_size == 0 and i < length - 1:
            cache_id += '-'

    return cache_id
