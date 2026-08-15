DROP TABLE IF EXISTS risk_data.new_clients_dpd_part1 FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_part1 AS
WITH
    base_data AS (
        SELECT
            CAST(user_account_id AS STRING) AS user_account_id,
            CAST(order_id AS STRING) AS order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d40_10 AS (
        SELECT
            user_account_id,
            order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d70_10 AS (
        SELECT
            user_account_id,
            order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    )
SELECT
    d33.user_account_id,
    d33.order_id,
    d33.stage_num,
    d33.loan,
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

DROP TABLE IF EXISTS risk_data.new_clients_dpd_part2 FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_part2 AS
WITH
    base_data AS (
        SELECT
            CAST(user_account_id AS STRING) AS user_account_id,
            CAST(order_id AS STRING) AS order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d130_10 AS (
        SELECT
            user_account_id,
            order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d160_10 AS (
        SELECT
            user_account_id,
            order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_d190_10 AS (
        SELECT
            user_account_id,
            order_id,
            stage_num,
            loan,
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
            stage_num,
            loan,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    )
SELECT
    d100.user_account_id,
    d100.order_id,
    d100.stage_num,
    d100.loan,
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

DROP TABLE IF EXISTS risk_data.new_clients_dpd_final FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_final AS
SELECT
    p1.user_account_id,
    p1.order_id,
    p1.stage_num,
    p1.loan,
    p1.loan_dt,
    p1.loan_time,
    p1.credit_limit,
    p1.apply_time,
    p1.M1_3,
    p1.M1_10,
    p1.M2_10,
    p2.M3_10,
    p2.M4_10,
    p2.M5_10,
    p2.M6_10
FROM
    risk_data.new_clients_dpd_part1 p1
    LEFT JOIN risk_data.new_clients_dpd_part2 p2 ON p1.user_account_id=p2.user_account_id
;

DROP TABLE IF EXISTS risk_data.new_clients_dpd_req_id_pro FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_req_id_pro AS
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
    d.stage_num,
    d.loan,
    d.credit_limit,
    r.scene,
    r.dt AS req_dt,
    r.created_at AS req_created_at,
    d.loan_dt,
    d.loan_time AS order_loan_time,
    d.apply_time AS order_apply_time,
    d.M1_3,
    d.M1_10,
    d.M2_10,
    d.M3_10,
    d.M4_10,
    d.M5_10,
    d.M6_10
FROM
    risk_data.new_clients_dpd_final d
    INNER JOIN base_requests r ON d.user_account_id=r.busi_account_id
    AND DATE(d.loan_dt)>=DATE(r.dt)
    AND DATE(d.loan_dt)<=DATE_ADD(DATE(r.dt), INTERVAL 30 DAY)
;