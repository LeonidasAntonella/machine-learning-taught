--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2025-09-23 10:59:23
-- Part 1: Base data and first three risk indicators (M1_3, M1_10, M2_10)
--********************************************************************--
DROP TABLE IF EXISTS risk_data.new_clients_dpd_part1 FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_part1 AS
WITH
    base_data AS (
        SELECT
            CAST(user_account_id AS STRING) AS user_account_id,
            CAST(order_id AS STRING) AS order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            dt,
            deadline_dt,
            finish_dt,
            credit_all_quota_at_loan AS credit_limit,
            cal_overdue_days
        FROM
            indonesia_dw.dwd_base_order_bill_repay_plan_df
        WHERE
            loan_dt>='2025-01-01'
            -- AND loan_dt <= '2025-02-30'
            AND dt>='2024-12-01'
            AND is_reloan=0
    ),
    d33_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            cal_overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(deadline_dt))=3
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=34
    ),
    d40_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            cal_overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(deadline_dt))=10
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=41
    ),
    d70_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            cal_overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(deadline_dt))=10
            AND DATEDIFF(DATE(dt), DATE(loan_dt))>41
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=72
    ),
    flag_d33_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(cal_overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(cal_overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS d33_3
        FROM
            d33_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d40_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(cal_overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(cal_overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS d40_10
        FROM
            d40_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d70_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(cal_overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(cal_overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS d70_10
        FROM
            d70_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    )
SELECT
    d33.user_account_id,
    d33.order_id,
    d33.period_mark,
    d33.loan_dt,
    d33.loan_time,
    d33.credit_limit,
    d33.apply_time,
    d33.d33_3 AS M1_3,
    COALESCE(d40.d40_10, -1) AS M1_10,
    COALESCE(d70.d70_10, -1) AS M2_10
FROM
    flag_d33_3 d33
    LEFT JOIN flag_d40_10 d40 ON d33.user_account_id=d40.user_account_id
    LEFT JOIN flag_d70_10 d70 ON d33.user_account_id=d70.user_account_id
;