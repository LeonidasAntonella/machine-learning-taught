INSERT
    OVERWRITE TABLE test_db.tmp_wqk_20250305_20251106_cbi_test_di PARTITION (dt)
SELECT
    account_id,
    create_time,
    GET_JSON_OBJECT(response, '$.status') AS status,
    GET_JSON_OBJECT(response, '$.error') AS error,
    GET_JSON_OBJECT(response, '$.message') AS message,
    GET_JSON_OBJECT(response, '$.result') AS result,
    dt
FROM
    (
        SELECT
            GET_JSON_OBJECT(line, '$.accountId') AS account_id,
            GET_JSON_OBJECT(line, '$.createTime') AS create_time,
            GET_JSON_OBJECT(line, '$.response') AS response,
            dt
        FROM
            indonesia_ods.ods_cbi_report_di
        WHERE
            dt>='2025-11-01'
            AND dt<'2025-11-10'
            -- where dt >= '2025-07-01' and dt < '2025-08-01'
            -- where dt = '2025-11-05'
    ) x
;

;

DROP TABLE indonesia_dw.dwd_risk_engine_cbi_src_report_di
;

CREATE EXTERNAL TABLE indonesia_dw.dwd_risk_engine_cbi_src_report_di (
    `id` BIGINT,
    `req_id` STRING,
    `busi_account_id` BIGINT,
    `create_at` STRING,
    `datacache_create_time` BIGINT,
    `scene` STRING,
    `hitcache` STRING,
    `is_found` INT,
    `account_id` STRING,
    `create_time` STRING,
    `status` STRING,
    `error` STRING,
    `message` STRING,
    `result` STRING
) PARTITIONED BY (req_type STRING, dt STRING)
STORED AS orcfile LOCATION 'obs://opay-datalake-idn/indonesia_dw/dwd_risk_engine_cbi_src_report_di'
;

INSERT
    OVERWRITE TABLE indonesia_dw.dwd_risk_engine_cbi_src_report_di PARTITION (req_type='online', dt)
SELECT
    id,
    req_id,
    busi_account_id,
    create_at,
    datacache_create_time,
    scene,
    hitcache,
    is_found,
    account_id,
    create_time,
    status,
    error,
    message,
    result,
    dt
FROM
    (
        SELECT
            x.id,
            req_id,
            busi_account_id,
            create_at,
            datacache_create_time,
            scene,
            IF(
                ABS(datacache_create_time-create_time)<=120*1000,
                0,
                1
            ) AS hitcache,
            IF(account_id IS NOT NULL, 1, 0) AS is_found,
            account_id,
            create_time,
            status,
            error,
            message,
            '{"status": "'||status||'","error": "'||error||'","message": "'||message||'","result": '||result||'}' AS result,
            x.dt,
            ROW_NUMBER() OVER (
                PARTITION BY
                    req_id,
                    busi_account_id,
                    scene,
                    x.dt
                ORDER BY
                    create_time DESC
            ) rnk
        FROM
            (
                SELECT
                    -- *
                    id,
                    req_id,
                    busi_account_id,
                    create_at,
                    scene,
                    UNIX_TIMESTAMP(create_at, 'yyyy-MM-dd HH:mm:ss')*1000 AS datacache_create_time,
                    -- if(get_json_object(get_json_object(results, '$.data'), '$.message') = 'Tidak ada data yang ditemukan. Silakan periksa kembali parameter anda', 0, 1) as is_found,
                    dt
                FROM
                    indonesia_dw.dw_risk_engine_datacache_country_dt dc
                WHERE
                    dt>='2025-10-01'
                    AND dt<='2025-11-10'
                    -- dt >= '2025-04-08' and dt < '2025-07-01'
                    -- dt = '2025-04-08'
                    AND dc.country='indonesia'
                    AND dc.source_from='cbi'
                    AND dc.source_type IN ('report', 'report_v2')
            ) x
            LEFT JOIN (
                SELECT
                    *
                FROM
                    test_db.tmp_wqk_20250305_20251106_cbi_test_di
                WHERE
                    dt<='2025-11-10'
            ) y ON x.busi_account_id=y.account_id
            AND y.create_time<=x.datacache_create_time+1000*1
    ) xx
WHERE
    rnk=1
;