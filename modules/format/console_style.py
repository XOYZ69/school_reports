import os
import time
import json

from random import random, randint
from colorama import Fore, Back

from modules.config.config_handler import setting_load
from modules.format.string import cutoff_filename

kiroku_colors = {
    'OTH': {
        '_desc':    'Default colors or other',
        'strtime':  Fore.WHITE,
        'epotime':  Fore.WHITE,
        'tag':      Fore.WHITE,
        'body':     Fore.WHITE
    },
    'CPY': {
        '_desc':    'Copy',
        'strtime':  Fore.CYAN,
        'epotime':  Fore.CYAN,
        'tag':      Fore.BLUE,
        'body':     Fore.BLUE
    },
    'INF': {
        '_desc':    'Information',
        'strtime':  Fore.MAGENTA,
        'epotime':  Fore.MAGENTA,
        'tag':      Fore.MAGENTA,
        'body':     Fore.MAGENTA
    },
    'WRN': {
        '_desc':    'Warning',
        'strtime':  Fore.YELLOW,
        'epotime':  Fore.YELLOW,
        'tag':      Fore.YELLOW,
        'body':     Fore.YELLOW
    },
    'ERR': {
        '_desc':    'Error',
        'strtime':  Fore.RED,
        'epotime':  Fore.RED,
        'tag':      Fore.RED,
        'body':     Fore.RED
    },
    'SCC': {
        '_desc':    'Success',
        'strtime':  Fore.GREEN,
        'epotime':  Fore.GREEN,
        'tag':      Fore.GREEN,
        'body':     Fore.GREEN
    }
}

def kiroku(information, tag='', print_output_path=False, print_to_console = True):
    '''
    Log different events while coloring the terminal, categorizing and saving the logs
    '''

    if tag not in kiroku_colors:
        tag = 'OTH'
    
    colors = kiroku_colors[tag]

    console_obj = {
        'strtime': time.ctime(),
        'epotime': round(time.time()),
        'tag': tag,
        'body': information
    }
    console_obj['tag'] = console_obj['tag']

    if isinstance(information, str):
        console_obj['body'] = information
    elif isinstance(information, list):
        cache = ''

        for i in information:
            cache += i + ' '

        console_obj['body'] = cache
    else:
        console_obj['body'] = str(information)

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

    if print_to_console:
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
