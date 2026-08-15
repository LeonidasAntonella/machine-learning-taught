--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2026-03-18 19:39:06
--********************************************************************--
DROP TABLE IF EXISTS test_db.ascore_features_funnel FORCE
;

CREATE TABLE IF NOT EXISTS test_db.ascore_features_funnel AS
WITH
    base_1 AS (
        SELECT
            *
        FROM
            (
                SELECT
                    req_id AS req_id,
                    busi_account_id AS busi_account_id,
                    final_decision AS final_decision,
                    data_used.sjy251010139__value AS cbi_raw_premium_v3,
                    data_used.sjy2511031662__value AS d100_cbi_v1,
                    data_used.sjy260204350__value AS a4m1,
                    data_used.sjy2602041040__value AS a4m3,
                    data_used.sjy260317321__value AS first_loan_d0_order_v1,
                    dt AS req_dt,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            busi_account_id
                        ORDER BY
                            create_at DESC
                    ) AS row_rnk
                FROM
                    indonesia_dw.dw_risk_engine_requests_v2_di
                WHERE
                    dt>='2026-01-01'
                    AND scene IN (
                        'indo_firstloan_credit_2',
                        'indo_firstloan_credit_1'
                    )
            )
        WHERE
            row_rnk=1
    ),
    base_2 AS (
        SELECT
            *
        FROM
            (
                SELECT
                    req_id AS req_id_anti,
                    busi_account_id AS busi_account_id_anti,
                    final_decision AS final_decision_anti,
                    dt AS dt_anti,
                    data_used.sjy2511031661__value AS d40_rescoring_v1,
                    data_used.sjy260210414__value AS a4m1_loan,
                    data_used.sjy260210665__value AS a4m3_loan,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            busi_account_id
                        ORDER BY
                            create_at DESC
                    ) AS row_rnk
                FROM
                    indonesia_dw.dw_risk_engine_requests_v2_di
                WHERE
                    dt>='2026-02-01'
                    AND scene='indo_cyc_firstloan_antifraud'
            )
        WHERE
            row_rnk=1
    )
SELECT
    b1.req_id,
    b1.busi_account_id,
    b1.final_decision,
    b1.req_dt,
    b2.req_id_anti,
    b2.busi_account_id_anti,
    b2.final_decision_anti,
    b2.dt_anti,
    b1.cbi_raw_premium_v3,
    b1.d100_cbi_v1,
    b1.a4m1,
    b1.a4m3,
    b1.first_loan_d0_order_v1,
    b2.d40_rescoring_v1,
    b2.a4m3_loan,
    b2.a4m1_loan
FROM
    base_1 AS b1
    LEFT JOIN base_2 AS b2 ON b1.busi_account_id=b2.busi_account_id_anti
    AND DATE(b2.dt_anti)>=DATE(b1.req_dt)
    AND DATE(b2.dt_anti)<=DATE_ADD(DATE(b1.req_dt), INTERVAL 30 DAY)
;

SELECT
    *
FROM
    test_db.ascore_features_funnel
LIMIT
    10
;