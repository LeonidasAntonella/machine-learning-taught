--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2025-09-23 10:59:23
-- Part 3: Final combined table with all risk indicators
--********************************************************************--
DROP TABLE IF EXISTS risk_data.new_clients_dpd_final FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.new_clients_dpd_final AS
SELECT
    p1.user_account_id,
    p1.order_id,
    p1.period_mark,
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
    d.period_mark,
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