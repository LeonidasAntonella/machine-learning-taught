--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2026-03-24 10:13:16
--********************************************************************--


DROP TABLE IF EXISTS risk_data.bscore_ever_dpd_req_id FORCE
;

CREATE TABLE IF NOT EXISTS risk_data.bscore_ever_dpd_req_id AS
SELECT
    req_id AS req_id_anti,
    account_id AS busi_account_id,
    req_dt AS req_dt_anti,
    req_at AS create_at_anti,
    scene as scene_anti,
    req_id_pre_quota as req_id_quota,
    req_dt_pre_quota as req_dt_quota,
    DATE_FORMAT(date_trunc ('week', loan_dt), '%Y-%m-%d') AS loan_dt_week,
    order_id,
    loan_dt,
    loan_at,
    order_stage,
    order_num,
    order_loan,
    order_outstanding,
    account_aging_days,
    mob1_7_ever AS mob1_7,
    mob2_7_ever AS mob2_7,
    mob3_7_ever AS mob3_7,
    mob4_7_ever AS mob4_7,
    mob5_7_ever AS mob5_7,
    mob6_7_ever AS mob6_7,
    mob7_7_ever AS mob7_7,
    mob8_7_ever AS mob8_7,
    mob9_7_ever AS mob9_7,
    mob10_7_ever AS mob10_7,
    mob11_7_ever AS mob11_7,
    mob12_7_ever AS mob12_7,
    mob1_7_loan,
    mob2_7_loan,
    mob3_7_loan,
    mob4_7_loan,
    mob5_7_loan,
    mob6_7_loan,
    mob7_7_loan,
    mob8_7_loan,
    mob9_7_loan,
    mob10_7_loan,
    mob11_7_loan,
    mob12_7_loan
FROM
    indonesia_dw.risk_request_order_vintage_df
WHERE
    dt=CAST(DATE_FORMAT(CURRENT_DATE() - 1, '%Y-%m-%d') AS STRING)
    AND req_dt>='2025-01-01'
    AND is_reloan = 1
;




select DATE_FORMAT(req_dt_pre_credit, '%Y-%m'), AVG(mob1_3)
FROM
    indonesia_dw.risk_request_order_vintage_df
WHERE
    dt=DATE(CURRENT_DATE () -1)
    AND req_dt_pre_credit>='2025-01-01'
    AND is_reloan=0
    group by DATE_FORMAT(req_dt_pre_credit, '%Y-%m')
;


select req_dt_month, avg(mob1_7) from risk_data.bscore_ever_dpd_req_id 
group by req_dt_month
;

select * from indonesia_dw.dw_afpi_new_features_v3_all_width_recall_di 
;

select * from indonesia_dw.dwd_risk_engine_cbi_src_report_di
where dt ='2026-01-01'
limit 10
;

select * from test_db.ascore_for_reloan_dt_20260401_v1
limit 10;




SELECT 
sam.user_account_id     --用户id
, sam.dt                --月中观察日
--, his_loan_num
, sam.order_deadline_dt
, sam.order_finish_dt
, case when sam.order_finish_dt < sam.dt then 1 when sam.order_finish_dt >= sam.dt then 0 end as is_settle  --是否结清
, DATEDIFF(sam.dt, sam.order_finish_dt) as settle_days--结清距今天数
, DATEDIFF(sam.dt, sam.order_deadline_dt) as deadline_days--最后一笔账单到期日距今天数
--, b.overdue_days
, c.is_blacklist_user
, c.is_risk_blacklist_user
, c.max_overdue_days
, c.overdue_status
from (
    SELECT
    user_account_id
    , date(dt) as dt  --月中观察日
    , (case when sum(if(finish_dt is null and datediff(to_date(deadline_dt), dt)<0,1,0))>=1 then 1 else 0 end) as overdue_ing
    --, max(his_loan_num)+1 as his_loan_num         --历史借款数
    --, max(credit_usable_at_loan) as credit_usable_at_loan --最后一笔订单借款额度
    , max(order_deadline_dt) as order_deadline_dt           --最后一笔订单到期日 
    --, max(ifnull(date(order_finish_at), date(order_deadline_dt))) as order_finish_dt  --最后一笔订单结清日（实还）,如果为空null则取order_deadline_dt；这会包含未实际还款的
    , max(ifnull(date(order_finish_at), date('2999-01-01'))) as order_finish_dt  --最后一笔订单结清日（实还）,如果为空null则取‘2999-01-01’
    from indonesia_dw.dwd_base_order_bill_repay_plan_df     --还款计划明细表
    where dt = '2026-03-01'
    group by user_account_id, dt
) sam   
--left join test_db.ly_20260224_test_tmp04 b on sam.user_account_id = b.user_account_id and sam.dt = b.dt
inner join (select account_id, dt, is_blacklist_user, is_risk_blacklist_user, overdue_status, max_overdue_days 
            from indonesia_app.app_user_portrait_df
            where dt = '2026-03-01'
            and loan_order_num >= 1     --1单+
            and overdue_status != 1     --非当前逾期
            and is_risk_blacklist_user != 1  --风控非黑名单
            ) c on cast(sam.user_account_id as string) = cast(c.account_id as string) and sam.dt = c.dt
--where sam.overdue_ing = 0       --剔除正在逾期的用户(自己的逻辑)
--and b.overdue_days < 31     --历史最大逾期天数<31（自己的逻辑）
--and c.is_blacklist_user!=1  --非黑名单。（用户画像表里的）
--and c.is_risk_blacklist_user!=1
;





SELECT * FROM indonesia_dw.dwd_risk_engine_cbi_src_report_di dc 
WHERE dc.scene = "indo_cyc_reloan_antifraud" and dt = '2025-11-12' limit 10;




select count(*) from indonesia_ods.ods_cbi_report_di 
where dt = '2026-01-01'
limit 10;

DROP TABLE IF EXISTS test_db.hugo_cbi_account_raw_report FORCE;
create table if not exists test_db.hugo_cbi_account_raw_report 
as 
SELECT * FROM indonesia_ods.ods_cbi_report_di
where dt = '2025-11-07' 
;

select count(*) from test_db.hugo_cbi_account_raw_report;



SELECT
features
, get_json_object(
        regexp_replace(features, 'NaN', 'null'), '$.ind_hist_identity_last_change_type') AS ind_hist_identity_last_change_type
, get_json_object(
        regexp_replace(features, 'NaN', 'null'), '$.ind_hist_identity_last_change_data') AS ind_hist_identity_last_change_data
FROM risk_data.risk_cbi_v3_feature
WHERE dt = '2025-06-01'
LIMIT 10;


select * from test_db.bst_cbi_v2_feature_202511 
limit 10;


