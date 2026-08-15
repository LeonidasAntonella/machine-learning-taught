DROP TABLE IF EXISTS risk_data.ascore_clients_ever_dpd FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.ascore_clients_ever_dpd AS
WITH
    base_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            stage_index,
            stage_num,
            loan_dt,
            loan_time,
            apply_time,
            dt,
            deadline_dt,
            finish_dt,
            loan as loan_amount,
            credit_all_quota_at_loan AS credit_limit
        FROM
            indonesia_dw.dwd_base_order_bill_repay_plan_df
        WHERE
            loan_dt>='2025-01-01'
            AND dt>='2025-01-01'
            AND is_reloan=0
    ),
    order_base AS (
        SELECT
            *
        FROM
            base_data
        WHERE
            dt=DATE_SUB(CURRENT_DATE (), 1)
            AND stage_index IN (0, 1)
    ),
    mob1_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=34
    ),
    mob2_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=65
    ),
    mob3_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=96
    ),
    mob4_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=127
    ),
    mob5_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=158
    ),
    mob6_3_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=189
    ),
    mob1_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=41
    ),
    mob2_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=72
    ),
    mob3_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=103
    ),
    mob4_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=134
    ),
    mob5_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=165
    ),
    mob6_10_data AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            DATEDIFF(
                DATE(
                    IF(
                        finish_dt IS NULL
                        OR finish_dt='',
                        dt,
                        finish_dt
                    )
                ),
                DATE(deadline_dt)
            ) AS overdue_days
        FROM
            base_data
        WHERE
            DATEDIFF(DATE(dt), DATE(loan_dt))=196
    ),
    flag_mob1_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob1_3
        FROM
            mob1_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob2_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob2_3
        FROM
            mob2_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob3_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob3_3
        FROM
            mob3_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob4_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob4_3
        FROM
            mob4_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob5_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob5_3
        FROM
            mob5_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob6_3 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=3, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob6_3
        FROM
            mob6_3_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob1_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob1_10
        FROM
            mob1_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob2_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob2_10
        FROM
            mob2_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob3_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob3_10
        FROM
            mob3_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob4_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob4_10
        FROM
            mob4_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob5_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob5_10
        FROM
            mob5_10_data
        GROUP BY
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit
    ),
    flag_mob6_10 AS (
        SELECT
            user_account_id,
            order_id,
            period_mark,
            loan_dt,
            loan_time,
            apply_time,
            credit_limit,
            CASE
                WHEN SUM(IF(overdue_days>=10, 1, 0))>=1 THEN 1
                WHEN COUNT(*)-SUM(IF(overdue_days<=1, 1, 0))=0 THEN 0
                ELSE 2
            END AS mob6_10
        FROM
            mob6_10_data
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
    order_base.user_account_id,
    order_base.order_id,
    order_base.period_mark,
    order_base.loan_dt,
    order_base.loan_time,
    order_base.credit_limit,
    order_base.loan_amount,
    order_base.apply_time,
    order_base.stage_num,
    COALESCE(t_mob1_3.mob1_3, -1) AS mob1_3,
    COALESCE(t_mob2_3.mob2_3, -1) AS mob2_3,
    COALESCE(t_mob3_3.mob3_3, -1) AS mob3_3,
    COALESCE(t_mob4_3.mob4_3, -1) AS mob4_3,
    COALESCE(t_mob5_3.mob5_3, -1) AS mob5_3,
    COALESCE(t_mob6_3.mob6_3, -1) AS mob6_3,
    COALESCE(t_mob1_10.mob1_10, -1) AS mob1_10,
    COALESCE(t_mob2_10.mob2_10, -1) AS mob2_10,
    COALESCE(t_mob3_10.mob3_10, -1) AS mob3_10,
    COALESCE(t_mob4_10.mob4_10, -1) AS mob4_10,
    COALESCE(t_mob5_10.mob5_10, -1) AS mob5_10,
    COALESCE(t_mob6_10.mob6_10, -1) AS mob6_10
FROM
    order_base
    LEFT JOIN flag_mob1_3 t_mob1_3 ON order_base.user_account_id=t_mob1_3.user_account_id
    LEFT JOIN flag_mob2_3 t_mob2_3 ON order_base.user_account_id=t_mob2_3.user_account_id
    LEFT JOIN flag_mob3_3 t_mob3_3 ON order_base.user_account_id=t_mob3_3.user_account_id
    LEFT JOIN flag_mob4_3 t_mob4_3 ON order_base.user_account_id=t_mob4_3.user_account_id
    LEFT JOIN flag_mob5_3 t_mob5_3 ON order_base.user_account_id=t_mob5_3.user_account_id
    LEFT JOIN flag_mob6_3 t_mob6_3 ON order_base.user_account_id=t_mob6_3.user_account_id
    LEFT JOIN flag_mob1_10 t_mob1_10 ON order_base.user_account_id=t_mob1_10.user_account_id
    LEFT JOIN flag_mob2_10 t_mob2_10 ON order_base.user_account_id=t_mob2_10.user_account_id
    LEFT JOIN flag_mob3_10 t_mob3_10 ON order_base.user_account_id=t_mob3_10.user_account_id
    LEFT JOIN flag_mob4_10 t_mob4_10 ON order_base.user_account_id=t_mob4_10.user_account_id
    LEFT JOIN flag_mob5_10 t_mob5_10 ON order_base.user_account_id=t_mob5_10.user_account_id
    LEFT JOIN flag_mob6_10 t_mob6_10 ON order_base.user_account_id=t_mob6_10.user_account_id
;



select * from risk_data.ascore_clients_ever_dpd limit 10


----- 场景一，场景二
DROP TABLE IF EXISTS risk_data.ascore_clients_ever_dpd_req_id FORCE
;

select * from risk_data.ascore_clients_ever_dpd_req_id limit 10
;

CREATE TABLE IF NOT EXISTS risk_data.ascore_clients_ever_dpd_req_id AS
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
                    dt>='2025-01-01'
                    -- AND dt<='2025-02-30'
                    AND country='indonesia'
                    AND scene IN (
                        'indo_firstloan_credit_2',
                        'indo_firstloan_credit_1'
                    )
                    AND final_decision='accept'
                    AND diagram_end_id NOT IN ('FLQ220413016', 'FLQ220413055')
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
    d.loan_amount,
    r.scene,
    r.dt AS req_dt,
    r.created_at AS req_created_at,
    d.loan_dt,
    d.loan_time AS order_loan_time,
    d.apply_time AS order_apply_time,
    d.stage_num,
    d.mob1_3,
    d.mob2_3,
    d.mob3_3,
    d.mob4_3,
    d.mob5_3,
    d.mob6_3,
    d.mob1_10,
    d.mob2_10,
    d.mob3_10,
    d.mob4_10,
    d.mob5_10,
    d.mob6_10
FROM
    risk_data.ascore_clients_ever_dpd d
    INNER JOIN base_requests r ON d.user_account_id=r.busi_account_id
    AND DATE(d.loan_dt)>=DATE(r.dt)
    AND DATE(d.loan_dt)<=DATE_ADD(DATE(r.dt), INTERVAL 30 DAY)
;


--- 反欺诈场景
DROP TABLE IF EXISTS risk_data.ascore_clients_ever_dpd_order_id FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.ascore_clients_ever_dpd_order_id AS
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
                    dt>='2025-01-01'
                    -- AND dt<='2025-02-30'
                    AND country='indonesia'
                    AND scene='indo_cyc_firstloan_antifraud'
                    AND final_decision='accept'
                    AND diagram_end_id NOT IN ('FLQ220413016', 'FLQ220413055')
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
    d.stage_num,
    d.credit_limit,
    r.scene,
    r.dt AS order_dt,
    r.created_at AS order_created_at,
    d.loan_dt,
    d.loan_time AS order_loan_time,
    d.apply_time AS order_apply_time,
    d.stage_num,
    d.mob1_3,
    d.mob2_3,
    d.mob3_3,
    d.mob4_3,
    d.mob5_3,
    d.mob6_3,
    d.mob1_10,
    d.mob2_10,
    d.mob3_10,
    d.mob4_10,
    d.mob5_10,
    d.mob6_10
FROM
    risk_data.ascore_clients_ever_dpd d
    INNER JOIN base_requests r ON d.user_account_id=r.busi_account_id
    AND DATE(d.loan_dt)>=DATE(r.dt)
    AND DATE(d.loan_dt)<=DATE_ADD(DATE(r.dt), INTERVAL 1 DAY)
;

