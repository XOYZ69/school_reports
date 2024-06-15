import os

from modules.error_handling import Error

def settings_find_location(setting_type):
    settings_file = 'data/config/' + setting_type + '.config'
    if not os.path.exists(settings_file):
        return Error('0x02011', 'settings_find_location')
    
    return settings_file

def setting_load(setting_to_get, setting_type='report_data', return_type='str'):
    '''
    Load the designated settings file and return the stored value if the setting exists
    Will return an Error Object if the file or value does not exist
    '''

    if setting_to_get == '':
        return Error('0x03012', 'setting_load', (setting_to_get, setting_type, return_type))

    settings_file = settings_find_location(setting_type)

    if isinstance(settings_file, Error):
        settings_file.add_traceback_fn('setting_load')
        return settings_file

    setting_value = ''

    with open(settings_file, 'r', encoding='utf-8') as cache_file:
        for line in cache_file.readlines():
            if line[0] != '#' and line != '' and ': ' in line:
                current_line = line.split(': ')
                current_line[0] = current_line[0].replace('.', '')

                if current_line[0] == setting_to_get or ('*' in setting_to_get and setting_to_get.replace('*', '') in current_line[0]):
                    if setting_value == '':
                        setting_value = current_line[1].replace('\n', '')
                    else:
                        if isinstance(setting_value, str):
                            setting_value = [setting_value]

                        setting_value.append(current_line[1].replace('\n', ''))

    if setting_value == '':
        return Error('0x03011', 'setting_load', (setting_to_get, setting_type, return_type))
    elif isinstance(setting_value, list):
        return setting_value
    else:
        if return_type == 'str':
            return str(setting_value)
        elif return_type == 'int':
            return int(setting_value)
        elif return_type == 'boolean' or return_type == 'bool':
            if setting_value in ['true', 'True', 'TRUE', 'Y', 'y', '1', 'yes', 'YES']:
                return True
            elif setting_value in ['false', 'False', 'FALSE', 'N', 'n', '0', 'no', 'NO']:
                return False
            else:
                return False
        elif return_type == 'float':
            return float(setting_value)
        else:
            return Error('0x03013', 'setting_load', (setting_to_get, setting_type, return_type))

def setting_change(setting_to_change, new_value, setting_type='settings'):
    settings_file = settings_find_location(setting_type)

    if isinstance(settings_file, Error):
        settings_file.add_traceback_fn('setting_change')
        return settings_file

    loaded_settings = []
    found_index = -1

    with open(settings_file, 'r', encoding='utf-8') as cache_file:
        loaded_settings = cache_file.readlines()

    for line in range(len(loaded_settings)):
        if loaded_settings[line][0] != '#' and loaded_settings[line] != '':
            current_line = loaded_settings[line].split(': ')

            if current_line[0].replace('.', '') == setting_to_change:
                found_index = line
                break
    if found_index > -1:
        cache_setting = loaded_settings[found_index].split(': ')
        loaded_settings[found_index] = cache_setting[0] + ': ' + new_value + '\n'

        with open(settings_file, 'w', encoding='utf-8') as cache_file:
            cache_file.writelines(loaded_settings)
    else:
        return Error('0x03011', 'setting_change')