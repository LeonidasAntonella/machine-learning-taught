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


class AppListFeature(object):
    def __init__(self):
        # 谷歌文件类
        self.GP_appDtls_id = get_obs_data(obsClient, bucketname, 'id_googlePlay_APPDtls_20240625.csv')
        self.GP_appDtls_id['is_inGP'] = 1
        # 监管机构类
        self.ojk_v1 = get_obs_data(obsClient, bucketname, 'ojk_pkglist_v1.csv')
        self.afpi_v1 = get_obs_data(obsClient, bucketname, 'afpi_pkglist_v1.csv')
        # 竞品类
        self.competing_v1 = get_obs_data(obsClient, bucketname, 'competing_pkglist_v1.csv')
        # 关键词搜索类
        self.sc_bank_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_bank_v1.csv')
        self.sc_cashloan_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_cashloan_v1.csv')
        self.sc_finance_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_finance_v1.csv')
        self.sc_investment_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_investment_v1.csv')
        self.sc_job_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_job_v1.csv')
        self.sc_wallet_v1 = get_obs_data(obsClient, bucketname, 'keywords_search_wallet_v1.csv')
        # 排行榜类
        self.rk_finance_v1 = get_obs_data(obsClient, bucketname, 'ranking_finance_v1.csv')
        self.rk_health_v1 = get_obs_data(obsClient, bucketname, 'ranking_health_v1.csv')
        self.rk_medical_v1 = get_obs_data(obsClient, bucketname, 'ranking_medical_v1.csv')
        self.rk_shopping_v1 = get_obs_data(obsClient, bucketname, 'ranking_shopping_v1.csv')
        self.rk_social_v1 = get_obs_data(obsClient, bucketname, 'ranking_social_v1.csv')
        self.rk_tools_v1 = get_obs_data(obsClient, bucketname, 'ranking_tools_v1.csv')
        self.rk_travel_v1 = get_obs_data(obsClient, bucketname, 'ranking_travel_v1.csv')
        # self.rk_education_v1 = pd.read_csv("conf/resources/rupiahcepat/ranking_education_v1.csv")
        # 分类IV效果一般不需要时间切片
        self.do_not_time_loop_category = ['is_competing_good', 'is_sc_bank', 'is_sc_finance', 'is_sc_investment',
                                          'is_sc_job', 'is_sc_wallet', 'is_ranking_medical', 'is_ranking_travel',
                                          'is_ranking_health', 'is_ranking_tools', 'is_ranking_shopping', 'isMedical',
                                          'isTravel', 'isHealth', 'isBusiness', 'isShopping', 'isProductivity',
                                          'isEducation', 'isTools']
        self.save_feature_list = get_obs_data(obsClient, bucketname, 'risk_v1_app_feature_list.csv')[
            'feature_name'].to_list()

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
            # 3.仅存储需要上线的特征
            if feature_name in self.save_feature_list:
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
        # APP更新距今天数, 2001年以前时间填充为nan
        df['last_update_day'] = self.date_diff(df['server_time'], df['last_update_time'])
        df.loc[df['last_update_time'] <= 1000000000, 'last_update_day'] = np.nan
        df['is_updated'] = 0
        df.loc[df['last_update_day'] < df['install_day'], 'is_updated'] = 1

        # 2. 特征计算
        # 2.1 合并app文件
        # 谷歌文件类
        df = pd.merge(df, self.GP_appDtls_id, how='left', on='pkgname')
        # 监管机构类
        df = pd.merge(df, self.ojk_v1, how='left', on='pkgname')
        df = pd.merge(df, self.afpi_v1, how='left', on='pkgname')
        # 竞品类
        df = pd.merge(df, self.competing_v1, how='left', on='pkgname')
        # 关键词搜索类
        df = pd.merge(df, self.sc_bank_v1, how='left', on='pkgname')
        df = pd.merge(df, self.sc_cashloan_v1, how='left', on='pkgname')
        df = pd.merge(df, self.sc_finance_v1, how='left', on='pkgname')
        df = pd.merge(df, self.sc_investment_v1, how='left', on='pkgname')
        df = pd.merge(df, self.sc_job_v1, how='left', on='pkgname')
        df = pd.merge(df, self.sc_wallet_v1, how='left', on='pkgname')
        # 排行榜类
        df = pd.merge(df, self.rk_finance_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_health_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_medical_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_shopping_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_social_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_tools_v1, how='left', on='pkgname')
        df = pd.merge(df, self.rk_travel_v1, how='left', on='pkgname')
        # df = pd.merge(df, self.rk_education_v1, how='left', on='pkgname')

        # 填充nan值
        label_columns = ['is_inGP', 'is_ojk', 'is_afpi', 'is_competing', 'is_competing_good', 'is_competing_bad',
                         'is_sc_bank', 'is_sc_cashloan', 'is_sc_finance', 'is_sc_investment', 'is_sc_job',
                         'is_sc_wallet',
                         'is_ranking_finance', 'is_ranking_health', 'is_ranking_medical',
                         'is_ranking_shopping', 'is_ranking_social', 'is_ranking_tools',
                         'is_ranking_travel',
                         # 'is_ranking_education',
                         ]
        df[label_columns] = df[label_columns].fillna(0)

        # 3. 其他预处理
        df['type'] = df['type'].astype(int)
        ## 系统预装软件在谷歌商店中且更新过
        # df['type'] = df[['type', 'is_inGP', 'is_updated']].apply(lambda row: 1 if row['type'] == 1 else (1 if row['is_inGP'] == 1 and row['is_updated'] == 1 else 0), axis=1)
        return df

    def dev_base_features(self, df):
        feature_dict = {}
        try:
            if df.shape[0] == 0:
                feature_dict['available'] = 0
            else:
                feature_dict['snap_time'] = df['server_time'].min()
                feature_dict['available'] = 1
                df_pre_app = df[df['type'] == 0]
                df_self_app = df[df['type'] == 1]
                feature_dict['whole_count'] = df.shape[0]
                feature_dict['self_install_count'] = df_self_app.shape[0]
                feature_dict['self_install_ratio'] = df['type'].mean()
                feature_dict['pre_install_count'] = df_pre_app.shape[0]
                feature_dict['pre_install_ratio'] = 1 - df['type'].mean()
                feature_dict['pre_install_day_median'] = df_pre_app['install_day'].median()
                feature_dict['pre_install_is_updated_ratio'] = df_pre_app['is_updated'].mean()
        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def inner_func(self, df, date='', key='', app_len=0, finance_len=0, whole_key_len=0):
        feature_dict = {}
        try:
            # 过滤不需要计算时间切片的分类
            if date != '' and key in self.do_not_time_loop_category:
                return feature_dict

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
                feature_dict['%sinstall_day_%smin' % (key_name, date_name)] = df['install_day'].min()
                feature_dict['%sinstall_day_%smax' % (key_name, date_name)] = df['install_day'].max()
                feature_dict['%sinstall_day_%smean' % (key_name, date_name)] = df['install_day'].mean()
                feature_dict['%sinstall_day_%smedian' % (key_name, date_name)] = df['install_day'].median()
                # 更新时长
                feature_dict['%slast_update_day_%smin' % (key_name, date_name)] = df['last_update_day'].min()
                feature_dict['%slast_update_day_%smax' % (key_name, date_name)] = df['last_update_day'].max()
                feature_dict['%slast_update_day_%smean' % (key_name, date_name)] = df['last_update_day'].mean()
                feature_dict['%slast_update_day_%smedian' % (key_name, date_name)] = df['last_update_day'].median()
                # 安装间隔时长
                feature_dict['%sinstall_interval_day_%smin' % (key_name, date_name)] = df['install_day'].diff(
                    periods=-1).min()
                feature_dict['%sinstall_interval_day_%smax' % (key_name, date_name)] = df['install_day'].diff(
                    periods=-1).max()
                feature_dict['%sinstall_interval_day_%smean' % (key_name, date_name)] = df['install_day'].diff(
                    periods=-1).mean()
                feature_dict['%sinstall_interval_day_%smedian' % (key_name, date_name)] = df['install_day'].diff(
                    periods=-1).median()
                # Google Play下架个数
                feature_dict['%sgoogle_play_removed_%scount' % (key_name, date_name)] = df[df['gp_removed'] == 1].shape[
                    0]
                # Google Play下架占比
                feature_dict['%sgoogle_play_removed_%sratio' % (key_name, date_name)] = df['gp_removed'].mean()
                # Google Play下载量级
                feature_dict['%sgoogle_play_installs_%smin' % (key_name, date_name)] = df['installs'].min()
                feature_dict['%sgoogle_play_installs_%smax' % (key_name, date_name)] = df['installs'].max()
                feature_dict['%sgoogle_play_installs_%smean' % (key_name, date_name)] = df['installs'].mean()
                feature_dict['%sgoogle_play_installs_%smedian' % (key_name, date_name)] = df['installs'].median()
                # Google Play打分
                feature_dict['%sgoogle_play_score_%smin' % (key_name, date_name)] = df['score'].min()
                feature_dict['%sgoogle_play_score_%smax' % (key_name, date_name)] = df['score'].max()
                feature_dict['%sgoogle_play_score_%smean' % (key_name, date_name)] = df['score'].mean()
                feature_dict['%sgoogle_play_score_%smedian' % (key_name, date_name)] = df['score'].median()
                # Google Play评论数量
                feature_dict['%sgoogle_play_reviews_%smin' % (key_name, date_name)] = df['reviews'].min()
                feature_dict['%sgoogle_play_reviews_%smax' % (key_name, date_name)] = df['reviews'].max()
                feature_dict['%sgoogle_play_reviews_%smean' % (key_name, date_name)] = df['reviews'].mean()
                feature_dict['%sgoogle_play_reviews_%smedian' % (key_name, date_name)] = df['reviews'].median()
                # Google Play评分数量
                feature_dict['%sgoogle_play_ratings_%smin' % (key_name, date_name)] = df['ratings'].min()
                feature_dict['%sgoogle_play_ratings_%smax' % (key_name, date_name)] = df['ratings'].max()
                feature_dict['%sgoogle_play_ratings_%smean' % (key_name, date_name)] = df['ratings'].mean()
                feature_dict['%sgoogle_play_ratings_%smedian' % (key_name, date_name)] = df['ratings'].median()
                # Google Play评论数量安装占比
                feature_dict['%sgoogle_play_reviews_ratio_%smin' % (key_name, date_name)] = (
                            df['reviews'] / df['installs']).min()
                feature_dict['%sgoogle_play_reviews_ratio_%smax' % (key_name, date_name)] = (
                            df['reviews'] / df['installs']).max()
                feature_dict['%sgoogle_play_reviews_ratio_%smean' % (key_name, date_name)] = (
                            df['reviews'] / df['installs']).mean()
                feature_dict['%sgoogle_play_reviews_ratio_%smedian' % (key_name, date_name)] = (
                            df['reviews'] / df['installs']).median()
                # Google Play评分数量安装占比
                feature_dict['%sgoogle_play_ratings_ratio_%smin' % (key_name, date_name)] = (
                            df['ratings'] / df['installs']).min()
                feature_dict['%sgoogle_play_ratings_ratio_%smax' % (key_name, date_name)] = (
                            df['ratings'] / df['installs']).max()
                feature_dict['%sgoogle_play_ratings_ratio_%smean' % (key_name, date_name)] = (
                            df['ratings'] / df['installs']).mean()
                feature_dict['%sgoogle_play_ratings_ratio_%smedian' % (key_name, date_name)] = (
                            df['ratings'] / df['installs']).median()

                # 当前类别 / APPList
                if app_len:
                    feature_dict['%sin_app_%sratio' % (key_name, date_name)] = self.division_method(df[key].sum(),
                                                                                                    app_len)

                # 当前类别 / Google Play Finance APPList
                if finance_len:
                    feature_dict['%sin_finance_%sratio' % (key_name, date_name)] = self.division_method(df[key].sum(),
                                                                                                        finance_len)

                # 安装时间趋势特征计算
                if date != '' and whole_key_len > 0:
                    feature_dict['%s%sinstall_in_history_ratio' % (key_name, date_name)] = self.division_method(
                        df.shape[0], whole_key_len)

                # 仅首次计算-类别标签不计算
                if key == '':
                    feature_dict['ojk_in_ojk_list_%sratio' % date_name] = self.division_method(
                        df[df['is_ojk'] == 1].shape[0], self.ojk_v1.shape[0])
                    feature_dict['afpi_in_afpi_list_%sratio' % date_name] = self.division_method(
                        df[df['is_afpi'] == 1].shape[0], self.afpi_v1.shape[0])
                    feature_dict['competing_in_competing_list_%sratio' % date_name] = self.division_method(
                        df[df['is_competing'] == 1].shape[0], self.competing_v1.shape[0])
                    feature_dict['competing_bad_in_competing_list_%sratio' % date_name] = self.division_method(
                        df[df['is_competing_bad'] == 1].shape[0], self.competing_v1.shape[0])
                    feature_dict['competing_bad_in_competing_bad_list_%sratio' % date_name] = self.division_method(
                        df[df['is_competing_bad'] == 1].shape[0], self.competing_v1['is_competing_bad'].sum())
                    feature_dict['sc_cashloan_in_sc_cashloan_list_%sratio' % date_name] = self.division_method(
                        df[df['is_sc_cashloan'] == 1].shape[0], self.sc_cashloan_v1.shape[0])
                    feature_dict['ranking_finance_in_ranking_finance_list_%sratio' % date_name] = self.division_method(
                        df[df['is_ranking_finance'] == 1].shape[0], self.rk_finance_v1.shape[0])
                    feature_dict['ranking_travel_in_ranking_travel_list_%sratio' % date_name] = self.division_method(
                        df[df['is_ranking_travel'] == 1].shape[0], self.rk_travel_v1.shape[0])
                    # IV效果不佳-不进行计算
                    # feature_dict['in_google_play_%scount' % date_name] = df[df['is_inGP'] == 1].shape[0]
                    # feature_dict['in_google_play_%sratio' % date_name] = df['is_inGP'].mean()
                    # feature_dict['competing_good_in_competing_list_%sratio' % date_name] = self.division_method(df[df['is_competing_good'] == 1].shape[0], self.competing_v1.shape[0])
                    # feature_dict['competing_good_in_competing_good_list_%sratio' % date_name] = self.division_method(df[df['is_competing_good'] == 1].shape[0], self.competing_v1['is_competing_good'].sum())
                    # feature_dict['sc_bank_in_sc_bank_list_%sratio' % date_name] = self.division_method(df[df['is_sc_bank'] == 1].shape[0], self.sc_bank_v1.shape[0])
                    # feature_dict['sc_finance_in_sc_finance_list_%sratio' % date_name] = self.division_method(df[df['is_sc_finance'] == 1].shape[0], self.sc_finance_v1.shape[0])
                    # feature_dict['sc_investment_in_sc_investment_list_%sratio' % date_name] = self.division_method(df[df['is_sc_investment'] == 1].shape[0], self.sc_investment_v1.shape[0])
                    # feature_dict['sc_job_in_sc_job_list_%sratio' % date_name] = self.division_method(df[df['is_sc_job'] == 1].shape[0], self.sc_job_v1.shape[0])
                    # feature_dict['sc_wallet_in_sc_wallet_list_%sratio' % date_name] = self.division_method(df[df['is_sc_wallet'] == 1].shape[0], self.sc_wallet_v1.shape[0])
                    # feature_dict['ranking_education_in_ranking_education_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_education'] == 1].shape[0], self.rk_education_v1.shape[0])
                    # feature_dict['ranking_health_in_ranking_health_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_health'] == 1].shape[0], self.rk_health_v1.shape[0])
                    # feature_dict['ranking_medical_in_ranking_medical_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_medical'] == 1].shape[0], self.rk_medical_v1.shape[0])
                    # feature_dict['ranking_shopping_in_ranking_shopping_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_shopping'] == 1].shape[0], self.rk_shopping_v1.shape[0])
                    # feature_dict['ranking_social_in_ranking_social_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_social'] == 1].shape[0], self.rk_social_v1.shape[0])
                    # feature_dict['ranking_tools_in_ranking_tools_list_%sratio' % date_name] = self.division_method(df[df['is_ranking_tools'] == 1].shape[0], self.rk_tools_v1.shape[0])

        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def one_hot_base_func(self, df, key=''):
        feature_dict = {}
        try:
            df_query = df[df[key] == 1][['appname', 'install_day', 'last_update_day']]
            if df_query.shape[0] > 0:
                for data_dict in df_query.to_dict('records'):
                    appname = data_dict['appname']
                    feature_dict['appname_%s_is_install' % appname] = 1
                    feature_dict['appname_%s_install_day' % appname] = data_dict['install_day']
                    feature_dict['appname_%s_last_update_day' % appname] = data_dict['last_update_day']
        except Exception as e:
            print('PYTHON_ERROR', format_exc())
        return feature_dict

    def dev_app_self_install_features(self, df):
        feature_dict = {}
        try:
            if df.shape[0] > 0:
                # 筛选自装app
                df = df[df['type'] == 1]
                df['isFinance'] = 0
                df.loc[df['category'] == 'FINANCE', 'isFinance'] = 1
                df['isTools'] = 0
                df.loc[df['category'] == 'TOOLS', 'isTools'] = 1
                df['isEducation'] = 0
                df.loc[df['category'] == 'EDUCATION', 'isEducation'] = 1
                df['isProductivity'] = 0
                df.loc[df['category'] == 'PRODUCTIVITY', 'isProductivity'] = 1
                df['isShopping'] = 0
                df.loc[df['category'] == 'SHOPPING', 'isShopping'] = 1
                df['isBusiness'] = 0
                df.loc[df['category'] == 'BUSINESS', 'isBusiness'] = 1
                df['isHealth'] = 0
                df.loc[df['category'] == 'HEALTH_AND_FITNESS', 'isHealth'] = 1
                df['isTravel'] = 0
                df.loc[df['category'] == 'TRAVEL_AND_LOCAL', 'isTravel'] = 1
                df['isMedical'] = 0
                df.loc[df['category'] == 'MEDICAL', 'isMedical'] = 1
                df['isVehicles'] = 0
                df.loc[df['category'] == 'AUTO_AND_VEHICLES', 'isVehicles'] = 1
                df['isFood'] = 0
                df.loc[df['category'] == 'FOOD_AND_DRINK', 'isFood'] = 1
                df['isGameCasino'] = 0
                df.loc[df['category'] == 'GAME_CASINO', 'isGameCasino'] = 1

                # app install 时间窗
                df_whole = df
                df_last_3d = df[df['install_day'] <= 3]
                df_last_7d = df[df['install_day'] <= 7]
                df_last_30d = df[df['install_day'] <= 30]
                df_last_90d = df[df['install_day'] <= 90]
                df_last_180d = df[df['install_day'] <= 180]
                df_last_365d = df[df['install_day'] <= 365]
                time_series_map = {'': df_whole, 'last_3d': df_last_3d, 'last_7d': df_last_7d, 'last_30d': df_last_30d,
                                   'last_90d': df_last_90d, 'last_180d': df_last_180d, 'last_365d': df_last_365d}

                # 计算整体APP特征
                for time_series, df_now in time_series_map.items():
                    app_len = df_now.shape[0]
                    # 时间切片数据为空，直接跳过不计算
                    if app_len == 0:
                        continue
                    finance_len = df_now['isFinance'].sum()
                    feature_dict.update(self.inner_func(df_now, date=time_series))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_ojk'] == 1], date=time_series, key='is_ojk', app_len=app_len,
                                        finance_len=finance_len, whole_key_len=df_whole['is_ojk'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['is_afpi'] == 1], date=time_series, key='is_afpi',
                                                        app_len=app_len, finance_len=finance_len,
                                                        whole_key_len=df_whole['is_afpi'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_competing'] == 1], date=time_series, key='is_competing',
                                        app_len=app_len, finance_len=finance_len,
                                        whole_key_len=df_whole['is_competing'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['is_competing_good'] == 1], date=time_series,
                                                        key='is_competing_good', app_len=app_len,
                                                        finance_len=finance_len,
                                                        whole_key_len=df_whole['is_competing_good'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['is_competing_bad'] == 1], date=time_series,
                                                        key='is_competing_bad', app_len=app_len,
                                                        finance_len=finance_len,
                                                        whole_key_len=df_whole['is_competing_bad'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_sc_bank'] == 1], date=time_series, key='is_sc_bank',
                                        app_len=app_len, finance_len=finance_len,
                                        whole_key_len=df_whole['is_sc_bank'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_sc_cashloan'] == 1], date=time_series, key='is_sc_cashloan',
                                        app_len=app_len, finance_len=finance_len,
                                        whole_key_len=df_whole['is_sc_cashloan'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_sc_finance'] == 1], date=time_series, key='is_sc_finance',
                                        app_len=app_len, finance_len=finance_len,
                                        whole_key_len=df_whole['is_sc_finance'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['is_sc_investment'] == 1], date=time_series,
                                                        key='is_sc_investment', app_len=app_len,
                                                        finance_len=finance_len,
                                                        whole_key_len=df_whole['is_sc_investment'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_sc_job'] == 1], date=time_series, key='is_sc_job',
                                        app_len=app_len, whole_key_len=df_whole['is_sc_job'].sum()))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['is_sc_wallet'] == 1], date=time_series, key='is_sc_wallet',
                                        app_len=app_len, finance_len=finance_len,
                                        whole_key_len=df_whole['is_sc_wallet'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_finance'] == 1], date=time_series,
                                                        key='is_ranking_finance', app_len=app_len,
                                                        finance_len=finance_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_health'] == 1], date=time_series,
                                                        key='is_ranking_health', app_len=app_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_medical'] == 1], date=time_series,
                                                        key='is_ranking_medical', app_len=app_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_shopping'] == 1], date=time_series,
                                                        key='is_ranking_shopping', app_len=app_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_social'] == 1], date=time_series,
                                                        key='is_ranking_social', app_len=app_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_tools'] == 1], date=time_series,
                                                        key='is_ranking_tools', app_len=app_len))
                    feature_dict.update(self.inner_func(df_now[df_now['is_ranking_travel'] == 1], date=time_series,
                                                        key='is_ranking_travel', app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isFinance'] == 1], date=time_series, key='isFinance',
                                        app_len=app_len, whole_key_len=df_whole['isFinance'].sum()))
                    feature_dict.update(self.inner_func(df_now[df_now['isTools'] == 1], date=time_series, key='isTools',
                                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isEducation'] == 1], date=time_series, key='isEducation',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isProductivity'] == 1], date=time_series, key='isProductivity',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isShopping'] == 1], date=time_series, key='isShopping',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isBusiness'] == 1], date=time_series, key='isBusiness',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isHealth'] == 1], date=time_series, key='isHealth',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isTravel'] == 1], date=time_series, key='isTravel',
                                        app_len=app_len))
                    feature_dict.update(
                        self.inner_func(df_now[df_now['isMedical'] == 1], date=time_series, key='isMedical',
                                        app_len=app_len))
                    # IV效果不佳-不进行计算
                    # feature_dict.update(self.inner_func(df_now[df_now['isGameCasino'] == 1], date=time_series, key='isGameCasino', app_len=app_len))
                    # feature_dict.update(self.inner_func(df_now[df_now['isFood'] == 1], date=time_series, key='isFood', app_len=app_len))
                    # feature_dict.update(self.inner_func(df_now[df_now['isVehicles'] == 1], date=time_series, key='isVehicles', app_len=app_len))
                    # feature_dict.update(self.inner_func(df_now[df_now['is_ranking_education'] == 1], date=time_series, key='is_ranking_education', app_len=app_len))

                # 计算竞品one-hot特征
                feature_dict.update(self.one_hot_base_func(df_whole, key='is_competing'))

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
        feature_dict = self.merge_feature(feature_dict, prefix='risk_v1_app_')
        if save_index:
            feature_dict = self.save_index(feature_dict)
        return feature_dict


class Work:

    def __init__(self) -> None:
        # print("sqlResult",sqlResult)
        logger.info("work_init_once")
        self.app_cls = AppListFeature()

    def do_work(self):
        parse_data = parseResult[0]['data']
        # 当APPList为空时直接返回空字典，避免写入redis缓存。导致正常数据不计算
        if len(parse_data.get('apps', [])) == 0:
            return {}   # 潘菲上线后优化成 return   安卓： {'__flag': {'feature_add_tag': 2, 'redis_tag': 0}}   ios： {'__flag': {'feature_add_tag': 2, 'redis_tag': 1}} 
        feature_dict = self.app_cls.feature_extraction(parse_data)
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