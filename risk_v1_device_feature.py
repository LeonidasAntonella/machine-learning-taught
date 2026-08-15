# compile_once_init_once_v2
# 首行必须是上面的格式，否则不会使用单例模式
from traceback import format_exc
from obs import ObsClient
from obs import loadtoken
import pandas as pd
import numpy as np
import warnings
import json
import time
import re

class DeviceBaseFeature(object):
    def __init__(self):
        self.good_brand_v1_list = ['samsung_sm-g985f', 'samsung_sm-a920f', 'samsung_sm-g965f', 'samsung_sm-a256e', 'asus_i003dd', 'samsung_sm-c900f', 'samsung_sm-n935f', 'iphone 13 pro max_iphone', 'realme_rmx3371', 'samsung_sm-m526br', 'samsung_sm-m536b', 'nokia_nokia 5.4', 'iphone16,2_iphone', 'iphone15,5_iphone', 'oppo_cph2371', 'samsung_sm-n770f', 'iphone 13 mini_iphone', 'oppo_cph2247', 'oppo_cph1955', 'asus_ai2202', 'iphone 14 pro max_iphone', 'samsung_sm-g770f', 'samsung_sm-f731b', 'samsung_sm-n985f', 'samsung_sm-g998b', 'samsung_sm-f711b', 'samsung_sm-n980f', 'xiaomi_22071212ag', 'samsung_sm-f926b', 'honor_jsn-l22', 'oppo_cph2357', 'samsung_sm-s911b', 'samsung_sm-s711b', 'samsung_sm-f721b', 'iqoo_i2216', 'vivo_vivo 1940', 'poco_2310fpca4g', 'kddi_sov41', 'oppo_cph1869', 'xiaomi_mi 8', 'samsung_sm-g996b', 'vivo_vivo 1610', 'samsung_sm-m305m', 'huawei_vog-l29', 'samsung_sm-s906e', 'iphone 13 pro_iphone', 'samsung_sm-f936b', 'xiaomi_2201122g', 'iphone15,4_iphone', 'samsung_sm-s908e', 'iphone16,1_iphone', 'samsung_sm-s918b', 'oppo_cph2603', 'samsung_sm-g980f', 'samsung_sm-j720f', 'samsung_sm-n976n', 'infinix_infinix x6525b', 'asus_d', 'xiaomi_2201123g', 'realme_rmx3741', 'realme_rmx1903', 'oppo_cph1919', 'vivo_v2327', 'samsung_sm-g780f', 'samsung_sm-g885f', 'infinix_infinix x672', 'samsung_sm-x205', 'tecno_tecno lf7n', 'samsung_sm-m625f', 'advan_6201', 'poco_2311drk48g', 'samsung_sm-s928b', 'samsung_sm-n986b', 'oppo_cph2599', 'oppo_f1f', 'samsung_sm-f946b', 'samsung_sm-g991b', 'asus_x00qd', 'kddi_scv41', 'oppo_oppo6833', 'samsung_sm-m546b', 'huawei_lya-l29']
        self.bad_brand_v1_list = ['samsung_sm-a260g', 'tecno_tecno ki5q', 'xiaomi_redmi 3s', 'google_pixel 3 xl', 'samsung_sm-j320g', 'samsung_sm-n971n', 'tecno_tecno ke5k', 'samsung_sm-m105g', 'advan_6501', 'vivo_vivo 1812', 'samsung_sm-j700f', 'infinix_infinix x687', 'asus_x00rd', 'google_pixel 4a', 'oppo_cph1859', 'vivo_vivo y19', 'samsung_sm-a310f', 'xiaomi_redmi 6', 'samsung_sm-j400f', 'infinix_infinix x6835', 'samsung_sm-g532g', 'vivo_v2144', 'oppo_oppo a57', 'itel_itel a571l', 'huawei_ldn-lx2', 'infinix_infinix x612b', 'xiaomi_redmi note 5a', 'infinix_infinix x690b', 'realme_rmx3690', 'samsung_sm-j600g', 'kddi_sov40', 'realme_rmx3561', 'honor_lld-l21', 'samsung_sm-j810y', 'infinix_infinix x6512', 'xiaomi_redmi 5 plus', 'xiaomi_redmi note 6 pro', 'vivo_vivo 1714', 'infinix_infinix x689d', 'xiaomi_mi max 2', 'vivo_vivo 1606', 'realme_rmx3771', 'samsung_sm-j111f', 'infinix_infinix x626b lte', 'infinix_infinix x625d', 'oppo_cph2137', 'oppo_x9009', 'samsung_sm-j250f', 'xiaomi_mi a2 lite', 'oppo_a37fw', 'oppo_cph1725', 'asus_x01ad', 'infinix_infinix x688c', 'vivo_vivo 1612', 'infinix_infinix x689', 'oppo_a37f', 'infinix_infinix x680b', 'infinix_infinix x6811', 'realme_rmx1925']

    def _init_some_value(self, data: dict):
        if data:
            self.server_time = data['server_time']
            self.imei = data['base']['imei']
            self.account_id = str(data['base'].get('account_id', '-9999'))
            self.df_base = pd.json_normalize(data.get('base', []))
            self.df_base['server_time'] = self.server_time
            self.df_base['account_id'] = self.account_id
        else:
            self.df_base = pd.DataFrame()

    def save_index(self, data):
        return {'account_id': self.account_id, 'imei': self.imei, 'data': data, 'create_time': int(time.time())*1000, '__flag': {'feature_add_tag': 1, 'redis_tag': 1}}

    @staticmethod
    def device_unit_normalize(x):
        try:
            memory = re.findall(r'[-+]?\d*\.\d+|\d+', x)[0]
            unit = x.split(memory)[-1].lower()
            memory = float(memory)
            if unit == 'k' or unit == 'kb':
                memory = memory / 1024
            elif unit == 'm' or unit == 'mb':
                memory = memory
            elif unit == 'g' or unit == 'gb':
                memory = memory * 1024
            elif unit == 't' or unit == 'tb':
                memory = memory * 1024 * 1024
            else:
                return np.nan
        except Exception:
            return np.nan

        return memory

    @staticmethod
    def device_unit_boot_time(data):
        """
        原生数据类型时间的转化
        """
        if data is None:
            return np.nan
        return pd.to_numeric(data, errors='coerce') / 3600000

    def device_base_features(self, df_base):
        feature_dict = {}
        try:
            for col in ['hasNfc', 'net', 'height', 'width', 'cpu_num']:
                if col not in df_base.columns:
                    df_base[col] = np.nan
            df_base['net'] = df_base['net'].astype(str)
            df_base['height'] = df_base['height'].astype(float)
            df_base['width'] = df_base['width'].astype(float)
            df_base['cpu_num'] = df_base['cpu_num'].astype(float)
            df_base['os_version'] = df_base['os'].map(lambda x: x.split(' ')[0])
            df_base['is_nfc'] = df_base['hasNfc'].astype(float)

            # 时区
            tz_list = ['Asia/Jakarta', 'Asia/Makassar', 'Asia/Jayapura', 'Asia/Pontianak']
            feature_dict['tz_is_jakarta'] = df_base['tz'].apply(lambda x: 1 if x == 'Asia/Jakarta' else 0)[0]
            feature_dict['tz_is_makassar'] = df_base['tz'].apply(lambda x: 1 if x == 'Asia/Makassar' else 0)[0]
            feature_dict['tz_is_jayapura'] = df_base['tz'].apply(lambda x: 1 if x == 'Asia/Jayapura' else 0)[0]
            feature_dict['tz_is_pontianak'] = df_base['tz'].apply(lambda x: 1 if x == 'Asia/Pontianak' else 0)[0]
            feature_dict['tz_is_other'] = df_base['tz'].apply(lambda x: 1 if x not in tz_list else 0)[0]
            # 屏幕尺寸
            df_base['screen_size'] = df_base['height'] * df_base['width']
            feature_dict['os_is_ios_screen_size'] = df_base.apply(lambda row: row['screen_size'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_android_screen_size'] = df_base.apply(lambda row: row['screen_size'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            # NFC
            feature_dict['is_nfc'] = df_base['is_nfc'][0]
            # System Version
            feature_dict['os_android'] = df_base['os'].map(lambda x: 1 if x.split(' ')[0] == 'android' else 0)[0]
            feature_dict['os_ios'] = df_base['os'].map(lambda x: 1 if x.split(' ')[0] == 'ios' else 0)[0]
            feature_dict['os_android_version'] = df_base['os'].map(lambda x: float(x.split('.')[0].split(' ')[1]) if x.split(' ')[0] == 'android' else np.nan)[0]
            feature_dict['os_ios_version'] = df_base['os'].map(lambda x: float(x.split('.')[0].split(' ')[1]) if x.split(' ')[0] == 'ios' else np.nan)[0]
            # CPU
            feature_dict['cpu_number'] = df_base['cpu_num'][0]
            feature_dict['os_is_ios_cpu_number'] = df_base.apply(lambda row: row['cpu_num'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_android_cpu_number'] = df_base.apply(lambda row: row['cpu_num'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            # 系统内存
            df_base['memory_mb'] = df_base['mem'].apply(self.device_unit_normalize)
            feature_dict['memory_mb'] = df_base['memory_mb'][0]
            # 存储空间
            # 未使用存储空间
            df_base['app_avaliable_memory_mb'] = df_base['app_avaliable_memory'].apply(self.device_unit_normalize)
            feature_dict['app_avaliable_memory_mb'] = df_base['app_avaliable_memory_mb'][0]
            # 已使用存储空间
            df_base['app_free_memory_mb'] = df_base['app_free_memory'].apply(self.device_unit_normalize)
            feature_dict['app_free_memory_mb'] = df_base['app_free_memory_mb'][0]
            # 最大存储空间
            df_base['app_max_memory_mb'] = df_base['app_max_memory'].apply(self.device_unit_normalize)
            feature_dict['app_max_memory_mb'] = df_base['app_max_memory_mb'][0]
            feature_dict['os_is_ios_app_avaliable_memory_mb'] = df_base.apply(lambda row: row['app_avaliable_memory_mb'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_ios_app_free_memory_mb'] = df_base.apply(lambda row: row['app_free_memory_mb'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_ios_app_max_memory_mb'] = df_base.apply(lambda row: row['app_max_memory_mb'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_ios_memory_mb'] = df_base.apply(lambda row: row['memory_mb'] if row['os_version'] == 'ios' else np.nan, axis=1)[0]
            feature_dict['os_is_ios_memory_usage'] = feature_dict['os_is_ios_app_free_memory_mb'] / feature_dict['os_is_ios_app_max_memory_mb']
            feature_dict['os_is_android_app_avaliable_memory_mb'] = df_base.apply(lambda row: row['app_avaliable_memory_mb'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            feature_dict['os_is_android_app_free_memory_mb'] = df_base.apply(lambda row: row['app_free_memory_mb'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            feature_dict['os_is_android_app_max_memory_mb'] = df_base.apply(lambda row: row['app_max_memory_mb'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            feature_dict['os_is_android_memory_mb'] = df_base.apply(lambda row: row['memory_mb'] if row['os_version'] == 'android' else np.nan, axis=1)[0]
            # 开机时长
            # total_boot_time开机总时长
            # total_boot_time_wake开机使用长
            df_base['total_boot_time_hour'] = df_base.apply(lambda row: pd.to_numeric(row['total_boot_time'], errors='coerce') / 3600 if row['os_version'] == 'ios' else pd.to_numeric(row['total_boot_time'], errors='coerce') / 3600000, axis=1)
            df_base['total_boot_time_wake_hour'] = df_base.apply(lambda row: pd.to_numeric(row['total_boot_time_wake'], errors='coerce') / 3600 if row['os_version'] == 'ios' else pd.to_numeric(row['total_boot_time_wake'], errors='coerce') / 3600000, axis=1)
            df_base['total_boot_time_day'] = df_base['total_boot_time_hour'] / 24
            df_base['total_boot_time_wake_day'] = df_base['total_boot_time_wake_hour'] / 24
            feature_dict['total_boot_time_hour'] = df_base['total_boot_time_hour'][0]
            feature_dict['total_boot_time_wake_hour'] = df_base['total_boot_time_wake_hour'][0]
            feature_dict['total_boot_time_day'] = df_base['total_boot_time_day'][0]
            feature_dict['total_boot_time_wake_day'] = df_base['total_boot_time_wake_day'][0]
            # 设备风险
            df_base['brand_clean'] = df_base['brand'].apply(lambda x: x.lower())
            df_base['model_clean'] = df_base['model'].apply(lambda x: x.lower())
            df_base['brand_clean'] = df_base['brand_clean'].apply(lambda x: x.split('_')[-1])
            df_base['model_clean'] = df_base['model_clean'].apply(lambda x: x.split('_')[-1])
            df_base['phone_brand'] = df_base['brand_clean'] + '_' + df_base['model_clean']
            # 低风险设备
            feature_dict['is_good_phone_brand'] = df_base['phone_brand'].apply(lambda x: 1 if x in self.good_brand_v1_list else 0)[0]
            # 高风险设备
            feature_dict['is_bad_phone_brand'] = df_base['phone_brand'].apply(lambda x: 1 if x in self.bad_brand_v1_list else 0)[0]
        except Exception as e:
            print('PYTHON_ERROR',format_exc())
        return feature_dict

    def merge_feature(self, feature_dict, prefix=''):
        """
        特征合并
        """
        features_merge = {}
        for k, v in feature_dict.items():
            # 1.特征类型优化
            try:
                feature_value = round(v, 6)
            except:
                feature_value = v
            # 2.增加特征前缀
            feature_name = prefix + k
            features_merge[feature_name] = feature_value
        return features_merge

    def feature_extraction(self, data, save_index=True):
        self._init_some_value(data)
        feature_dict = self.device_base_features(self.df_base)
        feature_dict = self.merge_feature(feature_dict, prefix='risk_v1_device_')
        if save_index:
            feature_dict = self.save_index(feature_dict)
        return feature_dict
        

class Work:

    def __init__(self) -> None:
        # print("sqlResult",sqlResult)
        print("初始化一次")

    def do_work(self):
        parse_data = parseResult[0]['data']
        feature_dict = DeviceBaseFeature().feature_extraction(parse_data)
        return feature_dict

def __init_env():
    global work
    work = Work()

try:
    if not work:
        __init_env()
except NameError as e:
    __init_env()


result=work.do_work()
