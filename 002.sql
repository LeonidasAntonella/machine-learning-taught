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
