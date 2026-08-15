DROP TABLE IF EXISTS risk_data.new_clients_dpd FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd AS
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
    )
SELECT
    d33.user_account_id,
    d33.order_id,
    d33.period_mark,
    d33.loan_dt,
    d33.loan_time,
    d33.credit_limit,
    d33.apply_time,
    d33.d33_3,
    COALESCE(d40.d40_10, -1) AS d40_10,
    COALESCE(d70.d70_10, -1) AS d70_10,
    COALESCE(d100.d100_10, -1) AS d100_10
FROM
    flag_d33_3 d33
    LEFT JOIN flag_d40_10 d40 ON d33.user_account_id=d40.user_account_id
    LEFT JOIN flag_d70_10 d70 ON d33.user_account_id=d70.user_account_id
    LEFT JOIN flag_d100_10 d100 ON d33.user_account_id=d100.user_account_id
;

SELECT
    *
FROM
    indonesia_dw.dwd_base_order_bill_repay_plan_df
WHERE
    is_reloan=0
    AND loan_dt='2025-07-01'
    AND dt='2025-09-01'
    AND installment_type!='single'
LIMIT
    20
;

SELECT
    *
FROM
    risk_data.new_clients_dpd
LIMIT
    10
;

DROP TABLE IF EXISTS risk_data.new_clients_dpd_req_id FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_req_id AS
WITH
    base_requests AS (
        SELECT
            *
        FROM
            (
                SELECT
                    req_id,
                    busi_account_id,
                    created_at,
                    dt,
                    scene,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            busi_account_id
                        ORDER BY
                            created_at DESC
                    ) AS seq
                FROM
                    indonesia_dw.dw_risk_engine_requests_dt
                WHERE
                    dt>='2024-12-30'
                    -- AND dt<='2025-02-30'
                    AND country='indonesia'
                    AND scene IN (
                        'indo_firstloan_credit_2',
                        'indo_firstloan_credit_1'
                    )
                    AND final_decision='accept'
            ) t
        WHERE
            seq=1
    )
SELECT
    -- DPD
    d.user_account_id,
    r.req_id,
    d.order_id,
    d.period_mark,
    d.credit_limit,
    r.scene,
    r.dt AS req_dt,
    r.created_at AS req_created_at,
    d.loan_dt,
    d.loan_time AS order_loan_time,
    d.apply_time AS order_apply_time,
    d.d33_3,
    d.d40_10,
    d.d70_10,
    d.d100_10
FROM
    risk_data.new_clients_dpd d
    INNER JOIN base_requests r ON d.user_account_id=r.busi_account_id
    AND DATE(d.loan_dt)>=DATE(r.dt)
    AND DATE(d.loan_dt)<=DATE_ADD(DATE(r.dt), INTERVAL 30 DAY)
;

SELECT
    MIN(loan_dt),
    MAX(loan_dt)
FROM
    risk_data.new_clients_dpd_req_id
;

-- SELECT
--     user_account_id,
--     COUNT(*) AS occurrence
-- FROM
--     test_db.new_clients_dpd
-- GROUP BY
--     user_account_id
-- HAVING
--     COUNT(*)>1
-- LIMIT
--     5
-- ;
-- select dataset_type, count(*) from test_db.tk_score_result_40d_70d_v2
-- group by dataset_type
-- ;
SELECT
    COUNT(dt)
FROM
    indonesia_ods.ods_sqoop_rupiah_risk_triple_management_third_partner_data_di
WHERE
    `__country_code`='indonesia'
    AND `third_partner_code`='cbi'
    AND `interface_code`='report'
    AND dt>='2025-04-06'
    AND dt<='2025-08-18'
SELECT
    COUNT(dt)
FROM
    indonesia_ods.ods_cbi_report_di
WHERE
    dt>='2025-04-06'
    AND dt<='2025-06-01'
;

SELECT
    *
FROM
    risk_data.df_cbi_report_v2_enterprises_feature_20250911_v1
LIMIT
    10
;

SELECT
    COUNT(*)
FROM
    risk_data.indo_ascore_d40_base_v1_oot_20250917
;

SELECT
    COUNT(*)
FROM
    risk_data.indo_ascore_d40_cbi_raw_premium_v3_oot_20250918
;

SELECT
    *
FROM
    indonesia_dw.dwd_base_order_bill_repay_plan_df
WHERE
    user_account_id=250209010631205694
    AND is_reloan=0
    AND dt='2025-05-23'
;
