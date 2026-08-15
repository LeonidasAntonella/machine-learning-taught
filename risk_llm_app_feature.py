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
import logging

logger = logging.getLogger('feature')


bucketname = 'risk-idn-hyfeature-config'
# obsClient = ObsClient(
#     access_key_id='SYKZD79NRI1ABAKPUDXO',
#     secret_access_key='PubOd3ZpboMLeVaozvTPN9HfVS8L0DuEE6JB4a4a',
#     server='https://obs.ap-southeast-4.myhuaweicloud.com'
# )

obsClient = ObsClient(
    access_key_id='HPUAR0K2INTLXE4WY87E',
    secret_access_key='r7oDfBARCD0PgykHZUmbfNFRGqKPyZc9UCKXhiUk',
    server='https://obs.ap-southeast-4.myhuaweicloud.com'
)


def get_obs_data(obsClient, bucketname, file_name):
    resp = obsClient.getObject(bucketname, file_name, loadStreamInMemory=True)

    if resp.status < 300:
        csv_reader = resp.body.buffer.decode('utf-8').strip().split('\n')
        tab_header = [i.replace('\r', '') for i in csv_reader[0].split(',')]
        print(tab_header)
        tab_info = [row.split(',') for row in csv_reader[1:]]
        tab_res = [dict(zip(tab_header, row)) for row in tab_info]
        obs_df = pd.DataFrame(tab_res)
        obs_df = obs_df.replace('', np.nan)
        for col in obs_df.columns:
            try:
                obs_df[col] = obs_df[col].astype(float)
            except:
                continue
        return obs_df
    else:
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
        return None


class LLMAppFeature(object):
    def __init__(self):
        # LLM打标类
        self.llm_label_v1 = get_obs_data(obsClient, bucketname, 'llm_label_v1.csv')

    @staticmethod
    def date_diff(end_time, start_time):
        diff_days = (end_time - start_time) // (24 * 60 * 60)
        return diff_days

    @staticmethod
    def division_method(numerator, denominator):
        try:
            return numerator / denominator
        except:
            return np.nan

    def merge_feature(self, feature_dict, prefix=''):
        """
        特征合并
        """
        features_merge = {}
        for k, v in feature_dict.items():
            # 1.特征类型优化
            try:
                feature_value = np.nan if v in [-np.inf, np.inf] else v
                feature_value = round(feature_value, 6)
            except:
                feature_value = v
            # 2.增加特征前缀
            feature_name = prefix + k
            features_merge[feature_name] = feature_value
        return features_merge

    def _init_some_value(self, data: dict):
        if data:
            self.server_time = data['server_time']
            self.imei = data['base']['imei']
            self.account_id = str(data['base'].get('account_id', '-9999'))
            self.df_app = pd.json_normalize(data.get('apps', []))
            self.df_app['server_time'] = self.server_time
            self.df_app['imei'] = self.imei
            self.df_app['account_id'] = self.account_id
        else:
            self.df_app = pd.DataFrame()

    def save_index(self, data):
        return {'account_id': self.account_id, 'imei': self.imei, 'data': data, 'create_time': int(time.time()) * 1000, '__flag': {'feature_add_tag': 1, 'redis_tag': 1}}

    def preprocess_data(self, df):
        """
            {
            "appname": "Chrome",                       //APP名
            "installtime_utc": "2008-12-31 16:00:00",  //安装时间UTC
            "last_timestamps": "1555129589314",        //更新时间-时间戳
            "installtime": "2008-12-31 21:30:00",      //安装时间
            "pkgname": "com.android.chrome",           //包名
            "timestamps": "1230739200000",             //安装时间-时间戳
            "type": "0",                               //是否自装 1自装 0预装
            "endcall":"0"                              //1，表示有挂断权限、0表示没有权限
            },
        """
        # 判断是否为空，ios都为空拿不到直接返回!
        if df.shape[0] == 0:
            return df

        # 1. 数据预处理
        # 1.1 app_name预处理，去除appname列中包含的特殊字符以及空格
        df['appname_origin'] = df['appname']
        df['appname'] = df.appname.str.replace(' |\\.|\\-|\\*|#|\\[|\\]|\\&|\\(|\\)|@', '')
        df['appname'] = df.appname.str.lower()
        # 1.2 时间数据预处理
        df['server_time'] = df['server_time'].apply(
            lambda x: int(str(x)[0:10]) if pd.isnull(x) == False and len(str(x)) > 0 else np.nan)
        df['install_time'] = df['timestamps'].apply(
            lambda x: int(str(x)[0:10]) if pd.isnull(x) == False and len(str(x)) > 0 else np.nan)
        df['last_update_time'] = df['last_timestamps'].apply(
            lambda x: int(str(x)[0:10]) if pd.isnull(x) == False and len(str(x)) > 0 else np.nan)
        # APP安装距今天数, 2001年以前时间填充为nan
        df['install_day'] = self.date_diff(df['server_time'], df['install_time'])
        df.loc[df['install_time'] <= 1000000000, 'install_day'] = np.nan
        df.loc[df['install_time'] >= 3000000000, 'install_day'] = np.nan
        # APP更新距今天数, 2001年以前时间填充为nan
        df['last_update_day'] = self.date_diff(df['server_time'], df['last_update_time'])
        df.loc[df['last_update_time'] <= 1000000000, 'last_update_day'] = np.nan
        df.loc[df['last_update_time'] >= 3000000000, 'last_update_day'] = np.nan
        df['is_updated'] = 0
        df.loc[df['last_update_day'] < df['install_day'], 'is_updated'] = 1

        # 2. 特征计算
        # 2.1 合并app文件
        # LLM打标类
        df = pd.merge(df, self.llm_label_v1, how='left', on='pkgname')

        # 填充nan值
        label_columns = ['business_blue_collar', 'business_micro_businesses', 'business_white_collar',
                         'consumer_business_travelers', 'consumer_eshopping', 'consumer_local_life',
                         'consumer_offline_payment', 'consumer_paylater',
                         'finance_bank', 'finance_car_loan', 'finance_cash_loan',
                         'finance_investment', 'finance_real_estate_loan',
                         'risk_casino_game', 'risk_virtual_coin',
                         'social_education', 'social_entertainment', 'social_religious',
                         'is_business', 'is_consumer', 'is_finance',
                         # 'is_risk', 'is_social',
                         ]
        df[label_columns] = df[label_columns].fillna(0)

        # 3. 其他预处理
        df['type'] = df['type'].astype(int)
        return df

    def dev_base_features(self, df):
        feature_dict = {}
        try:
            if df.shape[0] == 0:
                feature_dict['available'] = 0
            else:
                feature_dict['available'] = 1
                feature_dict['snap_time'] = df['server_time'].min()
        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def inner_func(self, df, date='', key='', app_len=0, whole_key_len=0):
        feature_dict = {}
        try:
            if df.shape[0] > 0:
                key_name = key if key == '' else key.replace('is_', '').replace('is', '').lower() + '_'
                date_name = date if date == '' else date + '_'
                # sort dataframe used install time
                df.sort_values(['installtime', 'appname'], ascending=[True, True], inplace=True)
                # 安装个数
                feature_dict['%sinstall_%scount' % (key_name, date_name)] = df.shape[0]
                # 更新个数
                feature_dict['%supdated_%scount' % (key_name, date_name)] = df[df['is_updated'] == 1].shape[0]
                # 更新占比
                feature_dict['%supdated_%sratio' % (key_name, date_name)] = df['is_updated'].mean()
                # 安装时长
                feature_dict['%sinstall_day_%smax' % (key_name, date_name)] = df['install_day'].max()
                feature_dict['%sinstall_day_%smean' % (key_name, date_name)] = df['install_day'].mean()
                # 更新时长
                feature_dict['%slast_update_day_%smax' % (key_name, date_name)] = df['last_update_day'].max()
                feature_dict['%slast_update_day_%smean' % (key_name, date_name)] = df['last_update_day'].mean()
                # 安装间隔时长
                feature_dict['%sinstall_interval_day_%smin' % (key_name, date_name)] = df['install_day'].diff(periods=-1).min()
                feature_dict['%sinstall_interval_day_%smax' % (key_name, date_name)] = df['install_day'].diff(periods=-1).max()
                feature_dict['%sinstall_interval_day_%smean' % (key_name, date_name)] = df['install_day'].diff(periods=-1).mean()
                # 当前类别 / APPList
                if app_len:
                    feature_dict['%sin_app_%sratio' % (key_name, date_name)] = self.division_method(df[key].sum(), app_len)
                # 安装时间趋势特征计算
                if date != '' and whole_key_len > 0:
                    feature_dict['%s%sinstall_in_history_ratio' % (key_name, date_name)] = self.division_method(df.shape[0], whole_key_len)

        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def dev_app_self_install_features(self, df):
        feature_dict = {}
        label_columns = ['business_blue_collar', 'business_micro_businesses', 'business_white_collar',
                         'consumer_business_travelers', 'consumer_eshopping', 'consumer_local_life',
                         'consumer_offline_payment', 'consumer_paylater',
                         'finance_bank', 'finance_car_loan', 'finance_cash_loan',
                         'finance_investment', 'finance_real_estate_loan',
                         'risk_casino_game', 'risk_virtual_coin',
                         'social_education', 'social_entertainment', 'social_religious',
                         'is_business', 'is_consumer', 'is_finance',
                         #'is_risk', 'is_social',
                         ]
        try:
            if df.shape[0] > 0:
                # 筛选自装app
                df = df[df['type'] == 1]
                # app install 时间窗
                df_whole = df
                df_last_7d = df[df['install_day'] <= 7]
                df_last_30d = df[df['install_day'] <= 30]
                df_last_90d = df[df['install_day'] <= 90]
                df_last_180d = df[df['install_day'] <= 180]
                time_series_map = {
                                   '': df_whole,
                                   'last_7d': df_last_7d,
                                   'last_30d': df_last_30d,
                                   'last_90d': df_last_90d,
                                   'last_180d': df_last_180d,
                                   }

                # 计算整体APP特征
                for time_series, df_now in time_series_map.items():
                    app_len = df_now.shape[0]
                    # 时间切片数据为空，直接跳过不计算
                    if app_len == 0:
                        continue
                    for label in label_columns:
                        feature_dict.update(self.inner_func(df_now[df_now[label] == 1], date=time_series, key=label, app_len=app_len, whole_key_len=df_whole[label].sum()))
        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def device_apps_features(self, df):
        feature_dict = {}
        df = self.preprocess_data(df)
        df_base_app_feature = self.dev_base_features(df)
        df_self_app_feature = self.dev_app_self_install_features(df)
        feature_dict.update(df_base_app_feature)
        feature_dict.update(df_self_app_feature)
        return feature_dict

    def feature_extraction(self, data, save_index=True):
        self._init_some_value(data)
        feature_dict = self.device_apps_features(self.df_app)
        feature_dict = self.merge_feature(feature_dict, prefix='llm_app_')
        if save_index:
            feature_dict = self.save_index(feature_dict)
        return feature_dict


class Work:

    def __init__(self) -> None:
        # print("sqlResult",sqlResult)
        logger.info("work_init_once")
        self.llm_app_cls = LLMAppFeature()

    def do_work(self):
        parse_data = parseResult[0]['data']
        # 当APPList为空时直接返回空字典，避免写入redis缓存。导致正常数据不计算
        if len(parse_data.get('apps', [])) == 0:
            return {}   # 潘菲上线后优化成 return   安卓： {'__flag': {'feature_add_tag': 2, 'redis_tag': 0}}   ios： {'__flag': {'feature_add_tag': 2, 'redis_tag': 1}}
        feature_dict = self.llm_app_cls.feature_extraction(parse_data)
        return feature_dict


def __init_env():
    global work
    work = Work()


try:
    if not work:
        __init_env()
except NameError as e:
    __init_env()

result = work.do_work()




