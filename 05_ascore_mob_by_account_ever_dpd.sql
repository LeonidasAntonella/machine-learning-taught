
DROP TABLE IF EXISTS risk_data.ascore_mob_by_account_ever_dpd FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.ascore_mob_by_account_ever_dpd AS
WITH
    first_order_data AS (
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
            loan AS loan_amount,
            overdue_days1,
            credit_all_quota_at_loan AS credit_limit,
            mob1,
            mob2,
            mob3,
            mob4,
            mob5,
            mob6,
            mob7,
            mob8,
            mob9,
            mob10,
            mob11,
            mob12
        FROM
            indonesia_dw.risk_monitor_new_vintage_mob_user_list_dt_temp
        WHERE
            dt=DATE_SUB(CURRENT_DATE (), 1)
            AND loan_dt>='2025-01-01'
            AND is_reloan=0
    ),
    order_base AS (
        SELECT
            *
        FROM
            first_order_data
        WHERE
            stage_index<=1 -- 有的首期是 0，有的是 1，根据实际情况调整
    ),
    account_base AS (
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
            loan, -- 每期放款金额
            loan_sum, -- 累计放款，按照 index 倒序排列
            amount_payed, -- 已还本金
            amount_all_payed, -- 总已还金额
            overdue_days1
        FROM
            indonesia_dw.risk_monitor_new_vintage_mob_user_list_dt_temp
        WHERE
            dt=DATE_SUB(CURRENT_DATE (), 1)
            AND loan_dt>='2025-01-01'
    ),
    base_data AS (
        SELECT
            acc.user_account_id,
            acc.order_id,
            acc.period_mark,
            acc.stage_index,
            acc.stage_num,
            acc.loan_dt,
            acc.loan_time,
            acc.apply_time,
            acc.dt,
            acc.deadline_dt,
            acc.finish_dt,
            acc.loan,
            acc.loan_sum,
            acc.amount_payed,
            acc.amount_all_payed,
            acc.overdue_days1,
            ord.mob1,
            ord.mob2,
            ord.mob3,
            ord.mob4,
            ord.mob5,
            ord.mob6,
            ord.mob7,
            ord.mob8,
            ord.mob9,
            ord.mob10,
            ord.mob11,
            ord.mob12
        FROM
            account_base acc
            LEFT JOIN order_base ord ON acc.user_account_id=ord.user_account_id
    ),
    flag_mobx_7 AS (
        SELECT
            user_account_id,
            order_id,
            MAX(
                IF(
                    DATE_ADD(mob1, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob1 -- 是否到期
                        AND (
                            finish_dt IS NULL --- 一直逾期
                            OR DATEDIFF(finish_dt, mob1)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob1_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob2, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob2 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob2)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob2_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob3, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob3 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob3)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob3_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob4, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob4 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob4)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob4_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob5, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob5 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob5)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob5_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob6, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob6 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob6)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob6_7_flag,
            MAX(
                IF(
                    DATE_ADD(mob7, 7)>dt, -- 可观测
                    NULL,
                    IF(
                        deadline_dt<=mob7 -- 是否到期
                        AND (
                            finish_dt IS NULL
                            OR DATEDIFF(finish_dt, mob7)>=7
                        ), -- 7 天未还
                        1,
                        0
                    )
                )
            ) AS mob7_7_flag
        FROM
            base_data
        GROUP BY
            user_account_id,
            order_id
    ),
    mobx_7 AS (
        SELECT
            user_account_id,
            COUNT(*) AS total_order_count,
            MAX(
                CASE
                    WHEN mob1_7_flag IS NULL THEN NULL
                    WHEN mob1_7_flag=1 THEN 1
                    ELSE 0
                END
            ) AS mob1_7,
            MAX(
                CASE
                    WHEN mob2_7_flag IS NULL THEN NULL
                    WHEN GREATEST(mob1_7_flag, mob2_7_flag)=1 THEN 1
                    ELSE 0
                END
            ) AS mob2_7,
            MAX(
                CASE
                    WHEN mob3_7_flag IS NULL THEN NULL
                    WHEN GREATEST(mob1_7_flag, mob2_7_flag, mob3_7_flag)=1 THEN 1
                    ELSE 0
                END
            ) AS mob3_7,
            MAX(
                CASE
                    WHEN mob4_7_flag IS NULL THEN NULL
                    WHEN GREATEST(
                        mob1_7_flag,
                        mob2_7_flag,
                        mob3_7_flag,
                        mob4_7_flag
                    )=1 THEN 1
                    ELSE 0
                END
            ) AS mob4_7,
            MAX(
                CASE
                    WHEN mob5_7_flag IS NULL THEN NULL
                    WHEN GREATEST(
                        mob1_7_flag,
                        mob2_7_flag,
                        mob3_7_flag,
                        mob4_7_flag,
                        mob5_7_flag
                    )=1 THEN 1
                    ELSE 0
                END
            ) AS mob5_7,
            MAX(
                CASE
                    WHEN mob6_7_flag IS NULL THEN NULL
                    WHEN GREATEST(
                        mob1_7_flag,
                        mob2_7_flag,
                        mob3_7_flag,
                        mob4_7_flag,
                        mob5_7_flag,
                        mob6_7_flag
                    )=1 THEN 1
                    ELSE 0
                END
            ) AS mob6_7,
            MAX(
                CASE
                    WHEN mob7_7_flag IS NULL THEN NULL
                    WHEN GREATEST(
                        mob1_7_flag,
                        mob2_7_flag,
                        mob3_7_flag,
                        mob4_7_flag,
                        mob5_7_flag,
                        mob6_7_flag,
                        mob7_7_flag
                    )=1 THEN 1
                    ELSE 0
                END
            ) AS mob7_7
        FROM
            flag_mobx_7
        GROUP BY
            user_account_id
    )
SELECT
    order_base.user_account_id,
    order_base.order_id,
    order_base.period_mark,
    order_base.loan_dt,
    order_base.loan_time,
    order_base.loan_amount,
    order_base.apply_time,
    order_base.stage_num,
    order_base.credit_limit,
    mobx_7.mob1_7,
    mobx_7.mob2_7,
    mobx_7.mob3_7,
    mobx_7.mob4_7,
    mobx_7.mob5_7,
    mobx_7.mob6_7,
    mobx_7.mob7_7
FROM
    order_base
    LEFT JOIN mobx_7 ON order_base.user_account_id=mobx_7.user_account_id
;

SELECT
    *
FROM
    risk_data.ascore_mob_by_account_ever_dpd
LIMIT
    10
;

DROP TABLE IF EXISTS risk_data.ascore_mob_by_account_ever_dpd_req_id FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.ascore_mob_by_account_ever_dpd_req_id AS
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
    d.mob1_7,
    d.mob2_7,
    d.mob3_7,
    d.mob4_7,
    d.mob5_7,
    d.mob6_7,
    d.mob7_7
FROM
    risk_data.ascore_mob_by_account_ever_dpd d
    INNER JOIN base_requests r ON d.user_account_id=r.busi_account_id
    AND DATE(d.loan_dt)>=DATE(r.dt)
    AND DATE(d.loan_dt)<=DATE_ADD(DATE(r.dt), INTERVAL 30 DAY)
;