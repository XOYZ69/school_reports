import os

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
