import os
import time

from colorama import Fore

def fit(content, length, fill='.', left_align=True):
    '''
    Fit the specified context to a specific length.
    The fill parameter defines with what the string will be filled and the left_align param defines if the fill is placed before or after the content.
    '''

    # Convert to string so numbers can work too
    cache_content = str(content)

    cache_return = cache_content

    # Just making sure there is no possibility of an infinite loop
    if fill == '':
        fill = ' '

    while len(cache_return) < length:
        if left_align:
            cache_return += fill
        else:
            cache_return = fill + cache_return
    
    return cache_return

def colorize(self, text):
    '''
    Use the <color:x> formatting to colorize text inside the document
    '''
    split_text = text.split('color:')
    split_text[0] = split_text[0][:-1]
    color_text = split_text[1].split('>')
    return split_text[0] + '\\textcolor{' + color_text[0] + '}{' + color_text[1][:-1] + '}'

def format_bytes(size, rounding = -1, as_string = True):
    '''
    Gets a number of an amount of Bytes and returns a formatted version with the scale.

    Code used from: https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    '''
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    
    if rounding > -1:
        size = round(size, rounding)

    if as_string:
        return f'{size} {power_labels[n]}B'
    else:
        return size, power_labels[n]+'bytes'

def escape_latex_special_chars(text):
    latex_special_chars = {
        '#': '\\#',
    }
    for char, replacement in latex_special_chars.items():
        text = text.replace(char, replacement)
    return text

def cutoff_filename(path):
    'Return the given path wihtout the file name'

    if '/' in path:
        cache_path = path.split('/')
    else:
        cache_path = path.split('\\')
    
    cache = ''

    # If the given path link to a directory return the path as it is
    if os.path.isdir(path):
        return path
    
    for i in range(0, len(cache_path) - 1):
        cache += cache_path[i] + '/'

    return cache

def today():
    gm = time.gmtime()
    return (fit(gm.tm_mday, 2, '0', True) + '.' +
            fit(gm.tm_mon,  2, '0', True) + '.' +
            fit(gm.tm_year, 2, '0', True)
            + ' - ' +
            fit(gm.tm_hour, 2, '0', True) + ':' +
            fit(gm.tm_min,  2, '0', True) + ':' +
            fit(gm.tm_sec,  2, '0', True))
