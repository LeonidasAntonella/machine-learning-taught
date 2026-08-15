import json
import datetime
import time
import xmltodict
import copy
import numpy as np
import pandas as pd

NO_DATA = -9998

FEATURE_SET = {
    "cbi_consume_cur_limit_max",
    "cbi_consume_cur_limit_min",
    "cbi_consume_cur_limit_mean",
    "cbi_consume_cur_limit_sum",
    "cbi_consume_his_ins_max_limit_sum_1m",
    "cbi_consume_his_limit_max_1m",
    "cbi_consume_his_limit_min_1m",
    "cbi_consume_his_limit_mean_1m",
    "cbi_consume_his_limit_sum_1m",
    "cbi_consume_onloan_quota_rate_1m",
    "cbi_consume_his_ins_max_limit_sum_2m",
    "cbi_consume_his_limit_max_2m",
    "cbi_consume_his_limit_min_2m",
    "cbi_consume_his_limit_mean_2m",
    "cbi_consume_his_limit_sum_2m",
    "cbi_consume_onloan_quota_rate_2m",
    "cbi_consume_his_ins_max_limit_sum_3m",
    "cbi_consume_his_limit_max_3m",
    "cbi_consume_his_limit_min_3m",
    "cbi_consume_his_limit_mean_3m",
    "cbi_consume_his_limit_sum_3m",
    "cbi_consume_onloan_quota_rate_3m",
    "cbi_consume_his_ins_max_limit_sum_6m",
    "cbi_consume_his_limit_max_6m",
    "cbi_consume_his_limit_min_6m",
    "cbi_consume_his_limit_mean_6m",
    "cbi_consume_his_limit_sum_6m",
    "cbi_consume_onloan_quota_rate_6m",
    "cbi_consume_his_ins_max_limit_sum_1year",
    "cbi_consume_his_limit_max_1year",
    "cbi_consume_his_limit_min_1year",
    "cbi_consume_his_limit_mean_1year",
    "cbi_consume_his_limit_sum_1year",
    "cbi_consume_onloan_quota_rate_1year",
    "cbi_consume_his_ins_max_limit_sum_2year",
    "cbi_consume_his_limit_max_2year",
    "cbi_consume_his_limit_min_2year",
    "cbi_consume_his_limit_mean_2year",
    "cbi_consume_his_limit_sum_2year",
    "cbi_consume_onloan_quota_rate_2year",
    "cbi_consume_his_ins_max_limit_sum_3year",
    "cbi_consume_his_limit_max_3year",
    "cbi_consume_his_limit_min_3year",
    "cbi_consume_his_limit_mean_3year",
    "cbi_consume_his_limit_sum_3year",
    "cbi_consume_onloan_quota_rate_3year",
    "cbi_consume_his_ins_max_limit_sum_all",
    "cbi_consume_his_limit_max_all",
    "cbi_consume_his_limit_min_all",
    "cbi_consume_his_limit_mean_all",
    "cbi_consume_his_limit_sum_all",
    "cbi_consume_onloan_quota_rate_all",
    "cbi_consume_outstanding_max",
    "cbi_consume_outstanding_sum",
    "cbi_consume_cur_month_amount_max",
    "cbi_consume_active_transactions_num",
    "cbi_consume_close_transactions_num",
    "cbi_consume_his_transactions_num",
    "cbi_consume_active_transactions_ins_num",
    "cbi_consume_close_transactions_ins_num",
    "cbi_consume_his_transactions_ins_num",
    "cbi_consume_repayment_amount_max_1m",
    "cbi_consume_repayment_amount_sum_1m",
    "cbi_consume_repayment_ins_num_1m",
    "cbi_consume_cur_loan_outstanding_rate_max_1m",
    "cbi_consume_loan_num_1m",
    "cbi_consume_loan_amount_max_1m",
    "cbi_consume_loan_amount_sum_1m",
    "cbi_consume_loan_ins_num_1m",
    "cbi_consume_loan_num_ins_mean_1m",
    "cbi_consume_repayment_amount_max_2m",
    "cbi_consume_repayment_amount_sum_2m",
    "cbi_consume_repayment_ins_num_2m",
    "cbi_consume_cur_loan_outstanding_rate_max_2m",
    "cbi_consume_loan_num_2m",
    "cbi_consume_loan_amount_max_2m",
    "cbi_consume_loan_amount_sum_2m",
    "cbi_consume_loan_ins_num_2m",
    "cbi_consume_loan_num_ins_mean_2m",
    "cbi_consume_repayment_amount_max_3m",
    "cbi_consume_repayment_amount_sum_3m",
    "cbi_consume_repayment_ins_num_3m",
    "cbi_consume_cur_loan_outstanding_rate_max_3m",
    "cbi_consume_loan_num_3m",
    "cbi_consume_loan_amount_max_3m",
    "cbi_consume_loan_amount_sum_3m",
    "cbi_consume_loan_ins_num_3m",
    "cbi_consume_loan_num_ins_mean_3m",
    "cbi_consume_repayment_amount_max_6m",
    "cbi_consume_repayment_amount_sum_6m",
    "cbi_consume_repayment_ins_num_6m",
    "cbi_consume_cur_loan_outstanding_rate_max_6m",
    "cbi_consume_loan_num_6m",
    "cbi_consume_loan_amount_max_6m",
    "cbi_consume_loan_amount_sum_6m",
    "cbi_consume_loan_ins_num_6m",
    "cbi_consume_loan_num_ins_mean_6m",
    "cbi_consume_repayment_amount_max_12m",
    "cbi_consume_repayment_amount_sum_12m",
    "cbi_consume_repayment_ins_num_12m",
    "cbi_consume_cur_loan_outstanding_rate_max_12m",
    "cbi_consume_loan_num_12m",
    "cbi_consume_loan_amount_max_12m",
    "cbi_consume_loan_amount_sum_12m",
    "cbi_consume_loan_ins_num_12m",
    "cbi_consume_loan_num_ins_mean_12m",
    "cbi_consume_repayment_amount_max_36m",
    "cbi_consume_repayment_amount_sum_36m",
    "cbi_consume_repayment_ins_num_36m",
    "cbi_consume_cur_loan_outstanding_rate_max_36m",
    "cbi_consume_loan_num_36m",
    "cbi_consume_loan_amount_max_36m",
    "cbi_consume_loan_amount_sum_36m",
    "cbi_consume_loan_ins_num_36m",
    "cbi_consume_loan_num_ins_mean_36m",
    "cbi_consume_last_repayment_gay_months",
    "cbi_consume_last_loan_gay_months",
    "cbi_consume_loan_aging_days_max",
    "cbi_consume_loan_aging_days_min",
    "cbi_consume_overdue_cur_day_max",
    "cbi_consume_overdue_cur_day_adjust_max",
    "cbi_consume_overdue_his_day_max",
    "cbi_consume_overdue_cur_amount_max",
    "cbi_consume_overdue_his_amount_max",
    "cbi_consume_overdue_cur_amount_sum",
    "cbi_consume_overdue_cur_loan_cnt",
    "cbi_consume_overdue_cur_loan_cnt_rate",
    "cbi_consume_overdue_cur_loan_cnt_all_rate",
    "cbi_consume_overdue_his_loan_cnt",
    "cbi_consume_overdue_his_loan_cnt_rate",
    "cbi_consume_overdue_cur_ins_cnt",
    "cbi_consume_overdue_cur_ins_cnt_rate",
    "cbi_consume_overdue_cur_ins_cnt_all_rate",
    "cbi_consume_overdue_his_ins_cnt",
    "cbi_consume_overdue_his_ins_cnt_rate",
    "cbi_consume_credit_remarks_cnt",
    "cbi_consume_credit_remarks_cnt_rate",
    "cbi_consume_overdue_cur_day_max_1m",
    "cbi_consume_overdue_cur_day_adjust_max_1m",
    "cbi_consume_overdue_his_day_max_1m",
    "cbi_consume_overdue_cur_amount_max_1m",
    "cbi_consume_overdue_his_amount_max_1m",
    "cbi_consume_overdue_cur_amount_sum_1m",
    "cbi_consume_overdue_cur_loan_cnt_1m",
    "cbi_consume_overdue_cur_loan_cnt_rate_1m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_consume_overdue_his_loan_cnt_1m",
    "cbi_consume_overdue_his_loan_cnt_rate_1m",
    "cbi_consume_overdue_cur_ins_cnt_1m",
    "cbi_consume_overdue_cur_ins_cnt_rate_1m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_consume_overdue_his_ins_cnt_1m",
    "cbi_consume_overdue_his_ins_cnt_rate_1m",
    "cbi_consume_credit_remarks_cnt_1m",
    "cbi_consume_credit_remarks_cnt_rate_1m",
    "cbi_consume_overdue_cur_day_max_2m",
    "cbi_consume_overdue_cur_day_adjust_max_2m",
    "cbi_consume_overdue_his_day_max_2m",
    "cbi_consume_overdue_cur_amount_max_2m",
    "cbi_consume_overdue_his_amount_max_2m",
    "cbi_consume_overdue_cur_amount_sum_2m",
    "cbi_consume_overdue_cur_loan_cnt_2m",
    "cbi_consume_overdue_cur_loan_cnt_rate_2m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_consume_overdue_his_loan_cnt_2m",
    "cbi_consume_overdue_his_loan_cnt_rate_2m",
    "cbi_consume_overdue_cur_ins_cnt_2m",
    "cbi_consume_overdue_cur_ins_cnt_rate_2m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_consume_overdue_his_ins_cnt_2m",
    "cbi_consume_overdue_his_ins_cnt_rate_2m",
    "cbi_consume_credit_remarks_cnt_2m",
    "cbi_consume_credit_remarks_cnt_rate_2m",
    "cbi_consume_overdue_cur_day_max_3m",
    "cbi_consume_overdue_cur_day_adjust_max_3m",
    "cbi_consume_overdue_his_day_max_3m",
    "cbi_consume_overdue_cur_amount_max_3m",
    "cbi_consume_overdue_his_amount_max_3m",
    "cbi_consume_overdue_cur_amount_sum_3m",
    "cbi_consume_overdue_cur_loan_cnt_3m",
    "cbi_consume_overdue_cur_loan_cnt_rate_3m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_consume_overdue_his_loan_cnt_3m",
    "cbi_consume_overdue_his_loan_cnt_rate_3m",
    "cbi_consume_overdue_cur_ins_cnt_3m",
    "cbi_consume_overdue_cur_ins_cnt_rate_3m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_consume_overdue_his_ins_cnt_3m",
    "cbi_consume_overdue_his_ins_cnt_rate_3m",
    "cbi_consume_credit_remarks_cnt_3m",
    "cbi_consume_credit_remarks_cnt_rate_3m",
    "cbi_consume_overdue_cur_day_max_6m",
    "cbi_consume_overdue_cur_day_adjust_max_6m",
    "cbi_consume_overdue_his_day_max_6m",
    "cbi_consume_overdue_cur_amount_max_6m",
    "cbi_consume_overdue_his_amount_max_6m",
    "cbi_consume_overdue_cur_amount_sum_6m",
    "cbi_consume_overdue_cur_loan_cnt_6m",
    "cbi_consume_overdue_cur_loan_cnt_rate_6m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_consume_overdue_his_loan_cnt_6m",
    "cbi_consume_overdue_his_loan_cnt_rate_6m",
    "cbi_consume_overdue_cur_ins_cnt_6m",
    "cbi_consume_overdue_cur_ins_cnt_rate_6m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_consume_overdue_his_ins_cnt_6m",
    "cbi_consume_overdue_his_ins_cnt_rate_6m",
    "cbi_consume_credit_remarks_cnt_6m",
    "cbi_consume_credit_remarks_cnt_rate_6m",
    "cbi_consume_overdue_cur_day_max_12m",
    "cbi_consume_overdue_cur_day_adjust_max_12m",
    "cbi_consume_overdue_his_day_max_12m",
    "cbi_consume_overdue_cur_amount_max_12m",
    "cbi_consume_overdue_his_amount_max_12m",
    "cbi_consume_overdue_cur_amount_sum_12m",
    "cbi_consume_overdue_cur_loan_cnt_12m",
    "cbi_consume_overdue_cur_loan_cnt_rate_12m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_consume_overdue_his_loan_cnt_12m",
    "cbi_consume_overdue_his_loan_cnt_rate_12m",
    "cbi_consume_overdue_cur_ins_cnt_12m",
    "cbi_consume_overdue_cur_ins_cnt_rate_12m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_consume_overdue_his_ins_cnt_12m",
    "cbi_consume_overdue_his_ins_cnt_rate_12m",
    "cbi_consume_credit_remarks_cnt_12m",
    "cbi_consume_credit_remarks_cnt_rate_12m",
    "cbi_consume_overdue_cur_day_max_24m",
    "cbi_consume_overdue_cur_day_adjust_max_24m",
    "cbi_consume_overdue_his_day_max_24m",
    "cbi_consume_overdue_cur_amount_max_24m",
    "cbi_consume_overdue_his_amount_max_24m",
    "cbi_consume_overdue_cur_amount_sum_24m",
    "cbi_consume_overdue_cur_loan_cnt_24m",
    "cbi_consume_overdue_cur_loan_cnt_rate_24m",
    "cbi_consume_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_consume_overdue_his_loan_cnt_24m",
    "cbi_consume_overdue_his_loan_cnt_rate_24m",
    "cbi_consume_overdue_cur_ins_cnt_24m",
    "cbi_consume_overdue_cur_ins_cnt_rate_24m",
    "cbi_consume_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_consume_overdue_his_ins_cnt_24m",
    "cbi_consume_overdue_his_ins_cnt_rate_24m",
    "cbi_consume_credit_remarks_cnt_24m",
    "cbi_consume_credit_remarks_cnt_rate_24m",
    "cbi_credit_card_his_limit_max",
    "cbi_credit_card_his_limit_min",
    "cbi_credit_card_his_limit_mean",
    "cbi_credit_card_his_limit_sum",
    "cbi_credit_card_active_limit_max",
    "cbi_credit_card_active_limit_min",
    "cbi_credit_card_active_limit_mean",
    "cbi_credit_card_active_limit_sum",
    "cbi_credit_card_close_limit_max",
    "cbi_credit_card_close_limit_min",
    "cbi_credit_card_close_limit_mean",
    "cbi_credit_card_close_limit_sum",
    "cbi_credit_card_outstanding_max",
    "cbi_credit_card_outstanding_sum",
    "cbi_credit_card_cur_month_amount_max",
    "cbi_credit_card_active_transactions_num",
    "cbi_credit_card_close_transactions_num",
    "cbi_credit_card_his_transactions_num",
    "cbi_credit_card_active_transactions_ins_num",
    "cbi_credit_card_close_transactions_ins_num",
    "cbi_credit_card_his_transactions_ins_num",
    "cbi_credit_card_repayment_amount_max_1m",
    "cbi_credit_card_repayment_amount_sum_1m",
    "cbi_credit_card_repayment_rate_1m",
    "cbi_credit_card_repayment_ins_num_1m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_1m",
    "cbi_credit_card_loan_num_1m",
    "cbi_credit_card_loan_amount_max_1m",
    "cbi_credit_card_loan_amount_sum_1m",
    "cbi_credit_card_loan_ins_num_1m",
    "cbi_credit_card_loan_num_ins_mean_1m",
    "cbi_credit_card_repayment_amount_max_2m",
    "cbi_credit_card_repayment_amount_sum_2m",
    "cbi_credit_card_repayment_rate_2m",
    "cbi_credit_card_repayment_ins_num_2m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_2m",
    "cbi_credit_card_loan_num_2m",
    "cbi_credit_card_loan_amount_max_2m",
    "cbi_credit_card_loan_amount_sum_2m",
    "cbi_credit_card_loan_ins_num_2m",
    "cbi_credit_card_loan_num_ins_mean_2m",
    "cbi_credit_card_repayment_amount_max_3m",
    "cbi_credit_card_repayment_amount_sum_3m",
    "cbi_credit_card_repayment_rate_3m",
    "cbi_credit_card_repayment_ins_num_3m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_3m",
    "cbi_credit_card_loan_num_3m",
    "cbi_credit_card_loan_amount_max_3m",
    "cbi_credit_card_loan_amount_sum_3m",
    "cbi_credit_card_loan_ins_num_3m",
    "cbi_credit_card_loan_num_ins_mean_3m",
    "cbi_credit_card_repayment_amount_max_6m",
    "cbi_credit_card_repayment_amount_sum_6m",
    "cbi_credit_card_repayment_rate_6m",
    "cbi_credit_card_repayment_ins_num_6m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_6m",
    "cbi_credit_card_loan_num_6m",
    "cbi_credit_card_loan_amount_max_6m",
    "cbi_credit_card_loan_amount_sum_6m",
    "cbi_credit_card_loan_ins_num_6m",
    "cbi_credit_card_loan_num_ins_mean_6m",
    "cbi_credit_card_repayment_amount_max_12m",
    "cbi_credit_card_repayment_amount_sum_12m",
    "cbi_credit_card_repayment_rate_12m",
    "cbi_credit_card_repayment_ins_num_12m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_12m",
    "cbi_credit_card_loan_num_12m",
    "cbi_credit_card_loan_amount_max_12m",
    "cbi_credit_card_loan_amount_sum_12m",
    "cbi_credit_card_loan_ins_num_12m",
    "cbi_credit_card_loan_num_ins_mean_12m",
    "cbi_credit_card_repayment_amount_max_36m",
    "cbi_credit_card_repayment_amount_sum_36m",
    "cbi_credit_card_repayment_rate_36m",
    "cbi_credit_card_repayment_ins_num_36m",
    "cbi_credit_card_cur_loan_outstanding_rate_max_36m",
    "cbi_credit_card_loan_num_36m",
    "cbi_credit_card_loan_amount_max_36m",
    "cbi_credit_card_loan_amount_sum_36m",
    "cbi_credit_card_loan_ins_num_36m",
    "cbi_credit_card_loan_num_ins_mean_36m",
    "cbi_credit_card_last_repayment_gay_months",
    "cbi_credit_card_last_loan_gay_months",
    "cbi_credit_card_loan_aging_days_max",
    "cbi_credit_card_loan_aging_days_min",
    "cbi_credit_card_overdue_cur_day_max",
    "cbi_credit_card_overdue_cur_day_adjust_max",
    "cbi_credit_card_overdue_his_day_max",
    "cbi_credit_card_overdue_cur_amount_max",
    "cbi_credit_card_overdue_his_amount_max",
    "cbi_credit_card_overdue_cur_amount_sum",
    "cbi_credit_card_overdue_cur_loan_cnt",
    "cbi_credit_card_overdue_cur_loan_cnt_rate",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate",
    "cbi_credit_card_overdue_his_loan_cnt",
    "cbi_credit_card_overdue_his_loan_cnt_rate",
    "cbi_credit_card_overdue_cur_ins_cnt",
    "cbi_credit_card_overdue_cur_ins_cnt_rate",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate",
    "cbi_credit_card_overdue_his_ins_cnt",
    "cbi_credit_card_overdue_his_ins_cnt_rate",
    "cbi_credit_card_credit_remarks_cnt",
    "cbi_credit_card_credit_remarks_cnt_rate",
    "cbi_credit_card_overdue_cur_day_max_1m",
    "cbi_credit_card_overdue_cur_day_adjust_max_2m",
    "cbi_credit_card_overdue_his_day_max_1m",
    "cbi_credit_card_overdue_cur_amount_max_1m",
    "cbi_credit_card_overdue_his_amount_max_1m",
    "cbi_credit_card_overdue_cur_amount_sum_1m",
    "cbi_credit_card_overdue_cur_loan_cnt_1m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_1m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_credit_card_overdue_his_loan_cnt_1m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_1m",
    "cbi_credit_card_overdue_cur_ins_cnt_1m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_1m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_credit_card_overdue_his_ins_cnt_1m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_1m",
    "cbi_credit_card_credit_remarks_cnt_1m",
    "cbi_credit_card_credit_remarks_cnt_rate_1m",
    "cbi_credit_card_overdue_cur_day_max_2m",
    "cbi_credit_card_overdue_cur_day_adjust_max_2m",
    "cbi_credit_card_overdue_his_day_max_2m",
    "cbi_credit_card_overdue_cur_amount_max_2m",
    "cbi_credit_card_overdue_his_amount_max_2m",
    "cbi_credit_card_overdue_cur_amount_sum_2m",
    "cbi_credit_card_overdue_cur_loan_cnt_2m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_2m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_credit_card_overdue_his_loan_cnt_2m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_2m",
    "cbi_credit_card_overdue_cur_ins_cnt_2m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_2m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_credit_card_overdue_his_ins_cnt_2m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_2m",
    "cbi_credit_card_credit_remarks_cnt_2m",
    "cbi_credit_card_credit_remarks_cnt_rate_2m",
    "cbi_credit_card_overdue_cur_day_max_3m",
    "cbi_credit_card_overdue_cur_day_adjust_max_3m",
    "cbi_credit_card_overdue_his_day_max_3m",
    "cbi_credit_card_overdue_cur_amount_max_3m",
    "cbi_credit_card_overdue_his_amount_max_3m",
    "cbi_credit_card_overdue_cur_amount_sum_3m",
    "cbi_credit_card_overdue_cur_loan_cnt_3m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_3m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_credit_card_overdue_his_loan_cnt_3m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_3m",
    "cbi_credit_card_overdue_cur_ins_cnt_3m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_3m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_credit_card_overdue_his_ins_cnt_3m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_3m",
    "cbi_credit_card_credit_remarks_cnt_3m",
    "cbi_credit_card_credit_remarks_cnt_rate_3m",
    "cbi_credit_card_overdue_cur_day_max_6m",
    "cbi_credit_card_overdue_cur_day_adjust_max_6m",
    "cbi_credit_card_overdue_his_day_max_6m",
    "cbi_credit_card_overdue_cur_amount_max_6m",
    "cbi_credit_card_overdue_his_amount_max_6m",
    "cbi_credit_card_overdue_cur_amount_sum_6m",
    "cbi_credit_card_overdue_cur_loan_cnt_6m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_6m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_credit_card_overdue_his_loan_cnt_6m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_6m",
    "cbi_credit_card_overdue_cur_ins_cnt_6m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_6m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_credit_card_overdue_his_ins_cnt_6m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_6m",
    "cbi_credit_card_credit_remarks_cnt_6m",
    "cbi_credit_card_credit_remarks_cnt_rate_6m",
    "cbi_credit_card_overdue_cur_day_max_12m",
    "cbi_credit_card_overdue_cur_day_adjust_max_12m",
    "cbi_credit_card_overdue_his_day_max_12m",
    "cbi_credit_card_overdue_cur_amount_max_12m",
    "cbi_credit_card_overdue_his_amount_max_12m",
    "cbi_credit_card_overdue_cur_amount_sum_12m",
    "cbi_credit_card_overdue_cur_loan_cnt_12m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_12m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_credit_card_overdue_his_loan_cnt_12m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_12m",
    "cbi_credit_card_overdue_cur_ins_cnt_12m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_12m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_credit_card_overdue_his_ins_cnt_12m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_12m",
    "cbi_credit_card_credit_remarks_cnt_12m",
    "cbi_credit_card_credit_remarks_cnt_rate_12m",
    "cbi_credit_card_overdue_cur_day_max_24m",
    "cbi_credit_card_overdue_cur_day_adjust_max_24m",
    "cbi_credit_card_overdue_his_day_max_24m",
    "cbi_credit_card_overdue_cur_amount_max_24m",
    "cbi_credit_card_overdue_his_amount_max_24m",
    "cbi_credit_card_overdue_cur_amount_sum_24m",
    "cbi_credit_card_overdue_cur_loan_cnt_24m",
    "cbi_credit_card_overdue_cur_loan_cnt_rate_24m",
    "cbi_credit_card_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_credit_card_overdue_his_loan_cnt_24m",
    "cbi_credit_card_overdue_his_loan_cnt_rate_24m",
    "cbi_credit_card_overdue_cur_ins_cnt_24m",
    "cbi_credit_card_overdue_cur_ins_cnt_rate_24m",
    "cbi_credit_card_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_credit_card_overdue_his_ins_cnt_24m",
    "cbi_credit_card_overdue_his_ins_cnt_rate_24m",
    "cbi_credit_card_credit_remarks_cnt_24m",
    "cbi_credit_card_credit_remarks_cnt_rate_24m",
    "cbi_car_his_limit_max",
    "cbi_car_his_limit_min",
    "cbi_car_his_limit_mean",
    "cbi_car_his_limit_sum",
    "cbi_car_active_limit_max",
    "cbi_car_active_limit_min",
    "cbi_car_active_limit_mean",
    "cbi_car_active_limit_sum",
    "cbi_car_close_limit_max",
    "cbi_car_close_limit_min",
    "cbi_car_close_limit_mean",
    "cbi_car_close_limit_sum",
    "cbi_car_outstanding_max",
    "cbi_car_outstanding_sum",
    "cbi_car_active_transactions_num",
    "cbi_car_close_transactions_num",
    "cbi_car_his_transactions_num",
    "cbi_car_active_transactions_ins_num",
    "cbi_car_close_transactions_ins_num",
    "cbi_car_his_transactions_ins_num",
    "cbi_car_repayment_amount_max_1m",
    "cbi_car_repayment_amount_sum_1m",
    "cbi_car_repayment_ins_num_1m",
    "cbi_car_loan_ins_num_1m",
    "cbi_car_repayment_amount_max_2m",
    "cbi_car_repayment_amount_sum_2m",
    "cbi_car_repayment_ins_num_2m",
    "cbi_car_loan_ins_num_2m",
    "cbi_car_repayment_amount_max_3m",
    "cbi_car_repayment_amount_sum_3m",
    "cbi_car_repayment_ins_num_3m",
    "cbi_car_loan_ins_num_3m",
    "cbi_car_repayment_amount_max_6m",
    "cbi_car_repayment_amount_sum_6m",
    "cbi_car_repayment_ins_num_6m",
    "cbi_car_loan_ins_num_6m",
    "cbi_car_repayment_amount_max_12m",
    "cbi_car_repayment_amount_sum_12m",
    "cbi_car_repayment_ins_num_12m",
    "cbi_car_loan_ins_num_12m",
    "cbi_car_repayment_amount_max_36m",
    "cbi_car_repayment_amount_sum_36m",
    "cbi_car_repayment_ins_num_36m",
    "cbi_car_loan_ins_num_36m",
    "cbi_car_last_repayment_gay_months",
    "cbi_car_loan_aging_days_max",
    "cbi_car_loan_aging_days_min",
    "cbi_car_2_his_limit_max",
    "cbi_car_2_his_limit_min",
    "cbi_car_2_his_limit_mean",
    "cbi_car_2_his_limit_sum",
    "cbi_car_2_active_limit_max",
    "cbi_car_2_active_limit_min",
    "cbi_car_2_active_limit_mean",
    "cbi_car_2_active_limit_sum",
    "cbi_car_2_close_limit_max",
    "cbi_car_2_close_limit_min",
    "cbi_car_2_close_limit_mean",
    "cbi_car_2_close_limit_sum",
    "cbi_car_2_outstanding_max",
    "cbi_car_2_outstanding_sum",
    "cbi_car_2_active_transactions_num",
    "cbi_car_2_close_transactions_num",
    "cbi_car_2_his_transactions_num",
    "cbi_car_2_active_transactions_ins_num",
    "cbi_car_2_close_transactions_ins_num",
    "cbi_car_2_his_transactions_ins_num",
    "cbi_car_2_repayment_amount_max_1m",
    "cbi_car_2_repayment_amount_sum_1m",
    "cbi_car_2_repayment_ins_num_1m",
    "cbi_car_2_loan_ins_num_1m",
    "cbi_car_2_repayment_amount_max_2m",
    "cbi_car_2_repayment_amount_sum_2m",
    "cbi_car_2_repayment_ins_num_2m",
    "cbi_car_2_loan_ins_num_2m",
    "cbi_car_2_repayment_amount_max_3m",
    "cbi_car_2_repayment_amount_sum_3m",
    "cbi_car_2_repayment_ins_num_3m",
    "cbi_car_2_loan_ins_num_3m",
    "cbi_car_2_repayment_amount_max_6m",
    "cbi_car_2_repayment_amount_sum_6m",
    "cbi_car_2_repayment_ins_num_6m",
    "cbi_car_2_loan_ins_num_6m",
    "cbi_car_2_repayment_amount_max_12m",
    "cbi_car_2_repayment_amount_sum_12m",
    "cbi_car_2_repayment_ins_num_12m",
    "cbi_car_2_loan_ins_num_12m",
    "cbi_car_2_repayment_amount_max_36m",
    "cbi_car_2_repayment_amount_sum_36m",
    "cbi_car_2_repayment_ins_num_36m",
    "cbi_car_2_loan_ins_num_36m",
    "cbi_car_2_last_repayment_gay_months",
    "cbi_car_2_loan_aging_days_max",
    "cbi_car_2_loan_aging_days_min",
    "cbi_car_4_his_limit_max",
    "cbi_car_4_his_limit_min",
    "cbi_car_4_his_limit_mean",
    "cbi_car_4_his_limit_sum",
    "cbi_car_4_active_limit_max",
    "cbi_car_4_active_limit_min",
    "cbi_car_4_active_limit_mean",
    "cbi_car_4_active_limit_sum",
    "cbi_car_4_close_limit_max",
    "cbi_car_4_close_limit_min",
    "cbi_car_4_close_limit_mean",
    "cbi_car_4_close_limit_sum",
    "cbi_car_4_outstanding_max",
    "cbi_car_4_outstanding_sum",
    "cbi_car_4_active_transactions_num",
    "cbi_car_4_close_transactions_num",
    "cbi_car_4_his_transactions_num",
    "cbi_car_4_active_transactions_ins_num",
    "cbi_car_4_close_transactions_ins_num",
    "cbi_car_4_his_transactions_ins_num",
    "cbi_car_4_repayment_amount_max_1m",
    "cbi_car_4_repayment_amount_sum_1m",
    "cbi_car_4_repayment_ins_num_1m",
    "cbi_car_4_loan_ins_num_1m",
    "cbi_car_4_repayment_amount_max_2m",
    "cbi_car_4_repayment_amount_sum_2m",
    "cbi_car_4_repayment_ins_num_2m",
    "cbi_car_4_loan_ins_num_2m",
    "cbi_car_4_repayment_amount_max_3m",
    "cbi_car_4_repayment_amount_sum_3m",
    "cbi_car_4_repayment_ins_num_3m",
    "cbi_car_4_loan_ins_num_3m",
    "cbi_car_4_repayment_amount_max_6m",
    "cbi_car_4_repayment_amount_sum_6m",
    "cbi_car_4_repayment_ins_num_6m",
    "cbi_car_4_loan_ins_num_6m",
    "cbi_car_4_repayment_amount_max_12m",
    "cbi_car_4_repayment_amount_sum_12m",
    "cbi_car_4_repayment_ins_num_12m",
    "cbi_car_4_loan_ins_num_12m",
    "cbi_car_4_repayment_amount_max_36m",
    "cbi_car_4_repayment_amount_sum_36m",
    "cbi_car_4_repayment_ins_num_36m",
    "cbi_car_4_loan_ins_num_36m",
    "cbi_car_4_last_repayment_gay_months",
    "cbi_car_4_loan_aging_days_max",
    "cbi_car_4_loan_aging_days_min",
    "cbi_car_overdue_cur_day_max",
    "cbi_car_overdue_his_day_adjust_max",
    "cbi_car_overdue_his_day_max",
    "cbi_car_overdue_cur_amount_max",
    "cbi_car_overdue_his_amount_max",
    "cbi_car_overdue_cur_amount_sum",
    "cbi_car_overdue_cur_loan_cnt",
    "cbi_car_overdue_cur_loan_cnt_rate",
    "cbi_car_overdue_cur_loan_cnt_all_rate",
    "cbi_car_overdue_his_loan_cnt",
    "cbi_car_overdue_his_loan_cnt_rate",
    "cbi_car_overdue_cur_ins_cnt",
    "cbi_car_overdue_cur_ins_cnt_rate",
    "cbi_car_overdue_cur_ins_cnt_all_rate",
    "cbi_car_overdue_his_ins_cnt",
    "cbi_car_overdue_his_ins_cnt_rate",
    "cbi_car_credit_remarks_cnt",
    "cbi_car_credit_remarks_cnt_rate",
    "cbi_car_overdue_cur_day_max_1m",
    "cbi_car_overdue_cur_day_adjust_max_1m",
    "cbi_car_overdue_his_day_max_1m",
    "cbi_car_overdue_cur_amount_max_1m",
    "cbi_car_overdue_his_amount_max_1m",
    "cbi_car_overdue_cur_amount_sum_1m",
    "cbi_car_overdue_cur_loan_cnt_1m",
    "cbi_car_overdue_cur_loan_cnt_rate_1m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_car_overdue_his_loan_cnt_1m",
    "cbi_car_overdue_his_loan_cnt_rate_1m",
    "cbi_car_overdue_cur_ins_cnt_1m",
    "cbi_car_overdue_cur_ins_cnt_rate_1m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_car_overdue_his_ins_cnt_1m",
    "cbi_car_overdue_his_ins_cnt_rate_1m",
    "cbi_car_credit_remarks_cnt_1m",
    "cbi_car_credit_remarks_cnt_rate_1m",
    "cbi_car_overdue_cur_day_max_2m",
    "cbi_car_overdue_cur_day_adjust_max_3m",
    "cbi_car_overdue_his_day_max_2m",
    "cbi_car_overdue_cur_amount_max_2m",
    "cbi_car_overdue_his_amount_max_2m",
    "cbi_car_overdue_cur_amount_sum_2m",
    "cbi_car_overdue_cur_loan_cnt_2m",
    "cbi_car_overdue_cur_loan_cnt_rate_2m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_car_overdue_his_loan_cnt_2m",
    "cbi_car_overdue_his_loan_cnt_rate_2m",
    "cbi_car_overdue_cur_ins_cnt_2m",
    "cbi_car_overdue_cur_ins_cnt_rate_2m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_car_overdue_his_ins_cnt_2m",
    "cbi_car_overdue_his_ins_cnt_rate_2m",
    "cbi_car_credit_remarks_cnt_2m",
    "cbi_car_credit_remarks_cnt_rate_2m",
    "cbi_car_overdue_cur_day_max_3m",
    "cbi_car_overdue_cur_day_adjust_max_3m",
    "cbi_car_overdue_his_day_max_3m",
    "cbi_car_overdue_cur_amount_max_3m",
    "cbi_car_overdue_his_amount_max_3m",
    "cbi_car_overdue_cur_amount_sum_3m",
    "cbi_car_overdue_cur_loan_cnt_3m",
    "cbi_car_overdue_cur_loan_cnt_rate_3m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_car_overdue_his_loan_cnt_3m",
    "cbi_car_overdue_his_loan_cnt_rate_3m",
    "cbi_car_overdue_cur_ins_cnt_3m",
    "cbi_car_overdue_cur_ins_cnt_rate_3m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_car_overdue_his_ins_cnt_3m",
    "cbi_car_overdue_his_ins_cnt_rate_3m",
    "cbi_car_credit_remarks_cnt_3m",
    "cbi_car_credit_remarks_cnt_rate_3m",
    "cbi_car_overdue_cur_day_max_6m",
    "cbi_car_overdue_cur_day_adjust_max_6m",
    "cbi_car_overdue_his_day_max_6m",
    "cbi_car_overdue_cur_amount_max_6m",
    "cbi_car_overdue_his_amount_max_6m",
    "cbi_car_overdue_cur_amount_sum_6m",
    "cbi_car_overdue_cur_loan_cnt_6m",
    "cbi_car_overdue_cur_loan_cnt_rate_6m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_car_overdue_his_loan_cnt_6m",
    "cbi_car_overdue_his_loan_cnt_rate_6m",
    "cbi_car_overdue_cur_ins_cnt_6m",
    "cbi_car_overdue_cur_ins_cnt_rate_6m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_car_overdue_his_ins_cnt_6m",
    "cbi_car_overdue_his_ins_cnt_rate_6m",
    "cbi_car_credit_remarks_cnt_6m",
    "cbi_car_credit_remarks_cnt_rate_6m",
    "cbi_car_overdue_cur_day_max_12m",
    "cbi_car_overdue_cur_day_adjust_max_12m",
    "cbi_car_overdue_his_day_max_12m",
    "cbi_car_overdue_cur_amount_max_12m",
    "cbi_car_overdue_his_amount_max_12m",
    "cbi_car_overdue_cur_amount_sum_12m",
    "cbi_car_overdue_cur_loan_cnt_12m",
    "cbi_car_overdue_cur_loan_cnt_rate_12m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_car_overdue_his_loan_cnt_12m",
    "cbi_car_overdue_his_loan_cnt_rate_12m",
    "cbi_car_overdue_cur_ins_cnt_12m",
    "cbi_car_overdue_cur_ins_cnt_rate_12m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_car_overdue_his_ins_cnt_12m",
    "cbi_car_overdue_his_ins_cnt_rate_12m",
    "cbi_car_credit_remarks_cnt_12m",
    "cbi_car_credit_remarks_cnt_rate_12m",
    "cbi_car_overdue_cur_day_max_24m",
    "cbi_car_overdue_cur_day_adjust_max_24m",
    "cbi_car_overdue_his_day_max_24m",
    "cbi_car_overdue_cur_amount_max_24m",
    "cbi_car_overdue_his_amount_max_24m",
    "cbi_car_overdue_cur_amount_sum_24m",
    "cbi_car_overdue_cur_loan_cnt_24m",
    "cbi_car_overdue_cur_loan_cnt_rate_24m",
    "cbi_car_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_car_overdue_his_loan_cnt_24m",
    "cbi_car_overdue_his_loan_cnt_rate_24m",
    "cbi_car_overdue_cur_ins_cnt_24m",
    "cbi_car_overdue_cur_ins_cnt_rate_24m",
    "cbi_car_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_car_overdue_his_ins_cnt_24m",
    "cbi_car_overdue_his_ins_cnt_rate_24m",
    "cbi_car_credit_remarks_cnt_24m",
    "cbi_car_credit_remarks_cnt_rate_24m",
    "cbi_room_his_limit_max",
    "cbi_room_his_limit_min",
    "cbi_room_his_limit_mean",
    "cbi_room_his_limit_sum",
    "cbi_room_active_limit_max",
    "cbi_room_active_limit_min",
    "cbi_room_active_limit_mean",
    "cbi_room_active_limit_sum",
    "cbi_room_close_limit_max",
    "cbi_room_close_limit_min",
    "cbi_room_close_limit_mean",
    "cbi_room_close_limit_sum",
    "cbi_room_outstanding_max",
    "cbi_room_outstanding_sum",
    "cbi_room_active_transactions_num",
    "cbi_room_close_transactions_num",
    "cbi_room_his_transactions_num",
    "cbi_room_active_transactions_ins_num",
    "cbi_room_close_transactions_ins_num",
    "cbi_room_his_transactions_ins_num",
    "cbi_room_repayment_amount_max_1m",
    "cbi_room_repayment_amount_sum_1m",
    "cbi_room_repayment_ins_num_1m",
    "cbi_room_loan_ins_num_1m",
    "cbi_room_repayment_amount_max_2m",
    "cbi_room_repayment_amount_sum_2m",
    "cbi_room_repayment_ins_num_2m",
    "cbi_room_loan_ins_num_2m",
    "cbi_room_repayment_amount_max_3m",
    "cbi_room_repayment_amount_sum_3m",
    "cbi_room_repayment_ins_num_3m",
    "cbi_room_loan_ins_num_3m",
    "cbi_room_repayment_amount_max_6m",
    "cbi_room_repayment_amount_sum_6m",
    "cbi_room_repayment_ins_num_6m",
    "cbi_room_loan_ins_num_6m",
    "cbi_room_repayment_amount_max_12m",
    "cbi_room_repayment_amount_sum_12m",
    "cbi_room_repayment_ins_num_12m",
    "cbi_room_loan_ins_num_12m",
    "cbi_room_repayment_amount_max_36m",
    "cbi_room_repayment_amount_sum_36m",
    "cbi_room_repayment_ins_num_36m",
    "cbi_room_loan_ins_num_36m",
    "cbi_room_last_repayment_gay_months",
    "cbi_room_loan_aging_days_max",
    "cbi_room_loan_aging_days_min",
    "cbi_room_21_his_transactions_num",
    "cbi_room_21_70_his_transactions_num",
    "cbi_room_70_his_transactions_num",
    "cbi_room_commerce_his_transactions_num",
    "cbi_room_dwelling_his_transactions_num",
    "cbi_room_overdue_cur_day_max",
    "cbi_room_overdue_cur_day_adjust_max",
    "cbi_room_overdue_his_day_max",
    "cbi_room_overdue_cur_amount_max",
    "cbi_room_overdue_his_amount_max",
    "cbi_room_overdue_cur_amount_sum",
    "cbi_room_overdue_cur_loan_cnt",
    "cbi_room_overdue_cur_loan_cnt_rate",
    "cbi_room_overdue_cur_loan_cnt_all_rate",
    "cbi_room_overdue_his_loan_cnt",
    "cbi_room_overdue_his_loan_cnt_rate",
    "cbi_room_overdue_cur_ins_cnt",
    "cbi_room_overdue_cur_ins_cnt_rate",
    "cbi_room_overdue_cur_ins_cnt_all_rate",
    "cbi_room_overdue_his_ins_cnt",
    "cbi_room_overdue_his_ins_cnt_rate",
    "cbi_room_credit_remarks_cnt",
    "cbi_room_credit_remarks_cnt_rate",
    "cbi_room_overdue_cur_day_max_1m",
    "cbi_room_overdue_cur_day_adjust_max_1m",
    "cbi_room_overdue_his_day_max_1m",
    "cbi_room_overdue_cur_amount_max_1m",
    "cbi_room_overdue_his_amount_max_1m",
    "cbi_room_overdue_cur_amount_sum_1m",
    "cbi_room_overdue_cur_loan_cnt_1m",
    "cbi_room_overdue_cur_loan_cnt_rate_1m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_room_overdue_his_loan_cnt_1m",
    "cbi_room_overdue_his_loan_cnt_rate_1m",
    "cbi_room_overdue_cur_ins_cnt_1m",
    "cbi_room_overdue_cur_ins_cnt_rate_1m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_room_overdue_his_ins_cnt_1m",
    "cbi_room_overdue_his_ins_cnt_rate_1m",
    "cbi_room_credit_remarks_cnt_1m",
    "cbi_room_credit_remarks_cnt_rate_1m",
    "cbi_room_overdue_cur_day_max_2m",
    "cbi_room_overdue_cur_day_adjust_max_2m",
    "cbi_room_overdue_his_day_max_2m",
    "cbi_room_overdue_cur_amount_max_2m",
    "cbi_room_overdue_his_amount_max_2m",
    "cbi_room_overdue_cur_amount_sum_2m",
    "cbi_room_overdue_cur_loan_cnt_2m",
    "cbi_room_overdue_cur_loan_cnt_rate_2m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_room_overdue_his_loan_cnt_2m",
    "cbi_room_overdue_his_loan_cnt_rate_2m",
    "cbi_room_overdue_cur_ins_cnt_2m",
    "cbi_room_overdue_cur_ins_cnt_rate_2m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_room_overdue_his_ins_cnt_2m",
    "cbi_room_overdue_his_ins_cnt_rate_2m",
    "cbi_room_credit_remarks_cnt_2m",
    "cbi_room_credit_remarks_cnt_rate_2m",
    "cbi_room_overdue_cur_day_max_3m",
    "cbi_room_overdue_cur_day_adjust_max_3m",
    "cbi_room_overdue_his_day_max_3m",
    "cbi_room_overdue_cur_amount_max_3m",
    "cbi_room_overdue_his_amount_max_3m",
    "cbi_room_overdue_cur_amount_sum_3m",
    "cbi_room_overdue_cur_loan_cnt_3m",
    "cbi_room_overdue_cur_loan_cnt_rate_3m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_room_overdue_his_loan_cnt_3m",
    "cbi_room_overdue_his_loan_cnt_rate_3m",
    "cbi_room_overdue_cur_ins_cnt_3m",
    "cbi_room_overdue_cur_ins_cnt_rate_3m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_room_overdue_his_ins_cnt_3m",
    "cbi_room_overdue_his_ins_cnt_rate_3m",
    "cbi_room_credit_remarks_cnt_3m",
    "cbi_room_credit_remarks_cnt_rate_3m",
    "cbi_room_overdue_cur_day_max_6m",
    "cbi_room_overdue_cur_day_adjust_max_6m",
    "cbi_room_overdue_his_day_max_6m",
    "cbi_room_overdue_cur_amount_max_6m",
    "cbi_room_overdue_his_amount_max_6m",
    "cbi_room_overdue_cur_amount_sum_6m",
    "cbi_room_overdue_cur_loan_cnt_6m",
    "cbi_room_overdue_cur_loan_cnt_rate_6m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_room_overdue_his_loan_cnt_6m",
    "cbi_room_overdue_his_loan_cnt_rate_6m",
    "cbi_room_overdue_cur_ins_cnt_6m",
    "cbi_room_overdue_cur_ins_cnt_rate_6m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_room_overdue_his_ins_cnt_6m",
    "cbi_room_overdue_his_ins_cnt_rate_6m",
    "cbi_room_credit_remarks_cnt_6m",
    "cbi_room_credit_remarks_cnt_rate_6m",
    "cbi_room_overdue_cur_day_max_12m",
    "cbi_room_overdue_cur_day_adjust_max_12m",
    "cbi_room_overdue_his_day_max_12m",
    "cbi_room_overdue_cur_amount_max_12m",
    "cbi_room_overdue_his_amount_max_12m",
    "cbi_room_overdue_cur_amount_sum_12m",
    "cbi_room_overdue_cur_loan_cnt_12m",
    "cbi_room_overdue_cur_loan_cnt_rate_12m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_room_overdue_his_loan_cnt_12m",
    "cbi_room_overdue_his_loan_cnt_rate_12m",
    "cbi_room_overdue_cur_ins_cnt_12m",
    "cbi_room_overdue_cur_ins_cnt_rate_12m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_room_overdue_his_ins_cnt_12m",
    "cbi_room_overdue_his_ins_cnt_rate_12m",
    "cbi_room_credit_remarks_cnt_12m",
    "cbi_room_credit_remarks_cnt_rate_12m",
    "cbi_room_overdue_cur_day_max_24m",
    "cbi_room_overdue_cur_day_adjust_max_24m",
    "cbi_room_overdue_his_day_max_24m",
    "cbi_room_overdue_cur_amount_max_24m",
    "cbi_room_overdue_his_amount_max_24m",
    "cbi_room_overdue_cur_amount_sum_24m",
    "cbi_room_overdue_cur_loan_cnt_24m",
    "cbi_room_overdue_cur_loan_cnt_rate_24m",
    "cbi_room_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_room_overdue_his_loan_cnt_24m",
    "cbi_room_overdue_his_loan_cnt_rate_24m",
    "cbi_room_overdue_cur_ins_cnt_24m",
    "cbi_room_overdue_cur_ins_cnt_rate_24m",
    "cbi_room_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_room_overdue_his_ins_cnt_24m",
    "cbi_room_overdue_his_ins_cnt_rate_24m",
    "cbi_room_credit_remarks_cnt_24m",
    "cbi_room_credit_remarks_cnt_rate_24m",
    "cbi_enterprises_loan_num",
    "cbi_enterprises_limit_max",
    "cbi_enterprises_limit_sum",
    "cbi_enterprises_ins_num",
    "cbi_enterprises_mikro_loan_num",
    "cbi_enterprises_mikro_limit_max",
    "cbi_enterprises_mikro_limit_sum",
    "cbi_enterprises_mikro_ins_num",
    "cbi_enterprises_small_loan_num",
    "cbi_enterprises_small_limit_max",
    "cbi_enterprises_small_limit_sum",
    "cbi_enterprises_small_ins_num",
    "cbi_enterprises_medium_loan_num",
    "cbi_enterprises_medium_limit_max",
    "cbi_enterprises_medium_limit_sum",
    "cbi_enterprises_medium_ins_num",
    "cbi_enterprises_overdue_cur_day_max",
    "cbi_enterprises_overdue_cur_day_adjust_max",
    "cbi_enterprises_overdue_his_day_max",
    "cbi_enterprises_overdue_cur_amount_max",
    "cbi_enterprises_overdue_his_amount_max",
    "cbi_enterprises_overdue_cur_amount_sum",
    "cbi_enterprises_overdue_cur_loan_cnt",
    "cbi_enterprises_overdue_cur_loan_cnt_rate",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate",
    "cbi_enterprises_overdue_his_loan_cnt",
    "cbi_enterprises_overdue_his_loan_cnt_rate",
    "cbi_enterprises_overdue_cur_ins_cnt",
    "cbi_enterprises_overdue_cur_ins_cnt_rate",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate",
    "cbi_enterprises_overdue_his_ins_cnt",
    "cbi_enterprises_overdue_his_ins_cnt_rate",
    "cbi_enterprises_credit_remarks_cnt",
    "cbi_enterprises_credit_remarks_cnt_rate",
    "cbi_enterprises_overdue_cur_day_max_1m",
    "cbi_enterprises_overdue_cur_day_adjust_max_1m",
    "cbi_enterprises_overdue_his_day_max_1m",
    "cbi_enterprises_overdue_cur_amount_max_1m",
    "cbi_enterprises_overdue_his_amount_max_1m",
    "cbi_enterprises_overdue_cur_amount_sum_1m",
    "cbi_enterprises_overdue_cur_loan_cnt_1m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_1m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_enterprises_overdue_his_loan_cnt_1m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_1m",
    "cbi_enterprises_overdue_cur_ins_cnt_1m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_1m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_enterprises_overdue_his_ins_cnt_1m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_1m",
    "cbi_enterprises_credit_remarks_cnt_1m",
    "cbi_enterprises_credit_remarks_cnt_rate_1m",
    "cbi_enterprises_overdue_cur_day_max_2m",
    "cbi_enterprises_overdue_cur_day_adjust_max_2m",
    "cbi_enterprises_overdue_his_day_max_2m",
    "cbi_enterprises_overdue_cur_amount_max_2m",
    "cbi_enterprises_overdue_his_amount_max_2m",
    "cbi_enterprises_overdue_cur_amount_sum_2m",
    "cbi_enterprises_overdue_cur_loan_cnt_2m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_2m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_enterprises_overdue_his_loan_cnt_2m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_2m",
    "cbi_enterprises_overdue_cur_ins_cnt_2m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_2m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_enterprises_overdue_his_ins_cnt_2m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_2m",
    "cbi_enterprises_credit_remarks_cnt_2m",
    "cbi_enterprises_credit_remarks_cnt_rate_2m",
    "cbi_enterprises_overdue_cur_day_max_3m",
    "cbi_enterprises_overdue_cur_day_adjust_max_3m",
    "cbi_enterprises_overdue_his_day_max_3m",
    "cbi_enterprises_overdue_cur_amount_max_3m",
    "cbi_enterprises_overdue_his_amount_max_3m",
    "cbi_enterprises_overdue_cur_amount_sum_3m",
    "cbi_enterprises_overdue_cur_loan_cnt_3m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_3m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_enterprises_overdue_his_loan_cnt_3m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_3m",
    "cbi_enterprises_overdue_cur_ins_cnt_3m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_3m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_enterprises_overdue_his_ins_cnt_3m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_3m",
    "cbi_enterprises_credit_remarks_cnt_3m",
    "cbi_enterprises_credit_remarks_cnt_rate_3m",
    "cbi_enterprises_overdue_cur_day_max_6m",
    "cbi_enterprises_overdue_cur_day_adjust_max_6m",
    "cbi_enterprises_overdue_his_day_max_6m",
    "cbi_enterprises_overdue_cur_amount_max_6m",
    "cbi_enterprises_overdue_his_amount_max_6m",
    "cbi_enterprises_overdue_cur_amount_sum_6m",
    "cbi_enterprises_overdue_cur_loan_cnt_6m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_6m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_enterprises_overdue_his_loan_cnt_6m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_6m",
    "cbi_enterprises_overdue_cur_ins_cnt_6m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_6m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_enterprises_overdue_his_ins_cnt_6m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_6m",
    "cbi_enterprises_credit_remarks_cnt_6m",
    "cbi_enterprises_credit_remarks_cnt_rate_6m",
    "cbi_enterprises_overdue_cur_day_max_12m",
    "cbi_enterprises_overdue_cur_day_adjust_max_12m",
    "cbi_enterprises_overdue_his_day_max_12m",
    "cbi_enterprises_overdue_cur_amount_max_12m",
    "cbi_enterprises_overdue_his_amount_max_12m",
    "cbi_enterprises_overdue_cur_amount_sum_12m",
    "cbi_enterprises_overdue_cur_loan_cnt_12m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_12m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_enterprises_overdue_his_loan_cnt_12m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_12m",
    "cbi_enterprises_overdue_cur_ins_cnt_12m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_12m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_enterprises_overdue_his_ins_cnt_12m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_12m",
    "cbi_enterprises_credit_remarks_cnt_12m",
    "cbi_enterprises_credit_remarks_cnt_rate_12m",
    "cbi_enterprises_overdue_cur_day_max_24m",
    "cbi_enterprises_overdue_cur_day_adjust_max_24m",
    "cbi_enterprises_overdue_his_day_max_24m",
    "cbi_enterprises_overdue_cur_amount_max_24m",
    "cbi_enterprises_overdue_his_amount_max_24m",
    "cbi_enterprises_overdue_cur_amount_sum_24m",
    "cbi_enterprises_overdue_cur_loan_cnt_24m",
    "cbi_enterprises_overdue_cur_loan_cnt_rate_24m",
    "cbi_enterprises_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_enterprises_overdue_his_loan_cnt_24m",
    "cbi_enterprises_overdue_his_loan_cnt_rate_24m",
    "cbi_enterprises_overdue_cur_ins_cnt_24m",
    "cbi_enterprises_overdue_cur_ins_cnt_rate_24m",
    "cbi_enterprises_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_enterprises_overdue_his_ins_cnt_24m",
    "cbi_enterprises_overdue_his_ins_cnt_rate_24m",
    "cbi_enterprises_credit_remarks_cnt_24m",
    "cbi_enterprises_credit_remarks_cnt_rate_24m",
    "cbi_collateral_loan_num",
    "cbi_collateral_limit_max",
    "cbi_collateral_limit_sum",
    "cbi_collateral_ins_num",
    "cbi_collateral_room_loan_num",
    "cbi_collateral_room_limit_max",
    "cbi_collateral_room_limit_sum",
    "cbi_collateral_room_ins_num",
    "cbi_collateral_car_loan_num",
    "cbi_collateral_car_limit_max",
    "cbi_collateral_car_limit_sum",
    "cbi_collateral_car_ins_num",
    "cbi_collateral_sukuk_loan_num",
    "cbi_collateral_sukuk_limit_max",
    "cbi_collateral_sukuk_limit_sum",
    "cbi_collateral_sukuk_ins_num",
    "cbi_collateral_other_loan_num",
    "cbi_collateral_other_limit_max",
    "cbi_collateral_other_limit_sum",
    "cbi_collateral_other_ins_num",
    "cbi_overdue_cur_day_max",
    "cbi_overdue_cur_day_adjust_max",
    "cbi_overdue_his_day_max",
    "cbi_overdue_cur_amount_max",
    "cbi_overdue_his_amount_max",
    "cbi_overdue_cur_amount_sum",
    "cbi_overdue_cur_loan_cnt",
    "cbi_overdue_cur_loan_cnt_rate",
    "cbi_overdue_cur_loan_cnt_all_rate",
    "cbi_overdue_his_loan_cnt",
    "cbi_overdue_his_loan_cnt_rate",
    "cbi_overdue_cur_ins_cnt",
    "cbi_overdue_cur_ins_cnt_rate",
    "cbi_overdue_cur_ins_cnt_all_rate",
    "cbi_overdue_his_ins_cnt",
    "cbi_overdue_his_ins_cnt_rate",
    "cbi_credit_remarks_cnt",
    "cbi_credit_remarks_cnt_rate",
    "cbi_overdue_cur_day_max_1m",
    "cbi_overdue_cur_day_adjust_max_1m",
    "cbi_overdue_his_day_max_1m",
    "cbi_overdue_cur_amount_max_1m",
    "cbi_overdue_his_amount_max_1m",
    "cbi_overdue_cur_amount_sum_1m",
    "cbi_overdue_cur_loan_cnt_1m",
    "cbi_overdue_cur_loan_cnt_rate_1m",
    "cbi_overdue_cur_loan_cnt_all_rate_1m",
    "cbi_overdue_his_loan_cnt_1m",
    "cbi_overdue_his_loan_cnt_rate_1m",
    "cbi_overdue_cur_ins_cnt_1m",
    "cbi_overdue_cur_ins_cnt_rate_1m",
    "cbi_overdue_cur_ins_cnt_all_rate_1m",
    "cbi_overdue_his_ins_cnt_1m",
    "cbi_overdue_his_ins_cnt_rate_1m",
    "cbi_credit_remarks_cnt_1m",
    "cbi_credit_remarks_cnt_rate_1m",
    "cbi_overdue_cur_day_max_2m",
    "cbi_overdue_cur_day_adjust_max_2m",
    "cbi_overdue_his_day_max_2m",
    "cbi_overdue_cur_amount_max_2m",
    "cbi_overdue_his_amount_max_2m",
    "cbi_overdue_cur_amount_sum_2m",
    "cbi_overdue_cur_loan_cnt_2m",
    "cbi_overdue_cur_loan_cnt_rate_2m",
    "cbi_overdue_cur_loan_cnt_all_rate_2m",
    "cbi_overdue_his_loan_cnt_2m",
    "cbi_overdue_his_loan_cnt_rate_2m",
    "cbi_overdue_cur_ins_cnt_2m",
    "cbi_overdue_cur_ins_cnt_rate_2m",
    "cbi_overdue_cur_ins_cnt_all_rate_2m",
    "cbi_overdue_his_ins_cnt_2m",
    "cbi_overdue_his_ins_cnt_rate_2m",
    "cbi_credit_remarks_cnt_2m",
    "cbi_credit_remarks_cnt_rate_2m",
    "cbi_overdue_cur_day_max_3m",
    "cbi_overdue_cur_day_adjust_max_3m",
    "cbi_overdue_his_day_max_3m",
    "cbi_overdue_cur_amount_max_3m",
    "cbi_overdue_his_amount_max_3m",
    "cbi_overdue_cur_amount_sum_3m",
    "cbi_overdue_cur_loan_cnt_3m",
    "cbi_overdue_cur_loan_cnt_rate_3m",
    "cbi_overdue_cur_loan_cnt_all_rate_3m",
    "cbi_overdue_his_loan_cnt_3m",
    "cbi_overdue_his_loan_cnt_rate_3m",
    "cbi_overdue_cur_ins_cnt_3m",
    "cbi_overdue_cur_ins_cnt_rate_3m",
    "cbi_overdue_cur_ins_cnt_all_rate_3m",
    "cbi_overdue_his_ins_cnt_3m",
    "cbi_overdue_his_ins_cnt_rate_3m",
    "cbi_credit_remarks_cnt_3m",
    "cbi_credit_remarks_cnt_rate_3m",
    "cbi_overdue_cur_day_max_6m",
    "cbi_overdue_cur_day_adjust_max_6m",
    "cbi_overdue_his_day_max_6m",
    "cbi_overdue_cur_amount_max_6m",
    "cbi_overdue_his_amount_max_6m",
    "cbi_overdue_cur_amount_sum_6m",
    "cbi_overdue_cur_loan_cnt_6m",
    "cbi_overdue_cur_loan_cnt_rate_6m",
    "cbi_overdue_cur_loan_cnt_all_rate_6m",
    "cbi_overdue_his_loan_cnt_6m",
    "cbi_overdue_his_loan_cnt_rate_6m",
    "cbi_overdue_cur_ins_cnt_6m",
    "cbi_overdue_cur_ins_cnt_rate_6m",
    "cbi_overdue_cur_ins_cnt_all_rate_6m",
    "cbi_overdue_his_ins_cnt_6m",
    "cbi_overdue_his_ins_cnt_rate_6m",
    "cbi_credit_remarks_cnt_6m",
    "cbi_credit_remarks_cnt_rate_6m",
    "cbi_overdue_cur_day_max_12m",
    "cbi_overdue_cur_day_adjust_max_12m",
    "cbi_overdue_his_day_max_12m",
    "cbi_overdue_cur_amount_max_12m",
    "cbi_overdue_his_amount_max_12m",
    "cbi_overdue_cur_amount_sum_12m",
    "cbi_overdue_cur_loan_cnt_12m",
    "cbi_overdue_cur_loan_cnt_rate_12m",
    "cbi_overdue_cur_loan_cnt_all_rate_12m",
    "cbi_overdue_his_loan_cnt_12m",
    "cbi_overdue_his_loan_cnt_rate_12m",
    "cbi_overdue_cur_ins_cnt_12m",
    "cbi_overdue_cur_ins_cnt_rate_12m",
    "cbi_overdue_cur_ins_cnt_all_rate_12m",
    "cbi_overdue_his_ins_cnt_12m",
    "cbi_overdue_his_ins_cnt_rate_12m",
    "cbi_credit_remarks_cnt_12m",
    "cbi_credit_remarks_cnt_rate_12m",
    "cbi_overdue_cur_day_max_24m",
    "cbi_overdue_cur_day_adjust_max_24m",
    "cbi_overdue_his_day_max_24m",
    "cbi_overdue_cur_amount_max_24m",
    "cbi_overdue_his_amount_max_24m",
    "cbi_overdue_cur_amount_sum_24m",
    "cbi_overdue_cur_loan_cnt_24m",
    "cbi_overdue_cur_loan_cnt_rate_24m",
    "cbi_overdue_cur_loan_cnt_all_rate_24m",
    "cbi_overdue_his_loan_cnt_24m",
    "cbi_overdue_his_loan_cnt_rate_24m",
    "cbi_overdue_cur_ins_cnt_24m",
    "cbi_overdue_cur_ins_cnt_rate_24m",
    "cbi_overdue_cur_ins_cnt_all_rate_24m",
    "cbi_overdue_his_ins_cnt_24m",
    "cbi_overdue_his_ins_cnt_rate_24m",
    "cbi_credit_remarks_cnt_24m",
    "cbi_credit_remarks_cnt_rate_24m",
    "cbi_inq_cnt_sum_1m",
    "cbi_inq_ins_cnt_max_1m",
    "cbi_inq_cnt_sum_2m",
    "cbi_inq_ins_cnt_max_2m",
    "cbi_inq_cnt_sum_3m",
    "cbi_inq_ins_cnt_max_3m",
    "cbi_inq_cnt_sum_6m",
    "cbi_inq_ins_cnt_max_6m",
    "cbi_inq_cnt_sum_12m",
    "cbi_inq_ins_cnt_max_12m",
    "cbi_gender",
    "cbi_birth",
    "cbi_age",
    "cbi_marital_status",
    "cbi_education",
    "cbi_cur_phone_number",
    "cbi_cur_cellular_number",
    "cbi_cur_email",
    "cbi_employment",
    "cbi_employment_desc",
    "cbi_his_phone_number_list",
    "cbi_his_cellular_number_list",
    "cbi_his_email_list",
    "cbi_enterprises_v2_active_ins_num_12m",
    "cbi_enterprises_v2_active_ins_num_24m",
    "cbi_enterprises_v2_active_ins_num_6m",
    "cbi_enterprises_v2_active_limit_max_12m",
    "cbi_enterprises_v2_active_limit_max_24m",
    "cbi_enterprises_v2_active_limit_max_6m",
    "cbi_enterprises_v2_active_limit_sum_12m",
    "cbi_enterprises_v2_active_limit_sum_24m",
    "cbi_enterprises_v2_active_limit_sum_6m",
    "cbi_enterprises_v2_active_loan_num_12m",
    "cbi_enterprises_v2_active_loan_num_24m",
    "cbi_enterprises_v2_active_loan_num_6m",
    "cbi_enterprises_v2_active_medium_ins_num_12m",
    "cbi_enterprises_v2_active_medium_ins_num_24m",
    "cbi_enterprises_v2_active_medium_ins_num_6m",
    "cbi_enterprises_v2_active_medium_limit_max_12m",
    "cbi_enterprises_v2_active_medium_limit_max_24m",
    "cbi_enterprises_v2_active_medium_limit_max_6m",
    "cbi_enterprises_v2_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_active_medium_loan_num_12m",
    "cbi_enterprises_v2_active_medium_loan_num_24m",
    "cbi_enterprises_v2_active_medium_loan_num_6m",
    "cbi_enterprises_v2_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_active_small_ins_num_12m",
    "cbi_enterprises_v2_active_small_ins_num_24m",
    "cbi_enterprises_v2_active_small_ins_num_6m",
    "cbi_enterprises_v2_active_small_limit_max_12m",
    "cbi_enterprises_v2_active_small_limit_max_24m",
    "cbi_enterprises_v2_active_small_limit_max_6m",
    "cbi_enterprises_v2_active_small_limit_sum_12m",
    "cbi_enterprises_v2_active_small_limit_sum_24m",
    "cbi_enterprises_v2_active_small_limit_sum_6m",
    "cbi_enterprises_v2_active_small_loan_num_12m",
    "cbi_enterprises_v2_active_small_loan_num_24m",
    "cbi_enterprises_v2_active_small_loan_num_6m",
    "cbi_enterprises_v2_non_active_ins_num_12m",
    "cbi_enterprises_v2_non_active_ins_num_24m",
    "cbi_enterprises_v2_non_active_ins_num_6m",
    "cbi_enterprises_v2_non_active_limit_max_12m",
    "cbi_enterprises_v2_non_active_limit_max_24m",
    "cbi_enterprises_v2_non_active_limit_max_6m",
    "cbi_enterprises_v2_non_active_limit_sum_12m",
    "cbi_enterprises_v2_non_active_limit_sum_24m",
    "cbi_enterprises_v2_non_active_limit_sum_6m",
    "cbi_enterprises_v2_non_active_loan_num_12m",
    "cbi_enterprises_v2_non_active_loan_num_24m",
    "cbi_enterprises_v2_non_active_loan_num_6m",
    "cbi_enterprises_v2_non_active_medium_ins_num_12m",
    "cbi_enterprises_v2_non_active_medium_ins_num_24m",
    "cbi_enterprises_v2_non_active_medium_ins_num_6m",
    "cbi_enterprises_v2_non_active_medium_limit_max_12m",
    "cbi_enterprises_v2_non_active_medium_limit_max_24m",
    "cbi_enterprises_v2_non_active_medium_limit_max_6m",
    "cbi_enterprises_v2_non_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_non_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_non_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_non_active_medium_loan_num_12m",
    "cbi_enterprises_v2_non_active_medium_loan_num_24m",
    "cbi_enterprises_v2_non_active_medium_loan_num_6m",
    "cbi_enterprises_v2_non_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_non_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_non_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_non_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_non_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_non_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_non_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_non_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_non_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_non_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_non_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_non_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_non_active_small_ins_num_12m",
    "cbi_enterprises_v2_non_active_small_ins_num_24m",
    "cbi_enterprises_v2_non_active_small_ins_num_6m",
    "cbi_enterprises_v2_non_active_small_limit_max_12m",
    "cbi_enterprises_v2_non_active_small_limit_max_24m",
    "cbi_enterprises_v2_non_active_small_limit_max_6m",
    "cbi_enterprises_v2_non_active_small_limit_sum_12m",
    "cbi_enterprises_v2_non_active_small_limit_sum_24m",
    "cbi_enterprises_v2_non_active_small_limit_sum_6m",
    "cbi_enterprises_v2_non_active_small_loan_num_12m",
    "cbi_enterprises_v2_non_active_small_loan_num_24m",
    "cbi_enterprises_v2_non_active_small_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_active_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_active_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_active_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_active_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_active_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_active_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_medium_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_medium_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_medium_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_active_medium_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_medium_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_medium_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_small_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_small_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_small_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_active_small_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_active_small_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_active_small_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_active_small_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_medium_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_non_active_small_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_medium_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_medium_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_medium_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_medium_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_medium_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_medium_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_medium_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_mikro_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_mikro_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_mikro_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_mikro_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_mikro_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_mikro_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_mikro_loan_num_6m",
    "cbi_enterprises_v2_conventional_finance_small_ins_num_12m",
    "cbi_enterprises_v2_conventional_finance_small_ins_num_24m",
    "cbi_enterprises_v2_conventional_finance_small_ins_num_6m",
    "cbi_enterprises_v2_conventional_finance_small_limit_max_12m",
    "cbi_enterprises_v2_conventional_finance_small_limit_max_24m",
    "cbi_enterprises_v2_conventional_finance_small_limit_max_6m",
    "cbi_enterprises_v2_conventional_finance_small_limit_sum_12m",
    "cbi_enterprises_v2_conventional_finance_small_limit_sum_24m",
    "cbi_enterprises_v2_conventional_finance_small_limit_sum_6m",
    "cbi_enterprises_v2_conventional_finance_small_loan_num_12m",
    "cbi_enterprises_v2_conventional_finance_small_loan_num_24m",
    "cbi_enterprises_v2_conventional_finance_small_loan_num_6m",
    "cbi_enterprises_v2_ins_num_12m",
    "cbi_enterprises_v2_ins_num_24m",
    "cbi_enterprises_v2_ins_num_6m",
    "cbi_enterprises_v2_limit_max_12m",
    "cbi_enterprises_v2_limit_max_24m",
    "cbi_enterprises_v2_limit_max_6m",
    "cbi_enterprises_v2_limit_sum_12m",
    "cbi_enterprises_v2_limit_sum_24m",
    "cbi_enterprises_v2_limit_sum_6m",
    "cbi_enterprises_v2_loan_num_12m",
    "cbi_enterprises_v2_loan_num_24m",
    "cbi_enterprises_v2_loan_num_6m",
    "cbi_enterprises_v2_medium_ins_num_12m",
    "cbi_enterprises_v2_medium_ins_num_24m",
    "cbi_enterprises_v2_medium_ins_num_6m",
    "cbi_enterprises_v2_medium_limit_max_12m",
    "cbi_enterprises_v2_medium_limit_max_24m",
    "cbi_enterprises_v2_medium_limit_max_6m",
    "cbi_enterprises_v2_medium_limit_sum_12m",
    "cbi_enterprises_v2_medium_limit_sum_24m",
    "cbi_enterprises_v2_medium_limit_sum_6m",
    "cbi_enterprises_v2_medium_loan_num_12m",
    "cbi_enterprises_v2_medium_loan_num_24m",
    "cbi_enterprises_v2_medium_loan_num_6m",
    "cbi_enterprises_v2_mikro_ins_num_12m",
    "cbi_enterprises_v2_mikro_ins_num_24m",
    "cbi_enterprises_v2_mikro_ins_num_6m",
    "cbi_enterprises_v2_mikro_limit_max_12m",
    "cbi_enterprises_v2_mikro_limit_max_24m",
    "cbi_enterprises_v2_mikro_limit_max_6m",
    "cbi_enterprises_v2_mikro_limit_sum_12m",
    "cbi_enterprises_v2_mikro_limit_sum_24m",
    "cbi_enterprises_v2_mikro_limit_sum_6m",
    "cbi_enterprises_v2_mikro_loan_num_12m",
    "cbi_enterprises_v2_mikro_loan_num_24m",
    "cbi_enterprises_v2_mikro_loan_num_6m",
    "cbi_enterprises_v2_small_ins_num_12m",
    "cbi_enterprises_v2_small_ins_num_24m",
    "cbi_enterprises_v2_small_ins_num_6m",
    "cbi_enterprises_v2_small_limit_max_12m",
    "cbi_enterprises_v2_small_limit_max_24m",
    "cbi_enterprises_v2_small_limit_max_6m",
    "cbi_enterprises_v2_small_limit_sum_12m",
    "cbi_enterprises_v2_small_limit_sum_24m",
    "cbi_enterprises_v2_small_limit_sum_6m",
    "cbi_enterprises_v2_small_loan_num_12m",
    "cbi_enterprises_v2_small_loan_num_24m",
    "cbi_enterprises_v2_small_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_active_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_active_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_active_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_active_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_active_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_active_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_medium_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_medium_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_medium_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_active_medium_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_medium_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_medium_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_small_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_small_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_small_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_active_small_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_active_small_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_active_small_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_active_small_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_medium_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_mikro_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_non_active_small_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_medium_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_medium_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_medium_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_medium_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_medium_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_medium_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_medium_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_mikro_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_mikro_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_mikro_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_mikro_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_mikro_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_mikro_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_mikro_loan_num_6m",
    "cbi_enterprises_v2_syariah_finance_small_ins_num_12m",
    "cbi_enterprises_v2_syariah_finance_small_ins_num_24m",
    "cbi_enterprises_v2_syariah_finance_small_ins_num_6m",
    "cbi_enterprises_v2_syariah_finance_small_limit_max_12m",
    "cbi_enterprises_v2_syariah_finance_small_limit_max_24m",
    "cbi_enterprises_v2_syariah_finance_small_limit_max_6m",
    "cbi_enterprises_v2_syariah_finance_small_limit_sum_12m",
    "cbi_enterprises_v2_syariah_finance_small_limit_sum_24m",
    "cbi_enterprises_v2_syariah_finance_small_limit_sum_6m",
    "cbi_enterprises_v2_syariah_finance_small_loan_num_12m",
    "cbi_enterprises_v2_syariah_finance_small_loan_num_24m",
    "cbi_enterprises_v2_syariah_finance_small_loan_num_6m",
    "cbi_inq_cnt_skewness_6m",
    "cbi_inq_cnt_kurtosis_6m",
    "cbi_inq_ins_cnt_skewness_6m",
    "cbi_inq_ins_cnt_kurtosis_6m",
    "cbi_inq_cnt_skewness_12m",
    "cbi_inq_cnt_kurtosis_12m",
    "cbi_inq_ins_cnt_skewness_12m",
    "cbi_inq_ins_cnt_kurtosis_12m",
    "cbi_consume_outstanding_mean",
    "cbi_consume_cur_month_amount_mean",
    "cbi_consume_outstanding_max_1m",
    "cbi_consume_outstanding_sum_1m",
    "cbi_consume_outstanding_mean_1m",
    "cbi_consume_cur_month_amount_max_1m",
    "cbi_consume_cur_month_amount_mean_1m",
    "cbi_consume_outstanding_max_2m",
    "cbi_consume_outstanding_sum_2m",
    "cbi_consume_outstanding_mean_2m",
    "cbi_consume_cur_month_amount_max_2m",
    "cbi_consume_cur_month_amount_mean_2m",
    "cbi_consume_outstanding_max_3m",
    "cbi_consume_outstanding_sum_3m",
    "cbi_consume_outstanding_mean_3m",
    "cbi_consume_cur_month_amount_max_3m",
    "cbi_consume_cur_month_amount_mean_3m",
    "cbi_consume_outstanding_max_6m",
    "cbi_consume_outstanding_sum_6m",
    "cbi_consume_outstanding_mean_6m",
    "cbi_consume_cur_month_amount_max_6m",
    "cbi_consume_cur_month_amount_mean_6m",
    "cbi_consume_outstanding_max_12m",
    "cbi_consume_outstanding_sum_12m",
    "cbi_consume_outstanding_mean_12m",
    "cbi_consume_cur_month_amount_max_12m",
    "cbi_consume_cur_month_amount_mean_12m",
    "cbi_consume_outstanding_max_24m",
    "cbi_consume_outstanding_sum_24m",
    "cbi_consume_outstanding_mean_24m",
    "cbi_consume_cur_month_amount_max_24m",
    "cbi_consume_cur_month_amount_mean_24m",
    "cbi_consume_outstanding_skewness_6m",
    "cbi_consume_outstanding_kurtosis_6m",
    "cbi_consume_cur_month_amount_skewness_6m",
    "cbi_consume_cur_month_amount_kurtosis_6m",
    "cbi_consume_outstanding_skewness_12m",
    "cbi_consume_outstanding_kurtosis_12m",
    "cbi_consume_cur_month_amount_skewness_12m",
    "cbi_consume_cur_month_amount_kurtosis_12m",
    "cbi_consume_outstanding_skewness_24m",
    "cbi_consume_outstanding_kurtosis_24m",
    "cbi_consume_cur_month_amount_skewness_24m",
    "cbi_consume_cur_month_amount_kurtosis_24m",
    "cbi_consume_outstanding_skewness_all",
    "cbi_consume_outstanding_kurtosis_all",
    "cbi_consume_cur_month_amount_skewness_all",
    "cbi_consume_cur_month_amount_kurtosis_all",
    "cbi_credit_remarks_paylater_flag_cnt_6m",
    "cbi_credit_remarks_paylater_flag_cnt_rate_6m",
    "cbi_credit_remarks_paylater_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_6m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_rate_6m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_akulaku_flag_cnt_6m",
    "cbi_credit_remarks_akulaku_flag_cnt_rate_6m",
    "cbi_credit_remarks_akulaku_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_kredivo_flag_cnt_6m",
    "cbi_credit_remarks_kredivo_flag_cnt_rate_6m",
    "cbi_credit_remarks_kredivo_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_easycash_flag_cnt_6m",
    "cbi_credit_remarks_easycash_flag_cnt_rate_6m",
    "cbi_credit_remarks_easycash_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_adapundi_flag_cnt_6m",
    "cbi_credit_remarks_adapundi_flag_cnt_rate_6m",
    "cbi_credit_remarks_adapundi_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_adakami_flag_cnt_6m",
    "cbi_credit_remarks_adakami_flag_cnt_rate_6m",
    "cbi_credit_remarks_adakami_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_julo_flag_cnt_6m",
    "cbi_credit_remarks_julo_flag_cnt_rate_6m",
    "cbi_credit_remarks_julo_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_indodana_flag_cnt_6m",
    "cbi_credit_remarks_indodana_flag_cnt_rate_6m",
    "cbi_credit_remarks_indodana_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_atome_flag_cnt_6m",
    "cbi_credit_remarks_atome_flag_cnt_rate_6m",
    "cbi_credit_remarks_atome_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_6m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_kredifazz_flag_cnt_6m",
    "cbi_credit_remarks_kredifazz_flag_cnt_rate_6m",
    "cbi_credit_remarks_kredifazz_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_finaccel_flag_cnt_6m",
    "cbi_credit_remarks_finaccel_flag_cnt_rate_6m",
    "cbi_credit_remarks_finaccel_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_amartha_flag_cnt_6m",
    "cbi_credit_remarks_amartha_flag_cnt_rate_6m",
    "cbi_credit_remarks_amartha_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_uangme_flag_cnt_6m",
    "cbi_credit_remarks_uangme_flag_cnt_rate_6m",
    "cbi_credit_remarks_uangme_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_6m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_rate_6m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_6m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_rate_6m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_6m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_rate_6m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_6m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_rate_6m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_6m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_rate_6m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_6m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_rate_6m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_6m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_rate_6m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_6m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_rate_6m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_6m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_rate_6m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_6m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_rate_6m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_danarupiah_flag_cnt_6m",
    "cbi_credit_remarks_danarupiah_flag_cnt_rate_6m",
    "cbi_credit_remarks_danarupiah_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_asetku_flag_cnt_6m",
    "cbi_credit_remarks_asetku_flag_cnt_rate_6m",
    "cbi_credit_remarks_asetku_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_6m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mega_finance_flag_cnt_6m",
    "cbi_credit_remarks_mega_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_mega_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_6m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_6m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_6m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_rate_6m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_covid19_related_flag_cnt_6m",
    "cbi_credit_remarks_covid19_related_flag_cnt_rate_6m",
    "cbi_credit_remarks_covid19_related_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_paid_off_flag_cnt_6m",
    "cbi_credit_remarks_paid_off_flag_cnt_rate_6m",
    "cbi_credit_remarks_paid_off_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_written_off_flag_cnt_6m",
    "cbi_credit_remarks_written_off_flag_cnt_rate_6m",
    "cbi_credit_remarks_written_off_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_6m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_rate_6m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_joint_financing_flag_cnt_6m",
    "cbi_credit_remarks_joint_financing_flag_cnt_rate_6m",
    "cbi_credit_remarks_joint_financing_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_channeling_product_flag_cnt_6m",
    "cbi_credit_remarks_channeling_product_flag_cnt_rate_6m",
    "cbi_credit_remarks_channeling_product_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_system_migration_flag_cnt_6m",
    "cbi_credit_remarks_system_migration_flag_cnt_rate_6m",
    "cbi_credit_remarks_system_migration_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_credit_card_flag_cnt_6m",
    "cbi_credit_remarks_credit_card_flag_cnt_rate_6m",
    "cbi_credit_remarks_credit_card_flag_cnt_all_rate_6m",
    "cbi_credit_remarks_paylater_flag_cnt_12m",
    "cbi_credit_remarks_paylater_flag_cnt_rate_12m",
    "cbi_credit_remarks_paylater_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_12m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_rate_12m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_akulaku_flag_cnt_12m",
    "cbi_credit_remarks_akulaku_flag_cnt_rate_12m",
    "cbi_credit_remarks_akulaku_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_kredivo_flag_cnt_12m",
    "cbi_credit_remarks_kredivo_flag_cnt_rate_12m",
    "cbi_credit_remarks_kredivo_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_easycash_flag_cnt_12m",
    "cbi_credit_remarks_easycash_flag_cnt_rate_12m",
    "cbi_credit_remarks_easycash_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_adapundi_flag_cnt_12m",
    "cbi_credit_remarks_adapundi_flag_cnt_rate_12m",
    "cbi_credit_remarks_adapundi_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_adakami_flag_cnt_12m",
    "cbi_credit_remarks_adakami_flag_cnt_rate_12m",
    "cbi_credit_remarks_adakami_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_julo_flag_cnt_12m",
    "cbi_credit_remarks_julo_flag_cnt_rate_12m",
    "cbi_credit_remarks_julo_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_indodana_flag_cnt_12m",
    "cbi_credit_remarks_indodana_flag_cnt_rate_12m",
    "cbi_credit_remarks_indodana_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_atome_flag_cnt_12m",
    "cbi_credit_remarks_atome_flag_cnt_rate_12m",
    "cbi_credit_remarks_atome_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_12m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_kredifazz_flag_cnt_12m",
    "cbi_credit_remarks_kredifazz_flag_cnt_rate_12m",
    "cbi_credit_remarks_kredifazz_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_finaccel_flag_cnt_12m",
    "cbi_credit_remarks_finaccel_flag_cnt_rate_12m",
    "cbi_credit_remarks_finaccel_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_amartha_flag_cnt_12m",
    "cbi_credit_remarks_amartha_flag_cnt_rate_12m",
    "cbi_credit_remarks_amartha_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_uangme_flag_cnt_12m",
    "cbi_credit_remarks_uangme_flag_cnt_rate_12m",
    "cbi_credit_remarks_uangme_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_12m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_rate_12m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_12m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_rate_12m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_12m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_rate_12m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_12m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_rate_12m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_12m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_rate_12m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_12m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_rate_12m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_12m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_rate_12m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_12m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_rate_12m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_12m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_rate_12m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_12m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_rate_12m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_danarupiah_flag_cnt_12m",
    "cbi_credit_remarks_danarupiah_flag_cnt_rate_12m",
    "cbi_credit_remarks_danarupiah_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_asetku_flag_cnt_12m",
    "cbi_credit_remarks_asetku_flag_cnt_rate_12m",
    "cbi_credit_remarks_asetku_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_12m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mega_finance_flag_cnt_12m",
    "cbi_credit_remarks_mega_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_mega_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_12m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_12m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_12m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_rate_12m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_covid19_related_flag_cnt_12m",
    "cbi_credit_remarks_covid19_related_flag_cnt_rate_12m",
    "cbi_credit_remarks_covid19_related_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_paid_off_flag_cnt_12m",
    "cbi_credit_remarks_paid_off_flag_cnt_rate_12m",
    "cbi_credit_remarks_paid_off_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_written_off_flag_cnt_12m",
    "cbi_credit_remarks_written_off_flag_cnt_rate_12m",
    "cbi_credit_remarks_written_off_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_12m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_rate_12m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_joint_financing_flag_cnt_12m",
    "cbi_credit_remarks_joint_financing_flag_cnt_rate_12m",
    "cbi_credit_remarks_joint_financing_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_channeling_product_flag_cnt_12m",
    "cbi_credit_remarks_channeling_product_flag_cnt_rate_12m",
    "cbi_credit_remarks_channeling_product_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_system_migration_flag_cnt_12m",
    "cbi_credit_remarks_system_migration_flag_cnt_rate_12m",
    "cbi_credit_remarks_system_migration_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_credit_card_flag_cnt_12m",
    "cbi_credit_remarks_credit_card_flag_cnt_rate_12m",
    "cbi_credit_remarks_credit_card_flag_cnt_all_rate_12m",
    "cbi_credit_remarks_paylater_flag_cnt_24m",
    "cbi_credit_remarks_paylater_flag_cnt_rate_24m",
    "cbi_credit_remarks_paylater_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_24m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_rate_24m",
    "cbi_credit_remarks_dana_tunai_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_akulaku_flag_cnt_24m",
    "cbi_credit_remarks_akulaku_flag_cnt_rate_24m",
    "cbi_credit_remarks_akulaku_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_kredivo_flag_cnt_24m",
    "cbi_credit_remarks_kredivo_flag_cnt_rate_24m",
    "cbi_credit_remarks_kredivo_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_easycash_flag_cnt_24m",
    "cbi_credit_remarks_easycash_flag_cnt_rate_24m",
    "cbi_credit_remarks_easycash_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_adapundi_flag_cnt_24m",
    "cbi_credit_remarks_adapundi_flag_cnt_rate_24m",
    "cbi_credit_remarks_adapundi_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_adakami_flag_cnt_24m",
    "cbi_credit_remarks_adakami_flag_cnt_rate_24m",
    "cbi_credit_remarks_adakami_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_julo_flag_cnt_24m",
    "cbi_credit_remarks_julo_flag_cnt_rate_24m",
    "cbi_credit_remarks_julo_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_indodana_flag_cnt_24m",
    "cbi_credit_remarks_indodana_flag_cnt_rate_24m",
    "cbi_credit_remarks_indodana_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_atome_flag_cnt_24m",
    "cbi_credit_remarks_atome_flag_cnt_rate_24m",
    "cbi_credit_remarks_atome_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_24m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_commerce_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_kredifazz_flag_cnt_24m",
    "cbi_credit_remarks_kredifazz_flag_cnt_rate_24m",
    "cbi_credit_remarks_kredifazz_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_finaccel_flag_cnt_24m",
    "cbi_credit_remarks_finaccel_flag_cnt_rate_24m",
    "cbi_credit_remarks_finaccel_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_amartha_flag_cnt_24m",
    "cbi_credit_remarks_amartha_flag_cnt_rate_24m",
    "cbi_credit_remarks_amartha_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_uangme_flag_cnt_24m",
    "cbi_credit_remarks_uangme_flag_cnt_rate_24m",
    "cbi_credit_remarks_uangme_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_24m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_rate_24m",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_24m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_rate_24m",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_24m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_rate_24m",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_24m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_rate_24m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_24m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_rate_24m",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_24m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_rate_24m",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_24m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_rate_24m",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_24m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_rate_24m",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_24m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_rate_24m",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_24m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_rate_24m",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_danarupiah_flag_cnt_24m",
    "cbi_credit_remarks_danarupiah_flag_cnt_rate_24m",
    "cbi_credit_remarks_danarupiah_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_asetku_flag_cnt_24m",
    "cbi_credit_remarks_asetku_flag_cnt_rate_24m",
    "cbi_credit_remarks_asetku_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_24m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mega_finance_flag_cnt_24m",
    "cbi_credit_remarks_mega_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_mega_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_24m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_24m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_24m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_rate_24m",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_covid19_related_flag_cnt_24m",
    "cbi_credit_remarks_covid19_related_flag_cnt_rate_24m",
    "cbi_credit_remarks_covid19_related_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_paid_off_flag_cnt_24m",
    "cbi_credit_remarks_paid_off_flag_cnt_rate_24m",
    "cbi_credit_remarks_paid_off_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_written_off_flag_cnt_24m",
    "cbi_credit_remarks_written_off_flag_cnt_rate_24m",
    "cbi_credit_remarks_written_off_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_24m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_rate_24m",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_joint_financing_flag_cnt_24m",
    "cbi_credit_remarks_joint_financing_flag_cnt_rate_24m",
    "cbi_credit_remarks_joint_financing_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_channeling_product_flag_cnt_24m",
    "cbi_credit_remarks_channeling_product_flag_cnt_rate_24m",
    "cbi_credit_remarks_channeling_product_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_system_migration_flag_cnt_24m",
    "cbi_credit_remarks_system_migration_flag_cnt_rate_24m",
    "cbi_credit_remarks_system_migration_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_credit_card_flag_cnt_24m",
    "cbi_credit_remarks_credit_card_flag_cnt_rate_24m",
    "cbi_credit_remarks_credit_card_flag_cnt_all_rate_24m",
    "cbi_credit_remarks_paylater_flag_cnt",
    "cbi_credit_remarks_paylater_flag_cnt_rate",
    "cbi_credit_remarks_paylater_flag_cnt_all_rate",
    "cbi_credit_remarks_dana_tunai_flag_cnt",
    "cbi_credit_remarks_dana_tunai_flag_cnt_rate",
    "cbi_credit_remarks_dana_tunai_flag_cnt_all_rate",
    "cbi_credit_remarks_akulaku_flag_cnt",
    "cbi_credit_remarks_akulaku_flag_cnt_rate",
    "cbi_credit_remarks_akulaku_flag_cnt_all_rate",
    "cbi_credit_remarks_kredivo_flag_cnt",
    "cbi_credit_remarks_kredivo_flag_cnt_rate",
    "cbi_credit_remarks_kredivo_flag_cnt_all_rate",
    "cbi_credit_remarks_easycash_flag_cnt",
    "cbi_credit_remarks_easycash_flag_cnt_rate",
    "cbi_credit_remarks_easycash_flag_cnt_all_rate",
    "cbi_credit_remarks_adapundi_flag_cnt",
    "cbi_credit_remarks_adapundi_flag_cnt_rate",
    "cbi_credit_remarks_adapundi_flag_cnt_all_rate",
    "cbi_credit_remarks_adakami_flag_cnt",
    "cbi_credit_remarks_adakami_flag_cnt_rate",
    "cbi_credit_remarks_adakami_flag_cnt_all_rate",
    "cbi_credit_remarks_julo_flag_cnt",
    "cbi_credit_remarks_julo_flag_cnt_rate",
    "cbi_credit_remarks_julo_flag_cnt_all_rate",
    "cbi_credit_remarks_indodana_flag_cnt",
    "cbi_credit_remarks_indodana_flag_cnt_rate",
    "cbi_credit_remarks_indodana_flag_cnt_all_rate",
    "cbi_credit_remarks_atome_flag_cnt",
    "cbi_credit_remarks_atome_flag_cnt_rate",
    "cbi_credit_remarks_atome_flag_cnt_all_rate",
    "cbi_credit_remarks_commerce_finance_flag_cnt",
    "cbi_credit_remarks_commerce_finance_flag_cnt_rate",
    "cbi_credit_remarks_commerce_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_kredifazz_flag_cnt",
    "cbi_credit_remarks_kredifazz_flag_cnt_rate",
    "cbi_credit_remarks_kredifazz_flag_cnt_all_rate",
    "cbi_credit_remarks_finaccel_flag_cnt",
    "cbi_credit_remarks_finaccel_flag_cnt_rate",
    "cbi_credit_remarks_finaccel_flag_cnt_all_rate",
    "cbi_credit_remarks_amartha_flag_cnt",
    "cbi_credit_remarks_amartha_flag_cnt_rate",
    "cbi_credit_remarks_amartha_flag_cnt_all_rate",
    "cbi_credit_remarks_uangme_flag_cnt",
    "cbi_credit_remarks_uangme_flag_cnt_rate",
    "cbi_credit_remarks_uangme_flag_cnt_all_rate",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_rate",
    "cbi_credit_remarks_lentera_dana_nusantara_flag_cnt_all_rate",
    "cbi_credit_remarks_kredit_pintar_flag_cnt",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_rate",
    "cbi_credit_remarks_kredit_pintar_flag_cnt_all_rate",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_rate",
    "cbi_credit_remarks_mapan_global_reksa_flag_cnt_all_rate",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_rate",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_flag_cnt_all_rate",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_rate",
    "cbi_credit_remarks_indonesia_fintopia_technology_flag_cnt_all_rate",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_rate",
    "cbi_credit_remarks_info_tekno_siaga_flag_cnt_all_rate",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_rate",
    "cbi_credit_remarks_pintar_inovasi_digital_flag_cnt_all_rate",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_rate",
    "cbi_credit_remarks_multifinance_anak_bangsa_flag_cnt_all_rate",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_rate",
    "cbi_credit_remarks_home_credit_indonesia_flag_cnt_all_rate",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_rate",
    "cbi_credit_remarks_rupiah_cepat_flag_cnt_all_rate",
    "cbi_credit_remarks_danarupiah_flag_cnt",
    "cbi_credit_remarks_danarupiah_flag_cnt_rate",
    "cbi_credit_remarks_danarupiah_flag_cnt_all_rate",
    "cbi_credit_remarks_asetku_flag_cnt",
    "cbi_credit_remarks_asetku_flag_cnt_rate",
    "cbi_credit_remarks_asetku_flag_cnt_all_rate",
    "cbi_credit_remarks_mega_central_finance_flag_cnt",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_rate",
    "cbi_credit_remarks_mega_central_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_mega_finance_flag_cnt",
    "cbi_credit_remarks_mega_finance_flag_cnt_rate",
    "cbi_credit_remarks_mega_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_rate",
    "cbi_credit_remarks_mega_auto_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_rate",
    "cbi_credit_remarks_mandiri_utama_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_rate",
    "cbi_credit_remarks_mandiri_tunas_finance_flag_cnt_all_rate",
    "cbi_credit_remarks_covid19_related_flag_cnt",
    "cbi_credit_remarks_covid19_related_flag_cnt_rate",
    "cbi_credit_remarks_covid19_related_flag_cnt_all_rate",
    "cbi_credit_remarks_paid_off_flag_cnt",
    "cbi_credit_remarks_paid_off_flag_cnt_rate",
    "cbi_credit_remarks_paid_off_flag_cnt_all_rate",
    "cbi_credit_remarks_written_off_flag_cnt",
    "cbi_credit_remarks_written_off_flag_cnt_rate",
    "cbi_credit_remarks_written_off_flag_cnt_all_rate",
    "cbi_credit_remarks_sold_to_collector_flag_cnt",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_rate",
    "cbi_credit_remarks_sold_to_collector_flag_cnt_all_rate",
    "cbi_credit_remarks_joint_financing_flag_cnt",
    "cbi_credit_remarks_joint_financing_flag_cnt_rate",
    "cbi_credit_remarks_joint_financing_flag_cnt_all_rate",
    "cbi_credit_remarks_channeling_product_flag_cnt",
    "cbi_credit_remarks_channeling_product_flag_cnt_rate",
    "cbi_credit_remarks_channeling_product_flag_cnt_all_rate",
    "cbi_credit_remarks_system_migration_flag_cnt",
    "cbi_credit_remarks_system_migration_flag_cnt_rate",
    "cbi_credit_remarks_system_migration_flag_cnt_all_rate",
    "cbi_credit_remarks_credit_card_flag_cnt",
    "cbi_credit_remarks_credit_card_flag_cnt_rate",
    "cbi_credit_remarks_credit_card_flag_cnt_all_rate",
    "cbi_credit_remarks_paylater_limit_max_6m",
    "cbi_credit_remarks_paylater_limit_sum_6m",
    "cbi_credit_remarks_dana_tunai_limit_max_6m",
    "cbi_credit_remarks_dana_tunai_limit_sum_6m",
    "cbi_credit_remarks_akulaku_limit_max_6m",
    "cbi_credit_remarks_akulaku_limit_sum_6m",
    "cbi_credit_remarks_kredivo_limit_max_6m",
    "cbi_credit_remarks_kredivo_limit_sum_6m",
    "cbi_credit_remarks_easycash_limit_max_6m",
    "cbi_credit_remarks_easycash_limit_sum_6m",
    "cbi_credit_remarks_adapundi_limit_max_6m",
    "cbi_credit_remarks_adapundi_limit_sum_6m",
    "cbi_credit_remarks_adakami_limit_max_6m",
    "cbi_credit_remarks_adakami_limit_sum_6m",
    "cbi_credit_remarks_julo_limit_max_6m",
    "cbi_credit_remarks_julo_limit_sum_6m",
    "cbi_credit_remarks_indodana_limit_max_6m",
    "cbi_credit_remarks_indodana_limit_sum_6m",
    "cbi_credit_remarks_atome_limit_max_6m",
    "cbi_credit_remarks_atome_limit_sum_6m",
    "cbi_credit_remarks_commerce_finance_limit_max_6m",
    "cbi_credit_remarks_commerce_finance_limit_sum_6m",
    "cbi_credit_remarks_kredifazz_limit_max_6m",
    "cbi_credit_remarks_kredifazz_limit_sum_6m",
    "cbi_credit_remarks_finaccel_limit_max_6m",
    "cbi_credit_remarks_finaccel_limit_sum_6m",
    "cbi_credit_remarks_amartha_limit_max_6m",
    "cbi_credit_remarks_amartha_limit_sum_6m",
    "cbi_credit_remarks_uangme_limit_max_6m",
    "cbi_credit_remarks_uangme_limit_sum_6m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_max_6m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_sum_6m",
    "cbi_credit_remarks_kredit_pintar_limit_max_6m",
    "cbi_credit_remarks_kredit_pintar_limit_sum_6m",
    "cbi_credit_remarks_mapan_global_reksa_limit_max_6m",
    "cbi_credit_remarks_mapan_global_reksa_limit_sum_6m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_max_6m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_sum_6m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_max_6m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_sum_6m",
    "cbi_credit_remarks_info_tekno_siaga_limit_max_6m",
    "cbi_credit_remarks_info_tekno_siaga_limit_sum_6m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_max_6m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_sum_6m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_max_6m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_sum_6m",
    "cbi_credit_remarks_home_credit_indonesia_limit_max_6m",
    "cbi_credit_remarks_home_credit_indonesia_limit_sum_6m",
    "cbi_credit_remarks_rupiah_cepat_limit_max_6m",
    "cbi_credit_remarks_rupiah_cepat_limit_sum_6m",
    "cbi_credit_remarks_danarupiah_limit_max_6m",
    "cbi_credit_remarks_danarupiah_limit_sum_6m",
    "cbi_credit_remarks_asetku_limit_max_6m",
    "cbi_credit_remarks_asetku_limit_sum_6m",
    "cbi_credit_remarks_mega_central_finance_limit_max_6m",
    "cbi_credit_remarks_mega_central_finance_limit_sum_6m",
    "cbi_credit_remarks_mega_finance_limit_max_6m",
    "cbi_credit_remarks_mega_finance_limit_sum_6m",
    "cbi_credit_remarks_mega_auto_finance_limit_max_6m",
    "cbi_credit_remarks_mega_auto_finance_limit_sum_6m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_max_6m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_sum_6m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_max_6m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_sum_6m",
    "cbi_credit_remarks_covid19_related_limit_max_6m",
    "cbi_credit_remarks_covid19_related_limit_sum_6m",
    "cbi_credit_remarks_paid_off_limit_max_6m",
    "cbi_credit_remarks_paid_off_limit_sum_6m",
    "cbi_credit_remarks_written_off_limit_max_6m",
    "cbi_credit_remarks_written_off_limit_sum_6m",
    "cbi_credit_remarks_sold_to_collector_limit_max_6m",
    "cbi_credit_remarks_sold_to_collector_limit_sum_6m",
    "cbi_credit_remarks_joint_financing_limit_max_6m",
    "cbi_credit_remarks_joint_financing_limit_sum_6m",
    "cbi_credit_remarks_channeling_product_limit_max_6m",
    "cbi_credit_remarks_channeling_product_limit_sum_6m",
    "cbi_credit_remarks_system_migration_limit_max_6m",
    "cbi_credit_remarks_system_migration_limit_sum_6m",
    "cbi_credit_remarks_credit_card_limit_max_6m",
    "cbi_credit_remarks_credit_card_limit_sum_6m",
    "cbi_credit_remarks_paylater_limit_max_12m",
    "cbi_credit_remarks_paylater_limit_sum_12m",
    "cbi_credit_remarks_dana_tunai_limit_max_12m",
    "cbi_credit_remarks_dana_tunai_limit_sum_12m",
    "cbi_credit_remarks_akulaku_limit_max_12m",
    "cbi_credit_remarks_akulaku_limit_sum_12m",
    "cbi_credit_remarks_kredivo_limit_max_12m",
    "cbi_credit_remarks_kredivo_limit_sum_12m",
    "cbi_credit_remarks_easycash_limit_max_12m",
    "cbi_credit_remarks_easycash_limit_sum_12m",
    "cbi_credit_remarks_adapundi_limit_max_12m",
    "cbi_credit_remarks_adapundi_limit_sum_12m",
    "cbi_credit_remarks_adakami_limit_max_12m",
    "cbi_credit_remarks_adakami_limit_sum_12m",
    "cbi_credit_remarks_julo_limit_max_12m",
    "cbi_credit_remarks_julo_limit_sum_12m",
    "cbi_credit_remarks_indodana_limit_max_12m",
    "cbi_credit_remarks_indodana_limit_sum_12m",
    "cbi_credit_remarks_atome_limit_max_12m",
    "cbi_credit_remarks_atome_limit_sum_12m",
    "cbi_credit_remarks_commerce_finance_limit_max_12m",
    "cbi_credit_remarks_commerce_finance_limit_sum_12m",
    "cbi_credit_remarks_kredifazz_limit_max_12m",
    "cbi_credit_remarks_kredifazz_limit_sum_12m",
    "cbi_credit_remarks_finaccel_limit_max_12m",
    "cbi_credit_remarks_finaccel_limit_sum_12m",
    "cbi_credit_remarks_amartha_limit_max_12m",
    "cbi_credit_remarks_amartha_limit_sum_12m",
    "cbi_credit_remarks_uangme_limit_max_12m",
    "cbi_credit_remarks_uangme_limit_sum_12m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_max_12m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_sum_12m",
    "cbi_credit_remarks_kredit_pintar_limit_max_12m",
    "cbi_credit_remarks_kredit_pintar_limit_sum_12m",
    "cbi_credit_remarks_mapan_global_reksa_limit_max_12m",
    "cbi_credit_remarks_mapan_global_reksa_limit_sum_12m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_max_12m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_sum_12m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_max_12m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_sum_12m",
    "cbi_credit_remarks_info_tekno_siaga_limit_max_12m",
    "cbi_credit_remarks_info_tekno_siaga_limit_sum_12m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_max_12m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_sum_12m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_max_12m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_sum_12m",
    "cbi_credit_remarks_home_credit_indonesia_limit_max_12m",
    "cbi_credit_remarks_home_credit_indonesia_limit_sum_12m",
    "cbi_credit_remarks_rupiah_cepat_limit_max_12m",
    "cbi_credit_remarks_rupiah_cepat_limit_sum_12m",
    "cbi_credit_remarks_danarupiah_limit_max_12m",
    "cbi_credit_remarks_danarupiah_limit_sum_12m",
    "cbi_credit_remarks_asetku_limit_max_12m",
    "cbi_credit_remarks_asetku_limit_sum_12m",
    "cbi_credit_remarks_mega_central_finance_limit_max_12m",
    "cbi_credit_remarks_mega_central_finance_limit_sum_12m",
    "cbi_credit_remarks_mega_finance_limit_max_12m",
    "cbi_credit_remarks_mega_finance_limit_sum_12m",
    "cbi_credit_remarks_mega_auto_finance_limit_max_12m",
    "cbi_credit_remarks_mega_auto_finance_limit_sum_12m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_max_12m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_sum_12m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_max_12m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_sum_12m",
    "cbi_credit_remarks_covid19_related_limit_max_12m",
    "cbi_credit_remarks_covid19_related_limit_sum_12m",
    "cbi_credit_remarks_paid_off_limit_max_12m",
    "cbi_credit_remarks_paid_off_limit_sum_12m",
    "cbi_credit_remarks_written_off_limit_max_12m",
    "cbi_credit_remarks_written_off_limit_sum_12m",
    "cbi_credit_remarks_sold_to_collector_limit_max_12m",
    "cbi_credit_remarks_sold_to_collector_limit_sum_12m",
    "cbi_credit_remarks_joint_financing_limit_max_12m",
    "cbi_credit_remarks_joint_financing_limit_sum_12m",
    "cbi_credit_remarks_channeling_product_limit_max_12m",
    "cbi_credit_remarks_channeling_product_limit_sum_12m",
    "cbi_credit_remarks_system_migration_limit_max_12m",
    "cbi_credit_remarks_system_migration_limit_sum_12m",
    "cbi_credit_remarks_credit_card_limit_max_12m",
    "cbi_credit_remarks_credit_card_limit_sum_12m",
    "cbi_credit_remarks_paylater_limit_max_24m",
    "cbi_credit_remarks_paylater_limit_sum_24m",
    "cbi_credit_remarks_dana_tunai_limit_max_24m",
    "cbi_credit_remarks_dana_tunai_limit_sum_24m",
    "cbi_credit_remarks_akulaku_limit_max_24m",
    "cbi_credit_remarks_akulaku_limit_sum_24m",
    "cbi_credit_remarks_kredivo_limit_max_24m",
    "cbi_credit_remarks_kredivo_limit_sum_24m",
    "cbi_credit_remarks_easycash_limit_max_24m",
    "cbi_credit_remarks_easycash_limit_sum_24m",
    "cbi_credit_remarks_adapundi_limit_max_24m",
    "cbi_credit_remarks_adapundi_limit_sum_24m",
    "cbi_credit_remarks_adakami_limit_max_24m",
    "cbi_credit_remarks_adakami_limit_sum_24m",
    "cbi_credit_remarks_julo_limit_max_24m",
    "cbi_credit_remarks_julo_limit_sum_24m",
    "cbi_credit_remarks_indodana_limit_max_24m",
    "cbi_credit_remarks_indodana_limit_sum_24m",
    "cbi_credit_remarks_atome_limit_max_24m",
    "cbi_credit_remarks_atome_limit_sum_24m",
    "cbi_credit_remarks_commerce_finance_limit_max_24m",
    "cbi_credit_remarks_commerce_finance_limit_sum_24m",
    "cbi_credit_remarks_kredifazz_limit_max_24m",
    "cbi_credit_remarks_kredifazz_limit_sum_24m",
    "cbi_credit_remarks_finaccel_limit_max_24m",
    "cbi_credit_remarks_finaccel_limit_sum_24m",
    "cbi_credit_remarks_amartha_limit_max_24m",
    "cbi_credit_remarks_amartha_limit_sum_24m",
    "cbi_credit_remarks_uangme_limit_max_24m",
    "cbi_credit_remarks_uangme_limit_sum_24m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_max_24m",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_sum_24m",
    "cbi_credit_remarks_kredit_pintar_limit_max_24m",
    "cbi_credit_remarks_kredit_pintar_limit_sum_24m",
    "cbi_credit_remarks_mapan_global_reksa_limit_max_24m",
    "cbi_credit_remarks_mapan_global_reksa_limit_sum_24m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_max_24m",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_sum_24m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_max_24m",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_sum_24m",
    "cbi_credit_remarks_info_tekno_siaga_limit_max_24m",
    "cbi_credit_remarks_info_tekno_siaga_limit_sum_24m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_max_24m",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_sum_24m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_max_24m",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_sum_24m",
    "cbi_credit_remarks_home_credit_indonesia_limit_max_24m",
    "cbi_credit_remarks_home_credit_indonesia_limit_sum_24m",
    "cbi_credit_remarks_rupiah_cepat_limit_max_24m",
    "cbi_credit_remarks_rupiah_cepat_limit_sum_24m",
    "cbi_credit_remarks_danarupiah_limit_max_24m",
    "cbi_credit_remarks_danarupiah_limit_sum_24m",
    "cbi_credit_remarks_asetku_limit_max_24m",
    "cbi_credit_remarks_asetku_limit_sum_24m",
    "cbi_credit_remarks_mega_central_finance_limit_max_24m",
    "cbi_credit_remarks_mega_central_finance_limit_sum_24m",
    "cbi_credit_remarks_mega_finance_limit_max_24m",
    "cbi_credit_remarks_mega_finance_limit_sum_24m",
    "cbi_credit_remarks_mega_auto_finance_limit_max_24m",
    "cbi_credit_remarks_mega_auto_finance_limit_sum_24m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_max_24m",
    "cbi_credit_remarks_mandiri_utama_finance_limit_sum_24m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_max_24m",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_sum_24m",
    "cbi_credit_remarks_covid19_related_limit_max_24m",
    "cbi_credit_remarks_covid19_related_limit_sum_24m",
    "cbi_credit_remarks_paid_off_limit_max_24m",
    "cbi_credit_remarks_paid_off_limit_sum_24m",
    "cbi_credit_remarks_written_off_limit_max_24m",
    "cbi_credit_remarks_written_off_limit_sum_24m",
    "cbi_credit_remarks_sold_to_collector_limit_max_24m",
    "cbi_credit_remarks_sold_to_collector_limit_sum_24m",
    "cbi_credit_remarks_joint_financing_limit_max_24m",
    "cbi_credit_remarks_joint_financing_limit_sum_24m",
    "cbi_credit_remarks_channeling_product_limit_max_24m",
    "cbi_credit_remarks_channeling_product_limit_sum_24m",
    "cbi_credit_remarks_system_migration_limit_max_24m",
    "cbi_credit_remarks_system_migration_limit_sum_24m",
    "cbi_credit_remarks_credit_card_limit_max_24m",
    "cbi_credit_remarks_credit_card_limit_sum_24m",
    "cbi_credit_remarks_paylater_limit_max",
    "cbi_credit_remarks_paylater_limit_sum",
    "cbi_credit_remarks_dana_tunai_limit_max",
    "cbi_credit_remarks_dana_tunai_limit_sum",
    "cbi_credit_remarks_akulaku_limit_max",
    "cbi_credit_remarks_akulaku_limit_sum",
    "cbi_credit_remarks_kredivo_limit_max",
    "cbi_credit_remarks_kredivo_limit_sum",
    "cbi_credit_remarks_easycash_limit_max",
    "cbi_credit_remarks_easycash_limit_sum",
    "cbi_credit_remarks_adapundi_limit_max",
    "cbi_credit_remarks_adapundi_limit_sum",
    "cbi_credit_remarks_adakami_limit_max",
    "cbi_credit_remarks_adakami_limit_sum",
    "cbi_credit_remarks_julo_limit_max",
    "cbi_credit_remarks_julo_limit_sum",
    "cbi_credit_remarks_indodana_limit_max",
    "cbi_credit_remarks_indodana_limit_sum",
    "cbi_credit_remarks_atome_limit_max",
    "cbi_credit_remarks_atome_limit_sum",
    "cbi_credit_remarks_commerce_finance_limit_max",
    "cbi_credit_remarks_commerce_finance_limit_sum",
    "cbi_credit_remarks_kredifazz_limit_max",
    "cbi_credit_remarks_kredifazz_limit_sum",
    "cbi_credit_remarks_finaccel_limit_max",
    "cbi_credit_remarks_finaccel_limit_sum",
    "cbi_credit_remarks_amartha_limit_max",
    "cbi_credit_remarks_amartha_limit_sum",
    "cbi_credit_remarks_uangme_limit_max",
    "cbi_credit_remarks_uangme_limit_sum",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_max",
    "cbi_credit_remarks_lentera_dana_nusantara_limit_sum",
    "cbi_credit_remarks_kredit_pintar_limit_max",
    "cbi_credit_remarks_kredit_pintar_limit_sum",
    "cbi_credit_remarks_mapan_global_reksa_limit_max",
    "cbi_credit_remarks_mapan_global_reksa_limit_sum",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_max",
    "cbi_credit_remarks_pembiayaan_digital_indonesia_limit_sum",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_max",
    "cbi_credit_remarks_indonesia_fintopia_technology_limit_sum",
    "cbi_credit_remarks_info_tekno_siaga_limit_max",
    "cbi_credit_remarks_info_tekno_siaga_limit_sum",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_max",
    "cbi_credit_remarks_pintar_inovasi_digital_limit_sum",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_max",
    "cbi_credit_remarks_multifinance_anak_bangsa_limit_sum",
    "cbi_credit_remarks_home_credit_indonesia_limit_max",
    "cbi_credit_remarks_home_credit_indonesia_limit_sum",
    "cbi_credit_remarks_rupiah_cepat_limit_max",
    "cbi_credit_remarks_rupiah_cepat_limit_sum",
    "cbi_credit_remarks_danarupiah_limit_max",
    "cbi_credit_remarks_danarupiah_limit_sum",
    "cbi_credit_remarks_asetku_limit_max",
    "cbi_credit_remarks_asetku_limit_sum",
    "cbi_credit_remarks_mega_central_finance_limit_max",
    "cbi_credit_remarks_mega_central_finance_limit_sum",
    "cbi_credit_remarks_mega_finance_limit_max",
    "cbi_credit_remarks_mega_finance_limit_sum",
    "cbi_credit_remarks_mega_auto_finance_limit_max",
    "cbi_credit_remarks_mega_auto_finance_limit_sum",
    "cbi_credit_remarks_mandiri_utama_finance_limit_max",
    "cbi_credit_remarks_mandiri_utama_finance_limit_sum",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_max",
    "cbi_credit_remarks_mandiri_tunas_finance_limit_sum",
    "cbi_credit_remarks_covid19_related_limit_max",
    "cbi_credit_remarks_covid19_related_limit_sum",
    "cbi_credit_remarks_paid_off_limit_max",
    "cbi_credit_remarks_paid_off_limit_sum",
    "cbi_credit_remarks_written_off_limit_max",
    "cbi_credit_remarks_written_off_limit_sum",
    "cbi_credit_remarks_sold_to_collector_limit_max",
    "cbi_credit_remarks_sold_to_collector_limit_sum",
    "cbi_credit_remarks_joint_financing_limit_max",
    "cbi_credit_remarks_joint_financing_limit_sum",
    "cbi_credit_remarks_channeling_product_limit_max",
    "cbi_credit_remarks_channeling_product_limit_sum",
    "cbi_credit_remarks_system_migration_limit_max",
    "cbi_credit_remarks_system_migration_limit_sum",
    "cbi_credit_remarks_credit_card_limit_max",
    "cbi_credit_remarks_credit_card_limit_sum",
    "cbi_credit_remarks_limit_max_6m",
    "cbi_credit_remarks_limit_sum_6m",
    "cbi_credit_no_remarks_limit_max_6m",
    "cbi_credit_no_remarks_limit_sum_6m",
    "cbi_credit_remarks_limit_max_12m",
    "cbi_credit_remarks_limit_sum_12m",
    "cbi_credit_no_remarks_limit_max_12m",
    "cbi_credit_no_remarks_limit_sum_12m",
    "cbi_credit_remarks_limit_max_24m",
    "cbi_credit_remarks_limit_sum_24m",
    "cbi_credit_no_remarks_limit_max_24m",
    "cbi_credit_no_remarks_limit_sum_24m",
    "cbi_credit_remarks_limit_max",
    "cbi_credit_remarks_limit_sum",
    "cbi_credit_no_remarks_limit_max",
    "cbi_credit_no_remarks_limit_sum",
    "cbi_credit_remarks_repayment_amount_max_1m",
    "cbi_credit_remarks_repayment_amount_sum_1m",
    "cbi_credit_remarks_repayment_ins_num_1m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_1m",
    "cbi_credit_remarks_loan_num_1m",
    "cbi_credit_remarks_loan_amount_max_1m",
    "cbi_credit_remarks_loan_amount_sum_1m",
    "cbi_credit_remarks_loan_ins_num_1m",
    "cbi_credit_remarks_loan_num_ins_mean_1m",
    "cbi_credit_remarks_repayment_amount_max_2m",
    "cbi_credit_remarks_repayment_amount_sum_2m",
    "cbi_credit_remarks_repayment_ins_num_2m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_2m",
    "cbi_credit_remarks_loan_num_2m",
    "cbi_credit_remarks_loan_amount_max_2m",
    "cbi_credit_remarks_loan_amount_sum_2m",
    "cbi_credit_remarks_loan_ins_num_2m",
    "cbi_credit_remarks_loan_num_ins_mean_2m",
    "cbi_credit_remarks_repayment_amount_max_3m",
    "cbi_credit_remarks_repayment_amount_sum_3m",
    "cbi_credit_remarks_repayment_ins_num_3m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_3m",
    "cbi_credit_remarks_loan_num_3m",
    "cbi_credit_remarks_loan_amount_max_3m",
    "cbi_credit_remarks_loan_amount_sum_3m",
    "cbi_credit_remarks_loan_ins_num_3m",
    "cbi_credit_remarks_loan_num_ins_mean_3m",
    "cbi_credit_remarks_repayment_amount_max_6m",
    "cbi_credit_remarks_repayment_amount_sum_6m",
    "cbi_credit_remarks_repayment_ins_num_6m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_6m",
    "cbi_credit_remarks_loan_num_6m",
    "cbi_credit_remarks_loan_amount_max_6m",
    "cbi_credit_remarks_loan_amount_sum_6m",
    "cbi_credit_remarks_loan_ins_num_6m",
    "cbi_credit_remarks_loan_num_ins_mean_6m",
    "cbi_credit_remarks_repayment_amount_max_12m",
    "cbi_credit_remarks_repayment_amount_sum_12m",
    "cbi_credit_remarks_repayment_ins_num_12m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_12m",
    "cbi_credit_remarks_loan_num_12m",
    "cbi_credit_remarks_loan_amount_max_12m",
    "cbi_credit_remarks_loan_amount_sum_12m",
    "cbi_credit_remarks_loan_ins_num_12m",
    "cbi_credit_remarks_loan_num_ins_mean_12m",
    "cbi_credit_remarks_repayment_amount_max_36m",
    "cbi_credit_remarks_repayment_amount_sum_36m",
    "cbi_credit_remarks_repayment_ins_num_36m",
    "cbi_credit_remarks_cur_loan_outstanding_rate_max_36m",
    "cbi_credit_remarks_loan_num_36m",
    "cbi_credit_remarks_loan_amount_max_36m",
    "cbi_credit_remarks_loan_amount_sum_36m",
    "cbi_credit_remarks_loan_ins_num_36m",
    "cbi_credit_remarks_loan_num_ins_mean_36m",
    "cbi_credit_remarks_last_repayment_gay_months",
    "cbi_credit_remarks_last_loan_gay_months",
    "cbi_credit_remarks_aging_days_max",
    "cbi_credit_remarks_aging_days_median",
    "cbi_credit_remarks_aging_days_min",
}

pop_condition = [
    "Dialihkan atau dijual kepada pihak lain non-Pelapor",
    "Dialihkan ke Fasilitas lain",
    "Dialihkan atau Dijual ke Pelapor lain",
]

credit_card_type = [
    "Kartu Kredit/ Kartu Pembiayaan Syariah",
    "Kartu Kredit atau Kartu Pembiayaan Syariah",
]

room_type = [
    "rumah tangga untuk pemilikan rumah tinggal tipe diatas 21 s.d. 70",
    "rumah tangga untuk pemilikan rumah tinggal tipe diatas 70",
    "rumah tangga untuk pemilikan rumah tinggal tipe 22 sampai dengan 70",
    "rumah tangga untuk pemilikan rumah tinggal s.d. tipe 21",
    "rumah tangga untuk pemilikan rumah tinggal sampai dengan tipe 21",
    "rumah tangga untuk pemilikan rumah tinggal",
    "rumah tangga untuk pemilikan flat atau apartemen s.d. tipe 21",
    "rumah tangga untuk pemilikan flat atau apartemen tipe diatas 21 s.d. 70",
    "rumah tangga untuk pemilikan flat atau apartemen tipe diatas 70",
    "rumah tangga untuk pemilikan rumah toko (ruko) atau rumah kantor (rukan)",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal s.d tipe 21",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal tipe diatas 21 s.d. 70",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal tipe diatas 70",
    "rumah tangga untuk keperluan multiguna beragunan apartemen s.d tipe 21",
    "rumah tangga untuk keperluan multiguna beragunan apartemen tipe 22 s.d 70",
    "rumah tangga untuk keperluan multiguna beragunan apartemen tipe diatas 70",
    "rumah tangga untuk keperluan multiguna beragunan ruko/rukan",
]

car_type = [
    "rumah tangga untuk pemilikan mobil roda empat",
    "rumah tangga untuk pemilikan sepeda bermotor",
    "rumah tangga untuk pemilikan truk dan kendaraan bermotor roda enam atau lebih",
    "rumah tangga untuk pemilikan kendaraan bermotor lainnya",
]
car_2 = ["rumah tangga untuk pemilikan sepeda bermotor"]
car_4 = [
    "rumah tangga untuk pemilikan mobil roda empat",
    "rumah tangga untuk pemilikan truk dan kendaraan bermotor roda enam atau lebih",
    "rumah tangga untuk pemilikan kendaraan bermotor lainnya",
]

room_21 = [
    "rumah tangga untuk pemilikan rumah tinggal s.d. tipe 21",
    "rumah tangga untuk pemilikan rumah tinggal sampai dengan tipe 21",
    "rumah tangga untuk pemilikan flat atau apartemen s.d. tipe 21",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal s.d tipe 21",
    "rumah tangga untuk keperluan multiguna beragunan apartemen s.d tipe 21",
]
room_21_70 = [
    "rumah tangga untuk pemilikan rumah tinggal tipe diatas 21 s.d. 70",
    "rumah tangga untuk pemilikan rumah tinggal tipe 22 sampai dengan 70",
    "rumah tangga untuk pemilikan flat atau apartemen tipe diatas 21 s.d. 70",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal tipe diatas 21 s.d. 70",
    "rumah tangga untuk keperluan multiguna beragunan apartemen tipe 22 s.d 70",
]
room_70 = [
    "rumah tangga untuk pemilikan rumah tinggal tipe diatas 70",
    "rumah tangga untuk pemilikan flat atau apartemen tipe diatas 70",
    "rumah tangga untuk keperluan multiguna beragunan rumah tinggal tipe diatas 70",
    "rumah tangga untuk keperluan multiguna beragunan apartemen tipe diatas 70",
]
room_commerce = [
    "rumah tangga untuk pemilikan rumah toko (ruko) atau rumah kantor (rukan)",
    "rumah tangga untuk keperluan multiguna beragunan ruko/rukan",
]

mikro_enterprises = [
    "debitur usaha mikro, kecil, dan menengah ? mikro",
    "debitur umkm-umkm lainnya?mikro",
    "debitur umkm?dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin tertentu?mikro",
    "debitur umkm-dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin lainnya?mikro",
]
small_enterprises = [
    "debitur usaha mikro, kecil, dan menengah ? kecil",
    "debitur umkm-umkm lainnya?kecil",
    "debitur umkm-dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin tertentu?kecil",
    "debitur umkm-dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin lainnya-kecil",
]
medium_enterprises = [
    "debitur usaha mikro, kecil, dan menengah ? menengah",
    "debitur umkm-umkm lainnya?menengah",
    "debitur umkm-dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin tertentu-menengah",
    "debitur umkm-dengan penjaminan atau asuransi kredit atau pembiayaan-penjamin lainnya? menengah",
]


def cbi_credit_credit_feature(df):
    fea = {}
    if df.empty:
        return fea
    max_b_rows = df.loc[
        df.groupby("CREDIT_Creditor")["CREDIT_CreditStartDate_new"].idxmax()
    ]
    fea = {
        "cbi_cur_limit_max": max_b_rows["max_limit"].max(),
        "cbi_cur_limit_min": max_b_rows["max_limit"].min(),
        "cbi_cur_limit_mean": max_b_rows["max_limit"].mean(),
        "cbi_cur_limit_sum": max_b_rows["max_limit"].sum(),
    }
    for t_type, t_df in {
        "1m": df[df.gap_days <= 30],
        "2m": df[df.gap_days <= 60],
        "3m": df[df.gap_days <= 90],
        "6m": df[df.gap_days <= 183],
        "1year": df[df.gap_days <= 365],
        "2year": df[df.gap_days <= 730],
        "3year": df[df.gap_days <= 1095],
        "all": df,
    }.items():
        max_limit_rows = t_df.loc[t_df.groupby("CREDIT_Creditor")["max_limit"].idxmax()]
        fea[f"cbi_his_ins_max_limit_sum_{t_type}"] = max_limit_rows.max_limit.sum()
        fea[f"cbi_his_limit_max_{t_type}"] = t_df.max_limit.max()
        fea[f"cbi_his_limit_min_{t_type}"] = t_df.max_limit.min()
        fea[f"cbi_his_limit_mean_{t_type}"] = t_df.max_limit.mean()
        fea[f"cbi_his_limit_sum_{t_type}"] = t_df.max_limit.sum()
        on_loan = t_df[t_df.label == "ac"]
        if on_loan.empty:
            continue
        if on_loan.max_limit.sum() > 0:
            quota_rate = round(
                on_loan.CREDIT_Outstanding.sum() / on_loan.max_limit.sum(), 6
            )
            fea[f"cbi_onloan_quota_rate_{t_type}"] = (
                quota_rate if quota_rate <= 1 else 1
            )
        else:
            fea[f"cbi_onloan_quota_rate_{t_type}"] = 1
    return fea


##### 在贷


def cbi_credit_onloan_feature(df):
    fea = {}
    time_slices = {"1m": 30, "2m": 60, "3m": 90, "6m": 183, "12m": 365, "24m": 730}

    # Time periods for skewness and kurtosis calculation
    skew_kurt_periods = {"6m": 183, "12m": 365, "24m": 730, "all": float("inf")}

    # Calculate features for all time periods
    for time_suffix, days_threshold in time_slices.items():
        time_filtered_df = df[df.gap_days <= days_threshold]
        on_loan = time_filtered_df[time_filtered_df.label == "ac"]

        if not on_loan.empty:
            fea[f"cbi_outstanding_max_{time_suffix}"] = on_loan.CREDIT_Outstanding.max()
            fea[f"cbi_outstanding_sum_{time_suffix}"] = on_loan.CREDIT_Outstanding.sum()
            fea[f"cbi_outstanding_mean_{time_suffix}"] = (
                on_loan.CREDIT_Outstanding.mean()
            )
            fea[f"cbi_cur_month_amount_max_{time_suffix}"] = (
                on_loan.CREDIT_LiqCurrentMonth.max()
            )
            fea[f"cbi_cur_month_amount_mean_{time_suffix}"] = (
                on_loan.CREDIT_LiqCurrentMonth.mean()
            )

    # Calculate skewness and kurtosis for specified periods
    for period_suffix, days_threshold in skew_kurt_periods.items():
        if period_suffix == "all":
            time_filtered_df = df
        else:
            time_filtered_df = df[df.gap_days <= days_threshold]

        on_loan = time_filtered_df[time_filtered_df.label == "ac"]

        if (
            not on_loan.empty and len(on_loan) > 1
        ):  # Need at least 2 data points for skewness/kurtosis
            # Outstanding skewness and kurtosis
            fea[f"cbi_outstanding_skewness_{period_suffix}"] = (
                on_loan.CREDIT_Outstanding.skew()
            )
            fea[f"cbi_outstanding_kurtosis_{period_suffix}"] = (
                on_loan.CREDIT_Outstanding.kurtosis()
            )

            # Current month amount skewness and kurtosis
            fea[f"cbi_cur_month_amount_skewness_{period_suffix}"] = (
                on_loan.CREDIT_LiqCurrentMonth.skew()
            )
            fea[f"cbi_cur_month_amount_kurtosis_{period_suffix}"] = (
                on_loan.CREDIT_LiqCurrentMonth.kurtosis()
            )

    # Keep original features for backward compatibility
    on_loan = df[df.label == "ac"]
    if not on_loan.empty:
        fea["cbi_outstanding_max"] = on_loan.CREDIT_Outstanding.max()
        fea["cbi_outstanding_sum"] = on_loan.CREDIT_Outstanding.sum()
        fea["cbi_outstanding_mean"] = on_loan.CREDIT_Outstanding.mean()
        fea["cbi_cur_month_amount_max"] = on_loan.CREDIT_LiqCurrentMonth.max()
        fea["cbi_cur_month_amount_mean"] = on_loan.CREDIT_LiqCurrentMonth.mean()

    return fea


##### 交易


def cbi_credit_transactions_feature(df):
    fea = {}
    on_loan = df[df.label == "ac"]
    cl_loan = df[df.label == "cl"]
    fea["cbi_active_transactions_num"] = on_loan.shape[0]
    fea["cbi_close_transactions_num"] = cl_loan.shape[0]
    fea["cbi_his_transactions_num"] = df.shape[0]
    fea["cbi_active_transactions_ins_num"] = on_loan.CREDIT_Creditor.nunique()
    fea["cbi_close_transactions_ins_num"] = cl_loan.CREDIT_Creditor.nunique()
    fea["cbi_his_transactions_ins_num"] = df.CREDIT_Creditor.nunique()

    return fea


##### 还款


def repayment_list_pre(df):
    pay_list_df = dataframe_explode_list_keys(
        df.reset_index(),
        "CREDIT_PaymentHistoryList",
        ["index", "CREDIT_Creditor", "cur_date"],
    )
    if pay_list_df.empty:
        return pay_list_df
    pay_list_df["CREDIT_YearMonthData_new"] = pd.to_datetime(
        pay_list_df.CREDIT_YearMonthData.str[:4]
        + "20"
        + pay_list_df.CREDIT_YearMonthData.str[-2:],
        format="%b-%Y",
    )
    pay_list_df2 = pay_list_df[~pay_list_df.CREDIT_InterestRate.isnull()]
    pay_list_df2 = pay_list_df2.sort_values("CREDIT_YearMonthData_new", ascending=False)
    pay_list_df2["date_gap_months"] = (
        pay_list_df2["cur_date"].dt.year
        - pay_list_df2["CREDIT_YearMonthData_new"].dt.year
    ) * 12 + (
        pay_list_df2["cur_date"].dt.month
        - pay_list_df2["CREDIT_YearMonthData_new"].dt.month
    )
    pay_amount_list = [
        "CREDIT_Limit",
        "CREDIT_Outstanding",
        "CREDIT_LiqCurrentMonth",
        "CREDIT_ArrearsOnInterest",
        "CREDIT_ArrearsAmmountSum",
    ]
    for p in pay_amount_list:
        pay_list_df2[p] = pay_list_df2[p].apply(
            lambda x: float(x.replace(".", "").replace(",", "."))
        )
    pay_list_df2["next_outstanding"] = (
        pay_list_df2.groupby("index")["CREDIT_Outstanding"].shift(-1).fillna(0)
    )  # 将下一行的 c 值填充为 0
    pay_list_df2["repay_amount"] = (
        pay_list_df2["CREDIT_LiqCurrentMonth"]
        + pay_list_df2["next_outstanding"]
        - pay_list_df2["CREDIT_Outstanding"]
    )
    pay_list_df2["repay_amount_gte0"] = pay_list_df2.repay_amount.apply(
        lambda x: x if x > 0 else 0
    )
    pay_list_df2["cur_loan_outstanding_rate"] = pay_list_df2.apply(
        lambda row: (
            row["CREDIT_LiqCurrentMonth"] / row["next_outstanding"]
            if row["next_outstanding"] != 0
            else np.nan
        ),
        axis=1,
    )
    return pay_list_df2


def cbi_credit_repayment_feature(df):
    fea = {}
    pre_pay_df = repayment_list_pre(df)
    if pre_pay_df.empty:
        return fea
    for month_num in [1, 2, 3, 6, 12, 36]:
        if month_num == "all":
            month_df = pre_pay_df
        else:
            month_df = pre_pay_df[pre_pay_df.date_gap_months <= month_num]
        fea[f"cbi_repayment_amount_max_{month_num}m"] = month_df.repay_amount_gte0.max()
        fea[f"cbi_repayment_amount_sum_{month_num}m"] = month_df.repay_amount_gte0.sum()
        #         if month_df.next_outstanding.sum() > 0:
        #             fea[f'cbi_repayment_rate_{month_num}m'] = round(fea[f'cbi_repayment_amount_sum_{month_num}m']/month_df.next_outstanding.sum(), 6)

        fea[f"cbi_repayment_ins_num_{month_num}m"] = month_df[
            month_df.repay_amount_gte0 > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_cur_loan_outstanding_rate_max_{month_num}m"] = (
            month_df.cur_loan_outstanding_rate.max()
        )
        fea[f"cbi_loan_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].shape[0]
        fea[f"cbi_loan_amount_max_{month_num}m"] = month_df.CREDIT_LiqCurrentMonth.max()
        fea[f"cbi_loan_amount_sum_{month_num}m"] = month_df.CREDIT_LiqCurrentMonth.sum()
        fea[f"cbi_loan_ins_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_loan_num_ins_mean_{month_num}m"] = 0
        if fea[f"cbi_loan_ins_num_{month_num}m"] > 0:
            fea[f"cbi_loan_num_ins_mean_{month_num}m"] = round(
                fea[f"cbi_loan_num_{month_num}m"]
                / fea[f"cbi_loan_ins_num_{month_num}m"],
                6,
            )

    fea["cbi_last_repayment_gay_months"] = month_df[
        month_df.repay_amount_gte0 > 0
    ].date_gap_months.min()
    fea["cbi_last_loan_gay_months"] = month_df[
        month_df.CREDIT_LiqCurrentMonth > 0
    ].date_gap_months.min()

    return fea


def cbi_credit_remarks_repayment_feature(df):
    fea = {}
    df_remarks = df[df["credit_remarks_flag"] == 1].copy()
    pre_pay_df = repayment_list_pre(df_remarks)
    if pre_pay_df.empty:
        return fea
    for month_num in [1, 2, 3, 6, 12, 36]:
        if month_num == "all":
            month_df = pre_pay_df
        else:
            month_df = pre_pay_df[pre_pay_df.date_gap_months <= month_num]
        fea[f"cbi_credit_remarks_repayment_amount_max_{month_num}m"] = (
            month_df.repay_amount_gte0.max()
        )
        fea[f"cbi_credit_remarks_repayment_amount_sum_{month_num}m"] = (
            month_df.repay_amount_gte0.sum()
        )
        #         if month_df.next_outstanding.sum() > 0:
        #             fea[f'cbi_repayment_rate_{month_num}m'] = round(fea[f'cbi_repayment_amount_sum_{month_num}m']/month_df.next_outstanding.sum(), 6)

        fea[f"cbi_credit_remarks_repayment_ins_num_{month_num}m"] = month_df[
            month_df.repay_amount_gte0 > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_credit_remarks_cur_loan_outstanding_rate_max_{month_num}m"] = (
            month_df.cur_loan_outstanding_rate.max()
        )
        fea[f"cbi_credit_remarks_loan_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].shape[0]
        fea[f"cbi_credit_remarks_loan_amount_max_{month_num}m"] = (
            month_df.CREDIT_LiqCurrentMonth.max()
        )
        fea[f"cbi_credit_remarks_loan_amount_sum_{month_num}m"] = (
            month_df.CREDIT_LiqCurrentMonth.sum()
        )
        fea[f"cbi_credit_remarks_loan_ins_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_credit_remarks_loan_num_ins_mean_{month_num}m"] = 0
        if fea[f"cbi_credit_remarks_loan_ins_num_{month_num}m"] > 0:
            fea[f"cbi_credit_remarks_loan_num_ins_mean_{month_num}m"] = round(
                fea[f"cbi_credit_remarks_loan_num_{month_num}m"]
                / fea[f"cbi_credit_remarks_loan_ins_num_{month_num}m"],
                6,
            )

    fea["cbi_credit_remarks_last_repayment_gay_months"] = month_df[
        month_df.repay_amount_gte0 > 0
    ].date_gap_months.min()
    fea["cbi_credit_remarks_last_loan_gay_months"] = month_df[
        month_df.CREDIT_LiqCurrentMonth > 0
    ].date_gap_months.min()

    return fea


def cbi_credit_remarks_aging_feature(df):
    fea = {}
    df_remarks = df[df["credit_remarks_flag"] == 1].copy()
    fea["cbi_credit_remarks_aging_days_max"] = df_remarks.gap_days.max()
    fea["cbi_credit_remarks_aging_days_median"] = df_remarks.gap_days.median()
    fea["cbi_credit_remarks_aging_days_min"] = df_remarks.gap_days.min()
    return fea


def cbi_credit_loan_aging_feature(df):
    fea = {}
    fea["cbi_loan_aging_days_max"] = df.gap_days.max()
    fea["cbi_loan_aging_days_min"] = df.gap_days.min()
    return fea


def cbi_credit_consum_feature(df):
    fea = {}
    fea.update(cbi_credit_credit_feature(df))
    fea.update(cbi_credit_onloan_feature(df))
    fea.update(cbi_credit_transactions_feature(df))
    fea.update(cbi_credit_repayment_feature(df))
    fea.update(cbi_credit_loan_aging_feature(df))
    fea.update(cbi_credit_overdue_feature(df))

    return fea


def cbi_credit_card_credit_feature(df):
    fea = {}
    if df.empty:
        return fea

    for t_type, t_df in {
        "his": df,
        "active": df[df.label == "ac"],
        "close": df[df.label == "cl"],
    }.items():
        if not t_df.empty:
            fea[f"cbi_{t_type}_limit_max"] = t_df.max_limit.max()
            fea[f"cbi_{t_type}_limit_min"] = t_df.max_limit.min()
            fea[f"cbi_{t_type}_limit_mean"] = t_df.max_limit.mean()
            fea[f"cbi_{t_type}_limit_sum"] = t_df.max_limit.sum()

    return fea


#####  还款


def cbi_credit_card_repayment_feature(df):
    fea = {}
    pre_pay_df = repayment_list_pre(df)
    if pre_pay_df.empty:
        return fea
    for month_num in [1, 2, 3, 6, 12, 36]:
        if month_num == "all":
            month_df = pre_pay_df
        else:
            month_df = pre_pay_df[pre_pay_df.date_gap_months <= month_num]
        fea[f"cbi_repayment_amount_max_{month_num}m"] = month_df.repay_amount_gte0.max()
        fea[f"cbi_repayment_amount_sum_{month_num}m"] = month_df.repay_amount_gte0.sum()
        if month_df.next_outstanding.sum() > 0:
            fea[f"cbi_repayment_rate_{month_num}m"] = round(
                fea[f"cbi_repayment_amount_sum_{month_num}m"]
                / month_df.next_outstanding.sum(),
                6,
            )

        fea[f"cbi_repayment_ins_num_{month_num}m"] = month_df[
            month_df.repay_amount_gte0 > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_cur_loan_outstanding_rate_max_{month_num}m"] = (
            month_df.cur_loan_outstanding_rate.max()
        )
        fea[f"cbi_loan_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].shape[0]
        fea[f"cbi_loan_amount_max_{month_num}m"] = month_df.CREDIT_LiqCurrentMonth.max()
        fea[f"cbi_loan_amount_sum_{month_num}m"] = month_df.CREDIT_LiqCurrentMonth.sum()
        fea[f"cbi_loan_ins_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_loan_num_ins_mean_{month_num}m"] = 0
        if fea[f"cbi_loan_ins_num_{month_num}m"] > 0:
            fea[f"cbi_loan_num_ins_mean_{month_num}m"] = round(
                fea[f"cbi_loan_num_{month_num}m"]
                / fea[f"cbi_loan_ins_num_{month_num}m"],
                6,
            )

    fea["cbi_last_repayment_gay_months"] = month_df[
        month_df.repay_amount_gte0 > 0
    ].date_gap_months.min()
    fea["cbi_last_loan_gay_months"] = month_df[
        month_df.CREDIT_LiqCurrentMonth > 0
    ].date_gap_months.min()

    return fea


def cbi_credit_card_feature(df):
    fea = {}
    fea.update(cbi_credit_card_credit_feature(df))
    fea.update(cbi_credit_onloan_feature(df))
    fea.update(cbi_credit_transactions_feature(df))
    fea.update(cbi_credit_card_repayment_feature(df))
    fea.update(cbi_credit_loan_aging_feature(df))
    fea.update(cbi_credit_overdue_feature(df))
    #     fea_result_list.append(fea)
    return fea


def cbi_credit_entity_base_feature(df):
    fea = {}
    fea.update(cbi_credit_entity_credit_feature(df))
    fea.update(cbi_credit_entity_onloan_feature(df))
    fea.update(cbi_credit_entity_transactions_feature(df))
    fea.update(cbi_credit_entity_repayment_feature(df))
    fea.update(cbi_credit_entity_loan_aging_feature(df))
    return fea


##### 额度


def cbi_credit_entity_credit_feature(df):
    fea = {}
    if df.empty:
        return fea

    for t_type, t_df in {
        "his": df,
        "active": df[df.label == "ac"],
        "close": df[df.label == "cl"],
    }.items():
        if not t_df.empty:
            fea[f"cbi_{t_type}_limit_max"] = t_df.max_limit.max()
            fea[f"cbi_{t_type}_limit_min"] = t_df.max_limit.min()
            fea[f"cbi_{t_type}_limit_mean"] = t_df.max_limit.mean()
            fea[f"cbi_{t_type}_limit_sum"] = t_df.max_limit.sum()

    return fea


##### 在贷


def cbi_credit_entity_onloan_feature(df):
    fea = {}
    on_loan = df[df.label == "ac"]
    if on_loan.empty:
        return fea
    fea["cbi_outstanding_max"] = on_loan.CREDIT_Outstanding.max()
    fea["cbi_outstanding_sum"] = on_loan.CREDIT_Outstanding.sum()

    return fea


##### 交易


def cbi_credit_entity_transactions_feature(df):
    fea = {}
    on_loan = df[df.label == "ac"]
    cl_loan = df[df.label == "cl"]
    fea["cbi_active_transactions_num"] = on_loan.shape[0]
    fea["cbi_close_transactions_num"] = cl_loan.shape[0]
    fea["cbi_his_transactions_num"] = df.shape[0]
    fea["cbi_active_transactions_ins_num"] = on_loan.CREDIT_Creditor.nunique()
    fea["cbi_close_transactions_ins_num"] = cl_loan.CREDIT_Creditor.nunique()
    fea["cbi_his_transactions_ins_num"] = df.CREDIT_Creditor.nunique()

    return fea


##### 还款


def repayment_entity_list_pre(df):
    pay_list_df = dataframe_explode_list_keys(
        df.reset_index(),
        "CREDIT_PaymentHistoryList",
        ["index", "CREDIT_Creditor", "cur_date"],
    )
    if pay_list_df.empty:
        return pay_list_df
    pay_list_df["CREDIT_YearMonthData_new"] = pd.to_datetime(
        pay_list_df.CREDIT_YearMonthData.str[:4]
        + "20"
        + pay_list_df.CREDIT_YearMonthData.str[-2:],
        format="%b-%Y",
    )
    pay_list_df2 = pay_list_df[~pay_list_df.CREDIT_InterestRate.isnull()]
    pay_list_df2 = pay_list_df2.sort_values("CREDIT_YearMonthData_new", ascending=False)
    pay_list_df2["date_gap_months"] = (
        pay_list_df2["cur_date"].dt.year
        - pay_list_df2["CREDIT_YearMonthData_new"].dt.year
    ) * 12 + (
        pay_list_df2["cur_date"].dt.month
        - pay_list_df2["CREDIT_YearMonthData_new"].dt.month
    )
    pay_amount_list = ["CREDIT_Limit", "CREDIT_Outstanding", "CREDIT_LiqCurrentMonth"]
    for p in pay_amount_list:
        pay_list_df2[p] = pay_list_df2[p].apply(
            lambda x: float(x.replace(".", "").replace(",", ""))
        )
    pay_list_df2["next_outstanding"] = (
        pay_list_df2.groupby("index")["CREDIT_Outstanding"].shift(-1).fillna(0)
    )  # 将下一行的 c 值填充为 0
    pay_list_df2["repay_amount"] = (
        pay_list_df2["CREDIT_LiqCurrentMonth"]
        + pay_list_df2["next_outstanding"]
        - pay_list_df2["CREDIT_Outstanding"]
    )
    pay_list_df2["repay_amount_gte0"] = pay_list_df2.repay_amount.apply(
        lambda x: x if x > 0 else 0
    )
    return pay_list_df2


def cbi_credit_entity_repayment_feature(df):
    fea = {}
    pre_pay_df = repayment_entity_list_pre(df)
    if pre_pay_df.empty:
        return fea
    for month_num in [1, 2, 3, 6, 12, 36]:
        if month_num == "all":
            month_df = pre_pay_df
        else:
            month_df = pre_pay_df[pre_pay_df.date_gap_months <= month_num]
        fea[f"cbi_repayment_amount_max_{month_num}m"] = month_df.repay_amount_gte0.max()
        fea[f"cbi_repayment_amount_sum_{month_num}m"] = month_df.repay_amount_gte0.sum()
        fea[f"cbi_repayment_ins_num_{month_num}m"] = month_df[
            month_df.repay_amount_gte0 > 0
        ].CREDIT_Creditor.nunique()
        fea[f"cbi_loan_ins_num_{month_num}m"] = month_df[
            month_df.CREDIT_LiqCurrentMonth > 0
        ].CREDIT_Creditor.nunique()

    fea["cbi_last_repayment_gay_months"] = month_df[
        month_df.repay_amount_gte0 > 0
    ].date_gap_months.min()

    return fea


##### 账龄


def cbi_credit_entity_loan_aging_feature(df):
    fea = {}
    fea["cbi_loan_aging_days_max"] = df.gap_days.max()
    fea["cbi_loan_aging_days_min"] = df.gap_days.min()
    return fea


def cbi_credit_car_feature(df):
    fea = {}
    if df.empty:
        return fea

    for t_type, t_df in {
        "cbi_": df,
        "cbi_2_": df[df.car_2_flag == 1],
        "cbi_4_": df[df.car_4_flag == 1],
    }.items():
        if not t_df.empty:
            fea.update(
                replace_dict_keys(cbi_credit_entity_base_feature(t_df), "cbi_", t_type)
            )
    fea.update(cbi_credit_overdue_feature(df))
    return fea


#### 房贷


def cbi_credit_room_feature(df):
    fea = {}
    if df.empty:
        return fea

    for t_type, t_df in {
        "cbi_": df,
        "cbi_21_": df[df.room_21_flag == 1],
        "cbi_21_70_": df[df.room_21_70_flag == 1],
        "cbi_70_": df[df.room_70_flag == 1],
        "cbi_commerce_": df[df.room_commerce_flag == 1],
        "cbi_dwelling_": df[df.room_dwelling_flag == 1],
    }.items():
        if not t_df.empty and t_type == "cbi_":
            fea.update(
                replace_dict_keys(cbi_credit_entity_base_feature(t_df), "cbi_", t_type)
            )
        else:
            fea[f"{t_type}his_transactions_num"] = t_df.shape[0]
    fea.update(cbi_credit_overdue_feature(df))
    return fea


def cbi_credit_enterprises_feature(df):
    fea = {}
    for t_type, t_df in {
        "": df[df.enterprises_flag > 0],
        "mikro_": df[df.enterprises_flag == 1],
        "small_": df[df.enterprises_flag == 2],
        "medium_": df[df.enterprises_flag == 3],
    }.items():
        if not t_df.empty:
            fea.update(
                replace_dict_keys(
                    cbi_credit_easy_feature(t_df), "cbi_", f"cbi_{t_type}"
                )
            )
    fea.update(cbi_credit_overdue_feature(df))

    return fea


# based on enterprise type, time slice, financial institution type, credit status
# prepare dict data
def _prepare_data_for_enterprise_v2_features(df):
    conventional_finance = {
        "bank umum konvensional": "conv_bank",
        "perusahaan pembiayaan": "conv_finco",
        "bpr konvensional": "conv_bpr",
        "perusahaan modal ventura": "conv_vc",
        "lembaga jasa keuangan lainnya": "conv_other",
    }

    syariah_finance = {
        "bank umum syariah / uus": "shariah_bank",
        "perusahaan pembiayaan syariah": "shariah_finco",
        "bpr syariah": "shariah_bpr",
        "perusahaan modal ventura syariah": "shariah_vc",
        "lembaga jasa keuangan lainnya syariah": "shariah_other",
    }

    credit_status_categories = {
        "active": [
            "fasilitas aktif",
        ],
        "non_active": [
            "lunas",
            "lunas dengan diskon",
            "lunas karena pengambilalihan agunan",
            "lunas karena diselesaikan melalui pengadilan",
            "dihapusbukukan",
            "dialihkan atau dijual kepada pihak lain non-pelapor",
            "disekuritisasi (kreditur asal sebagai servicer)",
            "kredit atau pembiayaan alihan dengan pengelolaan penagihan",
            "dialihkan ke fasilitas lain",
            "dialihkan atau dijual ke pelapor lain",
            "hapus tagih",
            "dibatalkan",
            "diblokir sementara",
        ],
    }

    df = df.copy()

    df["creditor_category_lower"] = (
        df["CREDIT_CreditorCategory"].str.lower().str.strip().fillna("")
    )
    df["credit_condition_lower"] = (
        df["CREDIT_Condition"].str.lower().str.strip().fillna("")
    )

    # Create credit status category mapping using pandas operations
    df["credit_status_category"] = "other"  # default value
    for category, conditions in credit_status_categories.items():
        df.loc[
            df["credit_condition_lower"].isin(conditions), "credit_status_category"
        ] = category

    return df, conventional_finance, syariah_finance


# basic enterprise features
def _generate_basic_enterprise_v2_features(time_filtered_df, time_suffix):
    fea = {}

    for t_type, t_df in {
        "": time_filtered_df[time_filtered_df["enterprises_flag"] > 0],
        "mikro_": time_filtered_df[time_filtered_df["enterprises_flag"] == 1],
        "small_": time_filtered_df[time_filtered_df["enterprises_flag"] == 2],
        "medium_": time_filtered_df[time_filtered_df["enterprises_flag"] == 3],
    }.items():
        if not t_df.empty:
            base_features = cbi_credit_easy_feature(t_df)
            for key, value in base_features.items():
                new_key = f"{key.replace('cbi_', f'cbi_{t_type}')}_{time_suffix}"
                fea[new_key] = value

    return fea


# basic credit status features
def _generate_credit_status_features(time_filtered_df, time_suffix):
    fea = {}

    if "credit_status_category" not in time_filtered_df.columns:
        return fea

    for status_category in ["active", "non_active"]:
        status_filtered_df = time_filtered_df[
            time_filtered_df["credit_status_category"] == status_category
        ]

        if not status_filtered_df.empty:
            for t_type, t_df in {
                "": status_filtered_df[status_filtered_df["enterprises_flag"] > 0],
                "mikro_": status_filtered_df[
                    status_filtered_df["enterprises_flag"] == 1
                ],
                "small_": status_filtered_df[
                    status_filtered_df["enterprises_flag"] == 2
                ],
                "medium_": status_filtered_df[
                    status_filtered_df["enterprises_flag"] == 3
                ],
            }.items():
                if not t_df.empty:
                    base_features = cbi_credit_easy_feature(t_df)
                    for key, value in base_features.items():
                        new_key = f"{key.replace('cbi_', f'cbi_{status_category}_{t_type}')}_{time_suffix}"
                        fea[new_key] = value

    return fea


def _generate_finance_institution_features(
    time_filtered_df,
    time_suffix,
    conventional_finance,
    syariah_finance,
):
    fea = {}

    if "creditor_category_lower" not in time_filtered_df.columns:
        return fea

    # 1. financial institution features (not by credit status)
    for finance_group, finance_dict in [
        ("conventional_finance", conventional_finance),
        ("syariah_finance", syariah_finance),
    ]:
        finance_filtered_df = time_filtered_df[
            time_filtered_df["creditor_category_lower"].isin(finance_dict.keys())
        ]

        if not finance_filtered_df.empty:
            for t_type, t_df in {
                "": finance_filtered_df[finance_filtered_df.enterprises_flag > 0],
                "mikro_": finance_filtered_df[
                    finance_filtered_df.enterprises_flag == 1
                ],
                "small_": finance_filtered_df[
                    finance_filtered_df.enterprises_flag == 2
                ],
                "medium_": finance_filtered_df[
                    finance_filtered_df.enterprises_flag == 3
                ],
            }.items():
                if not t_df.empty:
                    base_features = cbi_credit_easy_feature(t_df)
                    for key, value in base_features.items():
                        new_key = f"{key.replace('cbi_', f'cbi_{finance_group}_{t_type}')}_{time_suffix}"
                        fea[new_key] = value

    # 2. financial institution features (by credit status)
    if "credit_status_category" in time_filtered_df.columns:
        for finance_group, finance_dict in [
            ("conventional_finance", conventional_finance),
            ("syariah_finance", syariah_finance),
        ]:
            for status_category in ["active", "non_active"]:
                finance_status_filtered_df = time_filtered_df[
                    (
                        time_filtered_df["creditor_category_lower"].isin(
                            finance_dict.keys()
                        )
                    )
                    & (time_filtered_df["credit_status_category"] == status_category)
                ]

                if not finance_status_filtered_df.empty:
                    for t_type, t_df in {
                        "": finance_status_filtered_df[
                            finance_status_filtered_df.enterprises_flag > 0
                        ],
                        "mikro_": finance_status_filtered_df[
                            finance_status_filtered_df.enterprises_flag == 1
                        ],
                        "small_": finance_status_filtered_df[
                            finance_status_filtered_df.enterprises_flag == 2
                        ],
                        "medium_": finance_status_filtered_df[
                            finance_status_filtered_df.enterprises_flag == 3
                        ],
                    }.items():
                        if not t_df.empty:
                            base_features = cbi_credit_easy_feature(t_df)
                            for key, value in base_features.items():
                                new_key = f"{key.replace('cbi_', f'cbi_{finance_group}_{status_category}_{t_type}')}_{time_suffix}"
                                fea[new_key] = value

    return fea


# combined all features
def cbi_credit_enterprises_v2_feature(df):
    fea = {}
    time_slices = {"6m": 183, "12m": 365, "24m": 730}

    df, conventional_finance, syariah_finance = (
        _prepare_data_for_enterprise_v2_features(df)
    )

    for time_suffix, days_threshold in time_slices.items():
        time_filtered_df = df[df.gap_days <= days_threshold]

        if not time_filtered_df.empty:
            basic_features = _generate_basic_enterprise_v2_features(
                time_filtered_df, time_suffix
            )
            fea.update(basic_features)

            credit_status_features = _generate_credit_status_features(
                time_filtered_df, time_suffix
            )
            fea.update(credit_status_features)

            finance_features = _generate_finance_institution_features(
                time_filtered_df,
                time_suffix,
                conventional_finance,
                syariah_finance,
            )
            fea.update(finance_features)

    return fea


def cbi_credit_easy_feature(df):
    fea = {}
    fea[f"cbi_loan_num"] = df.shape[0]
    fea[f"cbi_limit_max"] = df.max_limit.max()
    fea[f"cbi_limit_sum"] = df.max_limit.sum()
    fea[f"cbi_ins_num"] = df.CREDIT_Creditor.nunique()
    return fea


def collateral_list_pre(df):
    coll_room_list = [
        "tanah",
        "gedung/ruang kantor",
        "gudang",
        "rumah toko/rumah kantor",
        "hotel",
        "properti komersial lainnya",
        "rumah",
        "apartemen/rumah susun",
        "rumah tinggal",
        "gedung",
    ]
    coll_car_list = [
        "kendaraan",
        "kendaraan bermotor",
        "pesawat udara",
        "kapal laut/transportasi air",
    ]
    coll_sukuk_list = [
        "sukuk ritel",
        "surat berharga lainnya",
        "surat perbendaharaan negara syariah",
        "sukuk bank indonesia",
        "surat perbendaharaan negara (spn)",
        "sukuk lainnya",
        "obligasi negara (on)",
        "obligasi ritel indonesia (ori)",
        "obligasi daerah",
        "sukuk negara",
        "ijarah fixed rate",
    ]

    coll_list_df = dataframe_explode_list_keys(
        df.reset_index(),
        "CREDIT_CollateralOnFacilityList",
        ["index", "CREDIT_Creditor", "cur_date", "max_limit"],
    )
    if not coll_list_df.empty:
        coll_list_df["CREDIT_CollateralType"] = (
            coll_list_df["CREDIT_CollateralType"].str.strip().str.lower()
        )
        coll_list_df["coll_flag"] = np.where(
            coll_list_df.CREDIT_CollateralType.isin(coll_room_list),
            1,
            np.where(
                coll_list_df.CREDIT_CollateralType.isin(coll_car_list),
                2,
                np.where(
                    coll_list_df.CREDIT_CollateralType.isin(coll_sukuk_list), 3, 4
                ),
            ),
        )
        max_b_rows = coll_list_df.loc[
            coll_list_df.groupby("index")["coll_flag"].idxmin()
        ]
        return max_b_rows
    return pd.DataFrame()


def cbi_credit_collateral_feature(df):
    fea = {}

    coll_df = collateral_list_pre(df[df.CollateralOnFacility_flag == 1])
    if not coll_df.empty:
        for t_type, t_df in {
            "": coll_df,
            "room_": coll_df[coll_df.coll_flag == 1],
            "car_": coll_df[coll_df.coll_flag == 2],
            "sukuk_": coll_df[coll_df.coll_flag == 3],
            "other_": coll_df[coll_df.coll_flag == 4],
        }.items():
            if not t_df.empty:
                fea.update(
                    replace_dict_keys(
                        cbi_credit_easy_feature(t_df), "cbi_", f"cbi_{t_type}"
                    )
                )

    return fea


def ratio_fun(a, b):
    if b == 0:
        return np.nan
    else:
        return round(a / b, 6)


def cbi_credit_overdue_feature(df):
    fea = {}
    time_slices = {"1m": 30, "2m": 60, "3m": 90, "6m": 183, "12m": 365, "24m": 730}

    # Generate features for each time slice
    for time_suffix, days_threshold in time_slices.items():
        time_filtered_df = df[df.gap_days <= days_threshold]

        if not time_filtered_df.empty:
            # Current day overdue features
            fea[f"cbi_overdue_cur_day_max_{time_suffix}"] = (
                time_filtered_df.CREDIT_DayPastDue.max()
            )
            fea[f"cbi_overdue_cur_day_adjust_max_{time_suffix}"] = (
                time_filtered_df.CREDIT_DayPastDue_adjust.max()
            )
            fea[f"cbi_overdue_cur_amount_max_{time_suffix}"] = (
                time_filtered_df.CREDIT_ArrearsOnPrincipal.max()
            )
            fea[f"cbi_overdue_cur_amount_sum_{time_suffix}"] = (
                time_filtered_df.CREDIT_ArrearsOnPrincipal.sum()
            )

            # Historical overdue features
            fea[f"cbi_overdue_his_day_max_{time_suffix}"] = (
                time_filtered_df.CREDIT_FacPerf_LongestArrearsDays.max()
            )
            fea[f"cbi_overdue_his_amount_max_{time_suffix}"] = (
                time_filtered_df.CREDIT_FacPerf_MaxArrearsAmount.max()
            )

            # Current loan count features
            fea[f"cbi_overdue_cur_loan_cnt_{time_suffix}"] = time_filtered_df[
                time_filtered_df.CREDIT_ArrearsOnPrincipal > 0
            ].shape[0]
            fea[f"cbi_overdue_cur_loan_cnt_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_cur_loan_cnt_{time_suffix}"],
                time_filtered_df[time_filtered_df.CREDIT_FacStatus == "Aktif"].shape[0],
            )
            fea[f"cbi_overdue_cur_loan_cnt_all_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_cur_loan_cnt_{time_suffix}"],
                time_filtered_df.shape[0],
            )

            # Historical loan count features
            fea[f"cbi_overdue_his_loan_cnt_{time_suffix}"] = time_filtered_df[
                time_filtered_df.CREDIT_FacPerf_MaxArrearsAmount > 0
            ].shape[0]
            fea[f"cbi_overdue_his_loan_cnt_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_his_loan_cnt_{time_suffix}"],
                time_filtered_df.shape[0],
            )

            # Current institution count features
            fea[f"cbi_overdue_cur_ins_cnt_{time_suffix}"] = time_filtered_df[
                time_filtered_df.CREDIT_ArrearsOnPrincipal > 0
            ].CREDIT_Creditor.nunique()
            fea[f"cbi_overdue_cur_ins_cnt_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_cur_ins_cnt_{time_suffix}"],
                time_filtered_df[
                    time_filtered_df.CREDIT_FacStatus == "Aktif"
                ].CREDIT_Creditor.nunique(),
            )
            fea[f"cbi_overdue_cur_ins_cnt_all_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_cur_ins_cnt_{time_suffix}"],
                time_filtered_df.CREDIT_Creditor.nunique(),
            )

            # Historical institution count features
            fea[f"cbi_overdue_his_ins_cnt_{time_suffix}"] = time_filtered_df[
                time_filtered_df.CREDIT_FacPerf_MaxArrearsAmount > 0
            ].CREDIT_Creditor.nunique()
            fea[f"cbi_overdue_his_ins_cnt_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_overdue_his_ins_cnt_{time_suffix}"],
                time_filtered_df.CREDIT_Creditor.nunique(),
            )

            fea[f"cbi_credit_remarks_cnt_{time_suffix}"] = (
                time_filtered_df.credit_remarks_flag.sum()
            )
            fea[f"cbi_credit_remarks_cnt_rate_{time_suffix}"] = ratio_fun(
                fea[f"cbi_credit_remarks_cnt_{time_suffix}"],
                time_filtered_df.shape[0],
            )

    # Keep original features for backward compatibility
    fea["cbi_overdue_cur_day_max"] = df.CREDIT_DayPastDue.max()
    fea["cbi_overdue_cur_day_adjust_max"] = df.CREDIT_DayPastDue_adjust.max()
    fea["cbi_overdue_his_day_max"] = df.CREDIT_FacPerf_LongestArrearsDays.max()
    fea["cbi_overdue_cur_amount_max"] = df.CREDIT_ArrearsOnPrincipal.max()
    fea["cbi_overdue_his_amount_max"] = df.CREDIT_FacPerf_MaxArrearsAmount.max()
    fea["cbi_overdue_cur_amount_sum"] = df.CREDIT_ArrearsOnPrincipal.sum()

    fea["cbi_overdue_cur_loan_cnt"] = df[df.CREDIT_ArrearsOnPrincipal > 0].shape[0]
    fea["cbi_overdue_cur_loan_cnt_rate"] = ratio_fun(
        fea["cbi_overdue_cur_loan_cnt"], df[df.CREDIT_FacStatus == "Aktif"].shape[0]
    )
    fea["cbi_overdue_cur_loan_cnt_all_rate"] = ratio_fun(
        fea["cbi_overdue_cur_loan_cnt"], df.shape[0]
    )

    fea["cbi_overdue_his_loan_cnt"] = df[df.CREDIT_FacPerf_MaxArrearsAmount > 0].shape[
        0
    ]
    fea["cbi_overdue_his_loan_cnt_rate"] = ratio_fun(
        fea["cbi_overdue_his_loan_cnt"], df.shape[0]
    )

    fea["cbi_overdue_cur_ins_cnt"] = df[
        df.CREDIT_ArrearsOnPrincipal > 0
    ].CREDIT_Creditor.nunique()
    fea["cbi_overdue_cur_ins_cnt_rate"] = ratio_fun(
        fea["cbi_overdue_cur_ins_cnt"],
        df[df.CREDIT_FacStatus == "Aktif"].CREDIT_Creditor.nunique(),
    )
    fea["cbi_overdue_cur_ins_cnt_all_rate"] = ratio_fun(
        fea["cbi_overdue_cur_ins_cnt"], df.CREDIT_Creditor.nunique()
    )

    fea["cbi_overdue_his_ins_cnt"] = df[
        df.CREDIT_FacPerf_MaxArrearsAmount > 0
    ].CREDIT_Creditor.nunique()
    fea["cbi_overdue_his_ins_cnt_rate"] = ratio_fun(
        fea["cbi_overdue_his_ins_cnt"], df.CREDIT_Creditor.nunique()
    )

    fea["cbi_credit_remarks_cnt"] = df.credit_remarks_flag.sum()
    fea["cbi_credit_remarks_cnt_rate"] = ratio_fun(
        fea["cbi_credit_remarks_cnt"], df.shape[0]
    )

    return fea


inq_foot_columns = [
    "INQSTC_InquiryTtlSum",
    "INQSTC_InquiryMonth1Sum",
    "INQSTC_InquiryMonth2Sum",
    "INQSTC_InquiryMonth3Sum",
    "INQSTC_InquiryMonth4Sum",
    "INQSTC_InquiryMonth5Sum",
    "INQSTC_InquiryMonth6Sum",
    "INQSTC_InquiryMonth7Sum",
    "INQSTC_InquiryMonth8Sum",
    "INQSTC_InquiryMonth9Sum",
    "INQSTC_InquiryMonth10Sum",
    "INQSTC_InquiryMonth11Sum",
    "INQSTC_InquiryMonth12Sum",
]

inq_columns = [
    "INQSTC_InquiryTtl",
    "INQSTC_InquiryMonth1",
    "INQSTC_InquiryMonth2",
    "INQSTC_InquiryMonth3",
    "INQSTC_InquiryMonth4",
    "INQSTC_InquiryMonth5",
    "INQSTC_InquiryMonth6",
    "INQSTC_InquiryMonth7",
    "INQSTC_InquiryMonth8",
    "INQSTC_InquiryMonth9",
    "INQSTC_InquiryMonth10",
    "INQSTC_InquiryMonth11",
    "INQSTC_InquiryMonth12",
]


def cbi_inq_num_fun(b_df, month):
    c_list = [f"INQSTC_InquiryMonth{i}Sum" for i in range(1, month + 1)]
    return b_df[c_list].sum().sum()


def cbi_inq_max_fun(b_df, month):
    c_list = [f"INQSTC_InquiryMonth{i}Sum" for i in range(1, month + 1)]
    return b_df[c_list].max().max()


def cbi_inq_skewness_fun(b_df, month):
    """Calculate skewness for inquiry data over specified months."""
    c_list = [f"INQSTC_InquiryMonth{i}Sum" for i in range(1, month + 1)]
    values = b_df[c_list].values.flatten()

    # Convert to pandas Series and calculate skewness
    # pandas will automatically handle NaN values and return NaN for insufficient data
    series = pd.Series(values)
    return series.skew()


def cbi_inq_kurtosis_fun(b_df, month):
    """Calculate kurtosis for inquiry data over specified months."""
    c_list = [f"INQSTC_InquiryMonth{i}Sum" for i in range(1, month + 1)]
    values = b_df[c_list].values.flatten()

    # Convert to pandas Series and calculate kurtosis (excess kurtosis)
    # pandas will automatically handle NaN values and return NaN for insufficient data
    series = pd.Series(values)
    return series.kurtosis()


inq_reason_map = {
    "LK - Pemenuhan Ketentuan OJK atau Pihak Berwenang Lain": "1",
    "LK - Pengelolaan SDM": "2",
    "Non LK - Pemenuhan Peraturan Perundang-undangan": "3",
    "Penyediaan Fasilitas baru": "4",
    "Monitoring Debitur": "5",
    "Manajemen Risiko": "6",
    "Pemenuhan Peraturan dan Perundangan": "7",
    "Layanan Masyarakat": "8",
    "LK - Proses Pemberian Fasilitas Penyediaan Dana": "9",
    "Pihak Lain - Pelaksanaan fungsi dan tugas sesuai peraturan perundang-undangan ": "10",
    "LK - Menerapkan manajemen risiko kredit atau pembiayaan": "11",
    "LK - Manajemen Resiko Kredit - Pelaksanaan Audit": "12",
    "LK - Manajemen Resiko Kredit - Anti Fraud": "13",
    "Non LK - Mendukung kegiatan operasional NonLK yang berkaitan dengan proses identifikasi integritas pelanggan dari sisi resiko kredit": "14",
    "Non LK - Seleksi calon pegawai, rekanan, agen, pedagang, dan/atau vendor nonLK": "15",
    "LK - Verifikasi Kerjasama LK dengan Pihak ke 3": "16",
}


def cbi_inq_feature(base_df):
    fea = {}
    inq_df = pd.json_normalize(
        base_df["result"].apply(lambda x: x["InquiryDetail"]["INQ_Statistic"])
    )

    inq_footer_df = dataframe_explode_list(inq_df, "INQSTC_InformationFooter")
    for i in inq_foot_columns:
        inq_footer_df[i] = inq_footer_df[i].astype(int)

    # Extract data for Jumlah Inquiry and Jumlah Institusi yang Melakukan Inquiry
    jumlah_inquiry_df = inq_footer_df[
        inq_footer_df.INQSTC_InquiryPurposeSum == "Jumlah Inquiry"
    ]
    jumlah_institusi_df = inq_footer_df[
        inq_footer_df.INQSTC_InquiryPurposeSum
        == "Jumlah Institusi yang Melakukan Inquiry"
    ]

    # Original features
    for m in [1, 2, 3, 6, 12]:
        fea[f"cbi_inq_cnt_sum_{m}m"] = cbi_inq_num_fun(jumlah_inquiry_df, m)
        fea[f"cbi_inq_ins_cnt_max_{m}m"] = cbi_inq_max_fun(jumlah_institusi_df, m)

    # New features: skewness and kurtosis for 6 and 12 months
    fea["cbi_inq_cnt_skewness_6m"] = cbi_inq_skewness_fun(jumlah_inquiry_df, 6)
    fea["cbi_inq_cnt_kurtosis_6m"] = cbi_inq_kurtosis_fun(jumlah_inquiry_df, 6)
    fea["cbi_inq_ins_cnt_skewness_6m"] = cbi_inq_skewness_fun(jumlah_institusi_df, 6)
    fea["cbi_inq_ins_cnt_kurtosis_6m"] = cbi_inq_kurtosis_fun(jumlah_institusi_df, 6)

    fea["cbi_inq_cnt_skewness_12m"] = cbi_inq_skewness_fun(jumlah_inquiry_df, 12)
    fea["cbi_inq_cnt_kurtosis_12m"] = cbi_inq_kurtosis_fun(jumlah_inquiry_df, 12)
    fea["cbi_inq_ins_cnt_skewness_12m"] = cbi_inq_skewness_fun(jumlah_institusi_df, 12)
    fea["cbi_inq_ins_cnt_kurtosis_12m"] = cbi_inq_kurtosis_fun(jumlah_institusi_df, 12)

    return fea


def process_column(series):
    def deduplicate_and_filter(lst):
        if not isinstance(lst, list):
            return lst
        # 去重并过滤空字符串
        unique_values = list(set(lst))
        filtered_values = [v for v in unique_values if v.strip() != ""]
        return json.dumps(filtered_values) if len(filtered_values) > 0 else np.nan

    return series.apply(deduplicate_and_filter)


# 计算年龄
def calculate_age(birth_date, current_date):
    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def addr_contact_pre(addr_contacts_df):
    addr_contacts_df2 = dataframe_explode_list(
        addr_contacts_df, "INDID_AddresAndContactHistoryList"
    )
    if not addr_contacts_df2.empty:
        result_dict = {}
        for _, row in addr_contacts_df2.iterrows():
            types = row["INDID_TypeOfData"].split("|")
            values = row["INDID_Data"].split("|")

            # 确保键值对数量一致
            if len(types) != len(values):
                continue

            # 获取当前 account_id 的字典
            current_dict = result_dict.get("account_id", {})

            # 更新键值对
            for t, v in zip(types, values):
                if t in current_dict:
                    # 如果已经是列表，直接追加；否则转换为列表
                    if isinstance(current_dict[t], list):
                        current_dict[t].append(v)
                    else:
                        current_dict[t] = [current_dict[t], v]
                else:
                    current_dict[t] = [v]

            # 更新 result_dict
            result_dict["account_id"] = current_dict
        new_df = pd.DataFrame.from_dict(result_dict, orient="index")
        new_df = new_df.apply(process_column)
        return new_df
    else:
        return pd.DataFrame()


def cbi_basic_identity(base_df):
    fea = {}

    report_info = base_df["result"].to_list()[0]
    personal = (
        report_info.get("IndividualIdentitySubject", {})
        .get("INDID_Information", {})
        .get("INDID_Personal", {})
    )
    addr_contact = (
        report_info.get("IndividualIdentitySubject", {})
        .get("INDID_Information", {})
        .get("INDID_AddresAndContact", {})
        .get("INDID_AddressAsIdentity", {})
    )
    employment = (
        report_info.get("IndividualIdentitySubject", {})
        .get("INDID_Information", {})
        .get("INDID_EmploymentInfo", {})
    )

    if personal:
        fea["cbi_gender"] = personal["INDID_Gender"]
        fea["cbi_birth"] = personal["INDID_DateOfBirth"]
        if fea["cbi_birth"]:
            birth_date = datetime.datetime.strptime(fea["cbi_birth"], "%Y-%m-%d")
            current_date = CURRENT_DATE_TIME.date()
            fea["cbi_age"] = calculate_age(birth_date, current_date)
        fea["cbi_marital_status"] = personal["INDID_MaritalStatus"]
        fea["cbi_education"] = (
            int(personal["INDID_EducationLevel"])
            if personal["INDID_EducationLevel"]
            and personal["INDID_EducationLevel"].isdigit()
            else np.nan
        )
        fea["cbi_gender"] = personal["INDID_Gender"]
    if addr_contact:
        fea["cbi_cur_phone_number"] = addr_contact["INDID_PhoneNumber"]
        fea["cbi_cur_cellular_number"] = addr_contact["INDID_CellularNumber"]
        fea["cbi_cur_email"] = addr_contact["INDID_Email"]
    if employment:
        fea["cbi_employment"] = (
            int(employment["INDID_Employment"])
            if employment["INDID_Employment"]
            and employment["INDID_Employment"].isdigit()
            else np.nan
        )
        fea["cbi_employment_desc"] = employment["INDID_EmploymentDesc"]
    addr_contacts_df = pd.json_normalize(
        base_df["result"].apply(
            lambda x: x["IndividualIdentitySubject"]["INDID_HistoricalInformation"][
                "INDID_AddresAndContactHistory"
            ]
        )
    )
    addr_contact_his_df = addr_contact_pre(addr_contacts_df)
    if not addr_contact_his_df.empty:
        addr_contact_his_dict = addr_contact_his_df.to_dict("records")[0]
        fea["cbi_his_phone_number_list"] = addr_contact_his_dict.get(
            "Nomor Telepon Seluler", np.nan
        )
        fea["cbi_his_cellular_number_list"] = addr_contact_his_dict.get(
            "Nomor Telepon", np.nan
        )
        fea["cbi_his_email_list"] = addr_contact_his_dict.get("E-mail", np.nan)
    return fea


def dataframe_explode_list(df, exp_col):
    df_explode = df[exp_col].explode().rename(exp_col).reset_index()
    df_explode = pd.json_normalize(df_explode[exp_col])
    df_explode.columns = [i.split(".")[-1] for i in df_explode.columns]
    # 删除NAN信息数据
    df_explode = df_explode.dropna(how="all")
    return df_explode


def dataframe_explode_list_keys(df, exp_col, primary_key_list=[]):
    df_explode = df[primary_key_list + [exp_col]].explode(exp_col)
    # 删除NAN信息数据
    df_explode = df_explode[df_explode[exp_col].notnull()]
    df_explode = df_explode.reset_index(drop=True)
    # json打平成N维列信息
    df_explode_new = pd.json_normalize(df_explode[exp_col])
    df_explode_new.columns = [i.split(".")[-1] for i in df_explode_new.columns]
    # 合并用户ID
    df_explode = pd.concat([df_explode[primary_key_list], df_explode_new], axis=1)
    ## 删除NAN信息数据
    # df_explode = df_explode.dropna(how='all')
    return df_explode


credit_remarks_mapping = {
    # 主流竞品（有些可以看看是不是拿出来，比如paylater）
    "paylater": "paylater",
    "dana": "dana_tunai",
    "akulaku": "akulaku",
    "kredivo": "kredivo",
    "easycash": "easycash",
    "adapundi": "adapundi",
    "adakami": "adakami",
    "julo": "julo",
    "indodana": "indodana",
    "atome": "atome",
    "commerce finance": "commerce_finance",
    "kredifazz": "kredifazz",
    "finaccel": "finaccel",
    "amartha": "amartha",
    "uangme": "uangme",
    # 其他金融服务商
    "lentera dana": "lentera_dana_nusantara",
    "kredit pintar": "kredit_pintar",
    "mapan": "mapan_global_reksa",
    "pembiayaan digital": "pembiayaan_digital_indonesia",
    "indonesia fintopia": "indonesia_fintopia_technology",
    "info tekno siaga": "info_tekno_siaga",
    "pintar inovasi": "pintar_inovasi_digital",
    "multifinance anak bangsa": "multifinance_anak_bangsa",
    "home credit": "home_credit_indonesia",
    "cepat": "rupiah_cepat",
    "danarupiah": "danarupiah",
    "asetku": "asetku",
    # 印尼当地信贷集团相关
    "mega central": "mega_central_finance",
    "mega finance": "mega_finance",
    "mega auto": "mega_auto_finance",
    "mandiri utama": "mandiri_utama_finance",
    "mandiri tunas": "mandiri_tunas_finance",
    # 其他else (后面可以单独拿出来)
    "covid": "covid19_related",
    "lunas": "paid_off",
    "hapus buku": "written_off",
    "dijual": "sold_to_collector",
    "joint finance": "joint_financing",
    "channeling": "channeling_product",
    "migrasi": "system_migration",
    "cc_": "credit_card",
}


def cbi_credit_pre(df_cbi_all):
    credit_df = pd.json_normalize(
        df_cbi_all["result"].apply(lambda x: x["CreditFacilityDetail"])
    )

    credit_ac_df = dataframe_explode_list(
        credit_df, "CREDIT_ActiveFacility_AsDebtor.CREDIT_ActiveFacility_AsDebtorList"
    )
    credit_cl_df = dataframe_explode_list(
        credit_df, "CREDIT_ClosedFacility_AsDebtor.CREDIT_ClosedFacility_AsDebtorList"
    )
    credit_ac_df["label"] = "ac"
    credit_cl_df["label"] = "cl"
    credit_all_df = pd.concat([credit_ac_df, credit_cl_df], ignore_index=True, axis=0)
    if credit_all_df.empty:
        return pd.DataFrame()
    credit_all_res_df = credit_all_df[
        ~credit_all_df.CREDIT_Condition.isin(pop_condition)
    ].copy()
    if credit_all_res_df.empty:
        return pd.DataFrame()

    credit_all_res_df["cur_date"] = CURRENT_DATE_TIME
    credit_all_res_df["CREDIT_InitialLimit"] = credit_all_res_df[
        "CREDIT_InitialLimit"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    credit_all_res_df["CREDIT_Limit"] = credit_all_res_df["CREDIT_Limit"].apply(
        lambda x: float(x.replace(".", "").replace(",", "."))
    )
    credit_all_res_df["CREDIT_LiqCurrentMonth"] = credit_all_res_df[
        "CREDIT_LiqCurrentMonth"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    credit_all_res_df["CREDIT_Outstanding"] = credit_all_res_df[
        "CREDIT_Outstanding"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    credit_all_res_df["CREDIT_ArrearsOnPrincipal"] = credit_all_res_df[
        "CREDIT_ArrearsOnPrincipal"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    credit_all_res_df["CREDIT_ArrearsOnInterest"] = credit_all_res_df[
        "CREDIT_ArrearsOnInterest"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    credit_all_res_df["CREDIT_FacPerf_MaxArrearsAmount"] = credit_all_res_df[
        "CREDIT_FacPerf_MaxArrearsAmount"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))

    credit_all_res_df["CREDIT_FacPerf_LongestArrearsDays"] = credit_all_res_df[
        "CREDIT_FacPerf_LongestArrearsDays"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))

    credit_all_res_df["CREDIT_DayPastDue"] = credit_all_res_df[
        "CREDIT_DayPastDue"
    ].apply(lambda x: float(x.replace(".", "").replace(",", ".")))

    credit_all_res_df["credit_remarks_flag"] = np.where(
        credit_all_res_df["CREDIT_Remarks"].isna()
        | (credit_all_res_df["CREDIT_Remarks"].str.strip() == ""),
        0,
        1,
    )
    credit_all_res_df["CREDIT_DayPastDue_adjust"] = np.where(
        credit_all_res_df["credit_remarks_flag"] == 1,
        credit_all_res_df["CREDIT_FacPerf_LongestArrearsDays"],
        credit_all_res_df["CREDIT_DayPastDue"],
    )

    date_columns = [
        "CREDIT_InitialContractDate",
        "CREDIT_LastContractDate",
        "CREDIT_InitialCreditDate",
        "CREDIT_CreditStartDate",
    ]
    for d in date_columns:
        credit_all_res_df[f"{d}_new"] = pd.to_datetime(
            credit_all_res_df[d], format="%d %b %Y"
        )

    credit_all_res_df["max_limit"] = credit_all_res_df[
        ["CREDIT_InitialLimit", "CREDIT_Limit"]
    ].max(axis=1)
    df_cleaned = credit_all_res_df.dropna(subset=["CREDIT_CreditStartDate_new"]).copy()
    df_cleaned["gap_days"] = (
        df_cleaned.cur_date - df_cleaned.CREDIT_CreditStartDate_new
    ).dt.days
    df_cleaned["GuarantorOnFacility_flag"] = np.where(
        df_cleaned.CREDIT_GuarantorOnFacilityList.str.len() > 0, 1, 0
    )
    df_cleaned["CollateralOnFacility_flag"] = np.where(
        df_cleaned.CREDIT_CollateralOnFacilityList.str.len() > 0, 1, 0
    )
    df_cleaned["credit_card_flag"] = np.where(
        df_cleaned.CREDIT_CreditType.isin(credit_card_type), 1, 0
    )
    df_cleaned["room_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_type), 1, 0
    )
    df_cleaned["car_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(car_type), 1, 0
    )
    df_cleaned["car_2_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(car_2), 1, 0
    )
    df_cleaned["car_4_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(car_4), 1, 0
    )

    df_cleaned["room_21_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_21), 1, 0
    )
    df_cleaned["room_21_70_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_21_70), 1, 0
    )
    df_cleaned["room_70_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_70), 1, 0
    )
    df_cleaned["room_commerce_flag"] = np.where(
        df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_commerce), 1, 0
    )
    df_cleaned["room_dwelling_flag"] = np.where(
        (~df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_commerce))
        & (df_cleaned.CREDIT_EconomicSector.str.lower().isin(room_type)),
        1,
        0,
    )

    df_cleaned["enterprises_flag"] = np.where(
        df_cleaned.CREDIT_DebtorCategory.str.lower().isin(mikro_enterprises),
        1,
        np.where(
            df_cleaned.CREDIT_DebtorCategory.str.lower().isin(small_enterprises),
            2,
            np.where(
                df_cleaned.CREDIT_DebtorCategory.str.lower().isin(medium_enterprises),
                3,
                0,
            ),
        ),
    )

    processed_remarks = (
        df_cleaned["CREDIT_Remarks"].fillna("").astype(str).str.strip().str.lower()
    )

    for keyword, flag_name in credit_remarks_mapping.items():
        flag_column = f"{flag_name}_flag"

        contains_keyword = processed_remarks.str.contains(keyword, case=False, na=False)
        df_cleaned[flag_column] = np.where(
            df_cleaned["credit_remarks_flag"] == 1,
            contains_keyword.astype(int),
            np.nan,
        )

    return df_cleaned


def cbi_credit_remarks_feature(df):
    fea = {}
    time_slices = {"6m": 183, "12m": 365, "24m": 730}  # 从目前的IV来看，切三片就够了

    for time_suffix, days_threshold in time_slices.items():
        time_filtered_df = df[df.gap_days <= days_threshold]

        if not time_filtered_df.empty:
            total_records = time_filtered_df.shape[0]
            records_with_remarks = time_filtered_df["credit_remarks_flag"].sum()

            for keyword, flag_name in credit_remarks_mapping.items():
                flag_column = f"{flag_name}_flag"

                if flag_column in time_filtered_df.columns:
                    # cnt
                    fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_{time_suffix}"] = (
                        time_filtered_df[flag_column].sum()
                    )

                    fea[
                        f"cbi_credit_remarks_{flag_name}_flag_cnt_rate_{time_suffix}"
                    ] = ratio_fun(
                        fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_{time_suffix}"],
                        records_with_remarks,
                    )

                    # cnt_all_rate: 所有记录的比例
                    fea[
                        f"cbi_credit_remarks_{flag_name}_flag_cnt_all_rate_{time_suffix}"
                    ] = ratio_fun(
                        fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_{time_suffix}"],
                        total_records,
                    )

                    # limit_max:
                    if "max_limit" in time_filtered_df.columns:
                        keyword_records = time_filtered_df[
                            time_filtered_df[flag_column] == 1
                        ]
                        if (
                            not keyword_records.empty
                            and "max_limit" in keyword_records.columns
                        ):
                            fea[
                                f"cbi_credit_remarks_{flag_name}_limit_max_{time_suffix}"
                            ] = keyword_records["max_limit"].max()
                            # limit_sum:
                            fea[
                                f"cbi_credit_remarks_{flag_name}_limit_sum_{time_suffix}"
                            ] = keyword_records["max_limit"].sum()
                        else:
                            fea[
                                f"cbi_credit_remarks_{flag_name}_limit_max_{time_suffix}"
                            ] = np.nan
                            fea[
                                f"cbi_credit_remarks_{flag_name}_limit_sum_{time_suffix}"
                            ] = np.nan
                    else:
                        fea[
                            f"cbi_credit_remarks_{flag_name}_limit_max_{time_suffix}"
                        ] = np.nan
                        fea[
                            f"cbi_credit_remarks_{flag_name}_limit_sum_{time_suffix}"
                        ] = np.nan
        else:
            # 兜底
            for keyword, flag_name in credit_remarks_mapping.items():
                fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_{time_suffix}"] = 0
                fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_rate_{time_suffix}"] = (
                    np.nan
                )
                fea[
                    f"cbi_credit_remarks_{flag_name}_flag_cnt_all_rate_{time_suffix}"
                ] = np.nan
                fea[f"cbi_credit_remarks_{flag_name}_limit_max_{time_suffix}"] = np.nan
                fea[f"cbi_credit_remarks_{flag_name}_limit_sum_{time_suffix}"] = np.nan

    # 统计全部的数
    total_records_all = df.shape[0]
    records_with_remarks_all = df["credit_remarks_flag"].sum()

    for keyword, flag_name in credit_remarks_mapping.items():
        flag_column = f"{flag_name}_flag"

        if flag_column in df.columns:
            # 全cnt
            fea[f"cbi_credit_remarks_{flag_name}_flag_cnt"] = df[flag_column].sum()

            # 全的cnt_rate
            fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_rate"] = ratio_fun(
                fea[f"cbi_credit_remarks_{flag_name}_flag_cnt"],
                records_with_remarks_all,
            )

            # 全cnt_all_rate
            fea[f"cbi_credit_remarks_{flag_name}_flag_cnt_all_rate"] = ratio_fun(
                fea[f"cbi_credit_remarks_{flag_name}_flag_cnt"], total_records_all
            )

            # 全limit
            if "max_limit" in df.columns:
                keyword_records_all = df[df[flag_column] == 1]
                if (
                    not keyword_records_all.empty
                    and "max_limit" in keyword_records_all.columns
                ):
                    fea[f"cbi_credit_remarks_{flag_name}_limit_max"] = (
                        keyword_records_all["max_limit"].max()
                    )
                    fea[f"cbi_credit_remarks_{flag_name}_limit_sum"] = (
                        keyword_records_all["max_limit"].sum()
                    )
                else:
                    fea[f"cbi_credit_remarks_{flag_name}_limit_max"] = np.nan
                    fea[f"cbi_credit_remarks_{flag_name}_limit_sum"] = np.nan
            else:
                fea[f"cbi_credit_remarks_{flag_name}_limit_max"] = np.nan
                fea[f"cbi_credit_remarks_{flag_name}_limit_sum"] = np.nan

    return fea


def cbi_credit_remarks_general_feature(df):
    fea = {}
    time_slices = {"6m": 183, "12m": 365, "24m": 730}

    for time_suffix, days_threshold in time_slices.items():
        time_filtered_df = df[df.gap_days <= days_threshold]

        if not time_filtered_df.empty and "max_limit" in time_filtered_df.columns:
            remarks_records = time_filtered_df[
                time_filtered_df["credit_remarks_flag"] == 1
            ]
            if not remarks_records.empty:
                fea[f"cbi_credit_remarks_limit_max_{time_suffix}"] = remarks_records[
                    "max_limit"
                ].max()
                fea[f"cbi_credit_remarks_limit_sum_{time_suffix}"] = remarks_records[
                    "max_limit"
                ].sum()
            else:
                fea[f"cbi_credit_remarks_limit_max_{time_suffix}"] = np.nan
                fea[f"cbi_credit_remarks_limit_sum_{time_suffix}"] = np.nan

            no_remarks_records = time_filtered_df[
                time_filtered_df["credit_remarks_flag"] != 1
            ]
            if not no_remarks_records.empty:
                fea[f"cbi_credit_no_remarks_limit_max_{time_suffix}"] = (
                    no_remarks_records["max_limit"].max()
                )
                fea[f"cbi_credit_no_remarks_limit_sum_{time_suffix}"] = (
                    no_remarks_records["max_limit"].sum()
                )
            else:
                fea[f"cbi_credit_no_remarks_limit_max_{time_suffix}"] = np.nan
                fea[f"cbi_credit_no_remarks_limit_sum_{time_suffix}"] = np.nan
        else:  # 兜底
            fea[f"cbi_credit_remarks_limit_max_{time_suffix}"] = np.nan
            fea[f"cbi_credit_remarks_limit_sum_{time_suffix}"] = np.nan
            fea[f"cbi_credit_no_remarks_limit_max_{time_suffix}"] = np.nan
            fea[f"cbi_credit_no_remarks_limit_sum_{time_suffix}"] = np.nan

    # 全范围total
    if "max_limit" in df.columns:
        remarks_records_all = df[df["credit_remarks_flag"] == 1]
        if not remarks_records_all.empty:
            fea["cbi_credit_remarks_limit_max"] = remarks_records_all["max_limit"].max()
            fea["cbi_credit_remarks_limit_sum"] = remarks_records_all["max_limit"].sum()
        else:
            fea["cbi_credit_remarks_limit_max"] = np.nan
            fea["cbi_credit_remarks_limit_sum"] = np.nan

        no_remarks_records_all = df[df["credit_remarks_flag"] != 1]
        if not no_remarks_records_all.empty:
            fea["cbi_credit_no_remarks_limit_max"] = no_remarks_records_all[
                "max_limit"
            ].max()
            fea["cbi_credit_no_remarks_limit_sum"] = no_remarks_records_all[
                "max_limit"
            ].sum()
        else:
            fea["cbi_credit_no_remarks_limit_max"] = np.nan
            fea["cbi_credit_no_remarks_limit_sum"] = np.nan
    else:
        fea["cbi_credit_remarks_limit_max"] = np.nan
        fea["cbi_credit_remarks_limit_sum"] = np.nan
        fea["cbi_credit_no_remarks_limit_max"] = np.nan
        fea["cbi_credit_no_remarks_limit_sum"] = np.nan

    return fea


def cbi_consum_run(base_df):
    fea = {}
    credit_pre_df = cbi_credit_pre(base_df)
    if credit_pre_df.empty:
        return fea
    cosum_df_cleaned = credit_pre_df[
        (credit_pre_df.CollateralOnFacility_flag != 1)
        & (credit_pre_df.credit_card_flag != 1)
        & (credit_pre_df.room_flag != 1)
        & (credit_pre_df.car_flag != 1)
    ]
    if not cosum_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_consum_feature(cosum_df_cleaned), "cbi_", "cbi_consume_"
            )
        )
    credit_card_df_cleaned = credit_pre_df[(credit_pre_df.credit_card_flag == 1)]
    if not credit_card_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_card_feature(credit_card_df_cleaned),
                "cbi_",
                "cbi_credit_card_",
            )
        )

    car_df_cleaned = credit_pre_df[(credit_pre_df.car_flag == 1)]
    if not car_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_car_feature(car_df_cleaned), "cbi_", "cbi_car_"
            )
        )

    room_df_cleaned = credit_pre_df[(credit_pre_df.room_flag == 1)]
    if not room_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_room_feature(room_df_cleaned), "cbi_", "cbi_room_"
            )
        )

    enterprises_df_cleaned = credit_pre_df[(credit_pre_df.enterprises_flag > 0)]
    if not enterprises_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_enterprises_feature(enterprises_df_cleaned),
                "cbi_",
                "cbi_enterprises_",
            )
        )
        # Add new v2 enterprise features with time slicing and multi-dimensional analysis
        fea.update(
            replace_dict_keys(
                cbi_credit_enterprises_v2_feature(enterprises_df_cleaned),
                "cbi_",
                "cbi_enterprises_v2_",
            )
        )

    coll_df_cleaned = credit_pre_df[(credit_pre_df.CollateralOnFacility_flag == 1)]
    if not coll_df_cleaned.empty:
        fea.update(
            replace_dict_keys(
                cbi_credit_collateral_feature(coll_df_cleaned),
                "cbi_",
                "cbi_collateral_",
            )
        )
    fea.update(cbi_credit_overdue_feature(credit_pre_df))
    # 计算remarks 的特征
    fea.update(cbi_credit_remarks_repayment_feature(credit_pre_df))
    fea.update(cbi_credit_remarks_aging_feature(credit_pre_df))
    fea.update(cbi_credit_remarks_feature(credit_pre_df))
    fea.update(cbi_credit_remarks_general_feature(credit_pre_df))
    return fea


def replace_dict_keys(d, old, new):
    new_dict = {}

    for key, value in d.items():
        new_key = key.replace(old, new)

        new_dict[new_key] = value

    return new_dict


def run(sqlResult):
    global CURRENT_DATE_TIME
    CURRENT_DATE_TIME = pd.to_datetime("now")
    result = {}
    if sqlResult:
        df = pd.DataFrame(json.loads(sqlResult[0]["response"]))

        result.update(cbi_consum_run(df))
        result.update(cbi_inq_feature(df))
        result.update(cbi_basic_identity(df))
        for k, v in result.items():
            if pd.isna(v):
                result[k] = NO_DATA
            elif isinstance(v, np.int64):
                result[k] = int(v)
        keys = set(result.keys())
        for k in keys - FEATURE_SET:
            result.pop(k)
        for k in FEATURE_SET - keys:
            result[k] = NO_DATA
        result["cbi_new_status"] = json.loads(sqlResult[0]["response"]).get(
            "status", "-9999"
        )
    result["cbi_new_ctime"] = sqlResult[0]["createTime"]
    return result


# result = run(sqlResult)
def run_retro_test(cbi_json, current_date: str):
    global CURRENT_DATE_TIME
    CURRENT_DATE_TIME = pd.to_datetime(current_date)
    result = {}
    if cbi_json:
        df = pd.DataFrame(json.loads(cbi_json))

        result.update(cbi_consum_run(df))
        result.update(cbi_inq_feature(df))
        result.update(cbi_basic_identity(df))
        for k, v in result.items():
            if pd.isna(v):
                result[k] = NO_DATA
            elif isinstance(v, np.int64):
                result[k] = int(v)
        keys = set(result.keys())
        for k in keys - FEATURE_SET:
            result.pop(k)
        for k in FEATURE_SET - keys:
            result[k] = NO_DATA
        result["cbi_new_status"] = json.loads(cbi_json).get("status", "-9999")
    return result


def run_online_test(cbi_json, cbi_timestamp: int):
    result = {}
    if cbi_json:
        global CURRENT_DATE_TIME
        CURRENT_DATE_TIME = pd.to_datetime(cbi_timestamp, unit="ms")
        df = pd.DataFrame(json.loads(cbi_json))

        result.update(cbi_consum_run(df))
        result.update(cbi_inq_feature(df))
        result.update(cbi_basic_identity(df))
        for k, v in result.items():
            if pd.isna(v):
                result[k] = NO_DATA
            elif isinstance(v, np.int64):
                result[k] = int(v)
        keys = set(result.keys())
        for k in keys - FEATURE_SET:
            result.pop(k)
        for k in FEATURE_SET - keys:
            result[k] = NO_DATA
        result["cbi_new_status"] = json.loads(cbi_json).get("status", "-9999")
    return result


if __name__ == "__main__":
    import json

    with open(
        "case_12.json",
        "r",
        encoding="utf-8",
    ) as f:
        cbi_json = json.load(f)
    # global CURRENT_DATE_TIME
    # CURRENT_DATE_TIME = pd.to_datetime(
    #     cbi_json["createTime"], unit="ms"
    # ) + pd.Timedelta(hours=7)
    # print(type(cbi_json["response"]))
    # df = pd.DataFrame(cbi_json["response"])
    # result = cbi_credit_pre(df)
    # print(result)
    cbi_json_str = json.dumps(cbi_json)
    result = run_online_test(cbi_json_str, 1762553014086)
    print(dict(sorted(result.items())))
