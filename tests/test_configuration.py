from modules.error_handling import Error
from modules.config.config_handler import setting_load, setting_change, settings_find_location

class TestConfigLoading:
    def test_empty_setting(self):
        cache = setting_load('')
        assert Error().is_error(cache)
        assert cache.this_error == '0x03012'

    def test_get_personal_data(self):
        assert setting_load('name_ausbilder', 'report_data') == 'Max Mustermann'
        assert setting_load('name_auszubildender', 'report_data') == 'Tim Azubi'
        assert setting_load('mail_auszubildender', 'report_data') == 'tim@mustermann.de'
    
    def test_config_location(self):
        assert settings_find_location('report_data') == 'data/config/report_data.config'
    
    def test_fail_config_load(self):
        cache = setting_load('a_non_existing_config')
        assert Error().is_error(cache)
        assert cache.this_error == '0x03011'
    
    def test_unkown_return_type(self):
        cache = setting_load('path_source', 'export', return_type='unknow_return_type')
        assert Error().is_error(cache)
        assert cache.this_error == '0x03013'
