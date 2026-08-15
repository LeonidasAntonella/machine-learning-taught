# compile_once_init_once_v2
# 首行必须是上面的格式，否则不会使用单例模式
import itertools
import warnings

warnings.filterwarnings("ignore")
import time
import json
import pandas as pd
import numpy as np


class Work:

    def __init__(self) -> None:

        self.top_set = {'AFDC239', 'AFDC168'}
        self.mid_set = {'AFDC242', 'AFDC230', 'AFDC150', 'AFDC130', 'AFDC255'}
        self.day_list = [30, 90, 360, 'all']
        self.last3d_ins_list = ["easycash", "indosaku", "adapundi", "360kredi", "adakami", "ktakilat", "pinjamduit",
                                "julo", "finplus", "cairin", "danarupiah", "uatas", "samir", "kreditpintar", "asetku",
                                "pinjam winwin", "uangme", "pinjamyuk", "spinjam", "indonada"]
        self.COMPETING_MAP = {'AFDC239': 'easycash',
                             'AFDC255': 'adapundi',
                             'AFDC230': 'kp',
                             'AFDC242': 'adakami',
                             'AFDC130': 'kredivo',
                             'AFDC212': 'optima',
                             'AFDC168': 'shopee_paylater',
                             'AFDC243': 'akulaku',
                             'AFDC123': 'gopay_later',
                             'AFDC150': 'julo',
                             'AFDC129': 'indodana',
                             'AFDC225': 'pinjamwinwin',
                             'AFDC209': 'samir',
                             'AFDC215': '360kredi',
                             'AFDC237': 'pinjamduit',
                             'AFDC263': 'bantusaku',
                             }

        print("初始化一次")

    @staticmethod
    def replace_dict_keys(d, old, new):
        new_dict = {}

        for key, value in d.items():
            new_key = key.replace(old, new)

            new_dict[new_key] = value

        return new_dict

    @staticmethod
    def calculate_stats(df, filter_col, time_thresholds, stat_col, metrics, prefix=''):
        """
        根据过滤列 (filter_col) 和阈值 (filter_threshold) 过滤数据，
        然后根据所需的统计项 (metrics) 计算统计列 (stat_col) 的最大值、最小值和/或均值。

        参数:
        df (pd.DataFrame): 数据框，包含过滤列和统计列。
        filter_col (str): 用于筛选的列名。
        time_thresholds (list): 用于筛选的阈值。
        stat_col (str): 需要计算统计值的列名。
        metrics (list): 包含需要计算的统计项，如 'max', 'min', 'mean'。
        prefix (list): 返回特征前缀

        返回:
        dict: 包含所需统计项的字典。
        """
        results = {}
        for day in time_thresholds:
            if day == 'all':
                filtered_df = df
            else:
                filtered_df = df[df[filter_col] < day]

            if 'max' in metrics:
                results[f'{prefix}max_{day}d'] = filtered_df[stat_col].max()
            if 'count' in metrics:
                results[f'{prefix}num_{day}d'] = filtered_df[stat_col].shape[0]
            if 'nunique' in metrics:
                results[f'{prefix}nunique_{day}d'] = filtered_df[stat_col].nunique()

        return results

    def prepare_df(self, datas=None, df=None, inquiry_date=None):
        if df is None:
            df = pd.DataFrame(datas)

        def peal_df(row):
            return row

        df['tgl_perjanjian_borrower'] = np.where(df['tgl_perjanjian_borrower'] < '2000-01-01', np.nan,
                                                 df['tgl_perjanjian_borrower'])
        df['tgl_penyaluran_dana'] = np.where(df['tgl_penyaluran_dana'] < '2000-01-01', np.nan,
                                             df['tgl_penyaluran_dana'])
        df['tgl_pelaporan_data'] = np.where(df['tgl_pelaporan_data'] < '2000-01-01', np.nan, df['tgl_pelaporan_data'])
        df['tgl_jatuh_tempo_pinjaman'] = np.where(df['tgl_jatuh_tempo_pinjaman'] < '2000-01-01', np.nan,
                                                  df['tgl_jatuh_tempo_pinjaman'])
        df['tgl_jatuh_tempo_pinjaman'] = np.where(df['tgl_jatuh_tempo_pinjaman'] == '9999-12-31', np.nan,
                                                  df['tgl_jatuh_tempo_pinjaman'])

        df = df.sort_values(by='tgl_perjanjian_borrower')
        df['apply_date'] = pd.to_datetime(df['tgl_perjanjian_borrower'])
        df['loan_date'] = pd.to_datetime(df['tgl_penyaluran_dana'])
        df['loan_mon'] = df['tgl_penyaluran_dana'].str[:7]
        df['deadline_date'] = pd.to_datetime(df['tgl_jatuh_tempo_pinjaman'])

        df['repay_amount'] = df['nilai_pendanaan'] - df['sisa_pinjaman_berjalan']

        df['periods'] = (df['deadline_date'] - df['loan_date']).dt.days
        df['apply_diff_day'] = df['apply_date'].diff().dt.days

        # Put in
        df['inq_gap_loan_days'] = (inquiry_date - df['loan_date']).dt.days

        # Put it outside
        # df = df[(df.nilai_pendanaan > 2000) & (df.id_penyelenggara != 'AFDC233')]
        df = df.apply(peal_df, axis=1)

        return df

    def transactional_features(self, df):
        fea = {}
        for k, t_df in {
            '_cashloan': df[df.sub_tipe_pinjaman == 'Onetime Loan / Cash Loan'],
            '': df
        }.items():
            fea.update(self.calculate_stats(t_df, 'inq_gap_loan_days', self.day_list, 'nilai_pendanaan', ['max'],
                                            f'afpi{k}_loan_amount_'))
            fea.update(self.calculate_stats(t_df, 'inq_gap_loan_days', self.day_list, 'sisa_pinjaman_berjalan', ['max'],
                                            f'afpi{k}_balance_amount_'))

        fea.update(
            self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'nilai_pendanaan', ['count'], f'afpi_loan_'))
        fea.update(self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'apply_diff_day', ['max'],
                                        f'afpi_apply_diff_day_'))
        fea['afpi_mon_loan_num_max'] = df.groupby('loan_mon').size().max()
        combinations = list(itertools.combinations(self.day_list, 2))
        for a, b in combinations:
            if fea[f'afpi_loan_num_{b}d'] != 0:  # 判断分母是否为0
                fea[f'afpi_loan_num_{a}_{b}_rate'] = round(fea[f'afpi_loan_num_{a}d'] / fea[f'afpi_loan_num_{b}d'], 4)

        return fea

    def repay_features(self, df):
        fea = {}
        for k, t_df in {
            '_cashloan': df[df.sub_tipe_pinjaman == 'Onetime Loan / Cash Loan'],
            '': df
        }.items():
            fea.update(self.calculate_stats(t_df, 'inq_gap_loan_days', self.day_list, 'repay_amount', ['max'],
                                            f'afpi{k}_repay_amount_'))
        for day in self.day_list:
            if day == 'all':
                day_df = df
            else:
                day_df = df[df.inq_gap_loan_days < day]
            if day_df.empty:
                continue
            fea[f'afpi_repay_amount_rate_{day}d'] = round(
                day_df['repay_amount'].sum() / day_df['nilai_pendanaan'].sum(), 4)

        return fea

    def period_features(self, df):
        fea = {}
        fea.update(
            self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'periods', ['max'], f'afpi_loan_periods_'))
        fea.update(self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'inq_gap_loan_days', ['max'],
                                        f'afpi_inq_gap_loan_days_'))
        fea['afpi_loan_gap_days'] = (df['loan_date'].max() - df['loan_date'].min()).days

        return fea

    def overdue_features(self, df):
        fea = {}
        fea.update(
            self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'dpd_max', ['max'], f'afpi_overdue_his_dpd_'))
        fea.update(self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'dpd_terakhir', ['max'],
                                        f'afpi_overdue_cur_dpd_'))
        fea.update(self.calculate_stats(df[df.dpd_terakhir > 0], 'inq_gap_loan_days', self.day_list, 'nilai_pendanaan',
                                        ['max'], f'afpi_overdue_cur_loan_amount_'))
        fea.update(
            self.calculate_stats(df[df.dpd_terakhir > 0], 'inq_gap_loan_days', self.day_list, 'sisa_pinjaman_berjalan',
                                 ['max'], f'afpi_overdue_cur_balance_amount_'))
        fea.update(
            self.calculate_stats(df[df.dpd_terakhir > 0], 'inq_gap_loan_days', self.day_list, 'sisa_pinjaman_berjalan',
                                 ['count'], f'afpi_overdue_cur_'))
        fea.update(
            self.calculate_stats(df[df.dpd_max > 0], 'inq_gap_loan_days', self.day_list, 'nilai_pendanaan', ['max'],
                                 f'afpi_overdue_his_loan_amount_'))
        fea.update(
            self.calculate_stats(df[df.dpd_max > 0], 'inq_gap_loan_days', self.day_list, 'sisa_pinjaman_berjalan',
                                 ['max'], f'afpi_overdue_his_balance_amount_'))
        fea.update(
            self.calculate_stats(df[df.dpd_max > 0], 'inq_gap_loan_days', self.day_list, 'sisa_pinjaman_berjalan',
                                 ['count'], f'afpi_overdue_his_'))

        return fea

    def multiple_loan_features(self, df):
        fea = {}
        fea.update(
            self.calculate_stats(df, 'inq_gap_loan_days', self.day_list, 'id_penyelenggara', ['nunique'], f'afpi_ins_'))
        fea.update(
            self.calculate_stats(df[df.status_pinjaman == 'O'], 'inq_gap_loan_days', self.day_list, 'id_penyelenggara',
                                 ['nunique'], f'afpi_ins_open_'))
        fea.update(
            self.calculate_stats(df[df.status_pinjaman == 'L'], 'inq_gap_loan_days', self.day_list, 'id_penyelenggara',
                                 ['nunique'], f'afpi_ins_clear_'))
        fea.update(self.calculate_stats(df[df.dpd_max > 0], 'inq_gap_loan_days', self.day_list, 'id_penyelenggara',
                                        ['nunique'], f'afpi_ins_his_overdue_'))
        fea.update(self.calculate_stats(df[df.dpd_terakhir > 0], 'inq_gap_loan_days', self.day_list, 'id_penyelenggara',
                                        ['nunique'], f'afpi_ins_his_overdue_'))

        return fea

    def high_quality_features(self, df):
        fea = {}
        if not df.empty:
            fea.update(self.transactional_features(df))
            fea.update(self.repay_features(df))
            fea.update(self.period_features(df))
        df_dpd_0 = df[df.dpd_max <= 0]
        if not df_dpd_0.empty:
            fea.update(self.replace_dict_keys(self.transactional_features(df_dpd_0), 'afpi', 'afpi_dpd0'))
            fea.update(self.replace_dict_keys(self.repay_features(df_dpd_0), 'afpi', 'afpi_dpd0'))
            fea.update(self.replace_dict_keys(self.period_features(df_dpd_0), 'afpi', 'afpi_dpd0'))
        return fea

    def low_quality_features(self, df):
        fea = {}
        if not df.empty:
            fea.update(self.overdue_features(df))
            fea.update(self.multiple_loan_features(df))
        return fea

    def do_work(self):
        print("处理业务")

        res_fea = {}
        account_id = parseResult[0]['data']['credit_data'][0]['account_id']
        inquiry_date = parseResult[0]['data']['credit_data'][0]['data'].get('inquiryDate')
        inquiry_date = pd.to_datetime(inquiry_date)
        pinjaman = parseResult[0]['data']['credit_data'][0]['data'].get('pinjaman')
        if pinjaman:
            # Field cleaning
            pre_df_all = self.prepare_df(datas=pinjaman, inquiry_date=inquiry_date)
            # > 0.12 USD AND DROP AFDC233
            pre_df = pre_df_all[(pre_df_all.nilai_pendanaan > 2000) & (pre_df_all.id_penyelenggara != 'AFDC233')]
            # > 0.12 USD AND <= 600 USD AND DROP AFDC233
            pre_df_lte_600 = pre_df[(pre_df.nilai_pendanaan <= 10000000)]
            if not pre_df.empty:
                for t, df in {
                    '_gt2k': pre_df,
                    '': pre_df_lte_600,
                }.items():
                    if not df.empty:
                        for k, v_df in {'': df,
                                        '_top': df[df.id_penyelenggara.isin(self.top_set)],
                                        '_mid': df[df.id_penyelenggara.isin(self.mid_set)],
                                        '_low': df[~df.id_penyelenggara.isin(self.mid_set | self.top_set)]}.items():
                            res_fea.update(self.replace_dict_keys(self.high_quality_features(v_df), 'afpi', f'afpi{t}{k}'))
                            res_fea.update(self.replace_dict_keys(self.low_quality_features(v_df), 'afpi', f'afpi{t}{k}'))
                pre_df = pre_df.sort_values(by='tgl_perjanjian_borrower', ascending=False).reset_index(drop=True)
                res_fea['afpi_last_tipe_pinjaman'] = pre_df.loc[0, 'tipe_pinjaman']
                res_fea['afpi_last_sub_tipe_pinjaman'] = pre_df.loc[0, 'sub_tipe_pinjaman']
                res_fea['afpi_max_jenis_pengguna'] = pre_df.jenis_pengguna.max()
                res_fea['afpi_last_nilai_pendanaan'] = pre_df.loc[0, 'nilai_pendanaan']

                for ins_code, ins_desc in self.COMPETING_MAP.items():
                    ins_df = pre_df[pre_df.id_penyelenggara == ins_code]
                    if not ins_df.empty:
                        res_fea[f'afpi_loan_amount_max_{ins_desc}_new'] = ins_df.nilai_pendanaan.max()
                        res_fea[f'afpi_current_dpd_max_{ins_desc}_new'] = ins_df.dpd_terakhir.max()
                        res_fea[f'afpi_ever_dpd_max_{ins_desc}_new'] = ins_df.dpd_max.max()
                        res_fea[f'afpi_loan_amount_sum_{ins_desc}_new'] = ins_df.nilai_pendanaan.sum()
                        res_fea[f'afpi_loan_first_to_now_day_{ins_desc}_new'] = ins_df.inq_gap_loan_days.max()
                        res_fea[f'afpi_loan_last_to_now_day_{ins_desc}_new'] = ins_df.inq_gap_loan_days.min()
                        res_fea[f'afpi_no_overdue_on_loan_amount_sum_{ins_desc}_new'] = ins_df[ins_df.dpd_terakhir<=0].sisa_pinjaman_berjalan.sum()
                        res_fea[f'afpi_no_overdue_on_loan_amount_max_{ins_desc}_new'] = ins_df[ins_df.dpd_terakhir<=0].sisa_pinjaman_berjalan.max()
                        res_fea[f'afpi_no_overdue_loan_amount_max_{ins_desc}_new'] = ins_df[ins_df.dpd_terakhir<=0].nilai_pendanaan.max()
                        res_fea[f'afpi_loan_amount_payed_rate_{ins_desc}_new'] = round(ins_df.repay_amount.sum()/ins_df.nilai_pendanaan.sum(), 6)

                # add afpi migration feature
                # afpi_lenders_nunique_90d
                res_fea.update(self.calculate_stats(pre_df_all, 'inq_gap_loan_days', [90], 'id_penyelenggara', ['nunique'], 'afpi_lenders_'))
                # afpi_whole_overduing_num
                res_fea['afpi_whole_overduing_num_new'] = pre_df_all[(pre_df_all.status_pinjaman != 'L') & (pre_df_all.dpd_max > 0)].shape[0]
                # afpi_loan_diff_day_max
                pre_df_all = pre_df_all.sort_values(by=['inq_gap_loan_days'])
                pre_df_all['loan_diff_day'] = pre_df_all['inq_gap_loan_days'].diff()
                res_fea['afpi_loan_diff_day_max'] = pre_df_all['loan_diff_day'].max()

        last3d_inquiry = parseResult[0]['data']['credit_data'][0]['data'].get('historyInquiry', {}).get(
            'last3DaysInquiry', [])
        afpi_ctime = parseResult[0]['data']['credit_data'][0]['ctime']
        if last3d_inquiry:
            last3d_df = pd.DataFrame(last3d_inquiry)
            last3d_df['tgl_inquiry_date'] = pd.to_datetime(last3d_df.tgl_inquiry)
            last3d_df['afpi_ctime_date'] = pd.to_datetime(afpi_ctime, unit='ms')
            last3d_df['last3d_gay_day'] = (last3d_df['afpi_ctime_date'] - last3d_df['tgl_inquiry_date']).dt.days
            last1d_df = last3d_df[(last3d_df.last3d_gay_day <= 1)]
            try:
                for ins in self.last3d_ins_list:
                    res_fea[f'afpi_{ins.replace(" ", "_")}_inq_cnt_1d'] = last1d_df[last1d_df.hit_by == ins].shape[0]
                    res_fea[f'afpi_{ins.replace(" ", "_")}_inq_cnt_3d'] = last3d_df[last3d_df.hit_by == ins].shape[0]
            except:
                pass
        statistic = parseResult[0]['data']['credit_data'][0]['data'].get('historyInquiry', {}).get('statistic', {})

        for k, v in [
            ['3_hari', 3],
            ['7_hari', 7],
            ['30_hari', 30],
            ['90_hari', 90],
            ['180_hari', 180],
            ['360_hari', 360],
            ['>360_hari', 'all']
        ]:
            res_fea[f'afpi_inquiry_cnt_{v}d_new'] = statistic.get(k, 0)
        res_fea2 = {}
        for k, v in res_fea.items():
            if not pd.isna(v):
                res_fea2[k] = v

        res_fea2['timestamp'] = int(time.time() * 1000)
        res_fea2['afpi_ctime'] = afpi_ctime
        res_fea2['afpi_inquiry_status'] = parseResult[0]['data']['credit_data'][0]['data'].get('status')
        if res_fea2['afpi_inquiry_status'] == 'Found':
            res_fea2['afpi_inquiry_status_tag'] = 1
        else:
            res_fea2['afpi_inquiry_status_tag'] = 0
        result = {
            'account_id': str(account_id),
            'timestamp': int(time.time() * 1000),
            'data': res_fea2,
            '__flag': {'feature_add_tag': 1, 'redis_tag': 1, 'afpi_inquiry_status_flag': 1}
        }
        return result


def __init_env():
    global work
    work = Work()


# print(parseResult)
try:
    if not work:
        __init_env()
except NameError as e:
    __init_env()
result = work.do_work()
