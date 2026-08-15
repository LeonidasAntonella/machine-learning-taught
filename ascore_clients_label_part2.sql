--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2025-09-23 10:59:23
-- Part 2: Last four risk indicators (M3_10, M4_10, M5_10, M6_10)
--********************************************************************--
DROP TABLE IF EXISTS risk_data.new_clients_dpd_part2 FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_part2 AS
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
    d100_10_data AS (
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
            AND DATEDIFF(DATE(dt), DATE(loan_dt))>72
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=103
    ),
    d130_10_data AS (
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
            AND DATEDIFF(DATE(dt), DATE(loan_dt))>103
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=134
    ),
    d160_10_data AS (
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
            AND DATEDIFF(DATE(dt), DATE(loan_dt))>134
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=165
    ),
    d190_10_data AS (
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
            AND DATEDIFF(DATE(dt), DATE(loan_dt))>165
            AND DATEDIFF(DATE(dt), DATE(loan_dt))<=196
    ),
    flag_d100_10 AS (
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
            END AS d100_10
        FROM
            d100_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d130_10 AS (
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
            END AS d130_10
        FROM
            d130_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d160_10 AS (
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
            END AS d160_10
        FROM
            d160_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d190_10 AS (
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
            END AS d190_10
        FROM
            d190_10_data
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
    d100.user_account_id,
    d100.order_id,
    d100.period_mark,
    d100.loan_dt,
    d100.loan_time,
    d100.credit_limit,
    d100.apply_time,
    COALESCE(d100.d100_10, -1) AS M3_10,
    COALESCE(d130.d130_10, -1) AS M4_10,
    COALESCE(d160.d160_10, -1) AS M5_10,
    COALESCE(d190.d190_10, -1) AS M6_10
FROM
    flag_d100_10 d100
    LEFT JOIN flag_d130_10 d130 ON d100.user_account_id=d130.user_account_id
    LEFT JOIN flag_d160_10 d160 ON d100.user_account_id=d160.user_account_id
    LEFT JOIN flag_d190_10 d190 ON d100.user_account_id=d190.user_account_id
;