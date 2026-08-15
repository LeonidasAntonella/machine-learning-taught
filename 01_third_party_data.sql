--SQL
--********************************************************************--
-- author: hugo1
-- create time: 2025-10-31 16:08:42
--********************************************************************--


ADD jar obs://opay-datalake-idn/public_udf/hiveudf-1.3-SNAPSHOT.jar;

SELECT
    id AS user_account_id,
    MD5(UPPER(realname)) AS name_md5,  --- 姓名大写之后加密
    MD5(
        CAST(
            CONCAT(
                '62', substr(aes256cbc_decrypt_fun(mobile, mobile___key___iv), 2)
            ) AS BIGINT
        )
    ) AS mobile_md5, --- 合并上62变成 628 之后加密
    MD5(aes256cbc_decrypt_fun (`identity`, mobile___key___iv)) AS identity_md5  --- 身份证加密
FROM
    indonesia_ods.ods_microloan_account_base_df
WHERE
    dt='2025-11-06'
    AND is_deleted=0
    AND id IN (
        SELECT
            user_account_id
        FROM
            risk_data.ascore_clients_overall_dpd_req_id
        WHERE
            d40_10 IN (0, 1)
            AND req_dt>='2025-09-13'
            AND loan_dt<='2025-09-21'
    )
;



-----------

ADD jar obs://opay-datalake-idn/public_udf/hiveudf-1.3-SNAPSHOT.jar;

SELECT
    id AS user_account_id,
    MD5(
        CONCAT(
            '+62', substr(aes256cbc_decrypt_fun(mobile, mobile___key___iv), 2)
        )
    ) AS mobile_md5 --- 解密之后的电话格式为 8 开头，合并上+62变成 +628 之后加密
FROM
    indonesia_ods.ods_microloan_account_base_df
WHERE
    dt='2025-11-06'
    AND is_deleted=0
    AND id IN (
        SELECT
            user_account_id
        FROM
            risk_data.ascore_clients_overall_dpd_req_id
        WHERE
            d40_10 IN (0, 1)
            AND req_dt>='2025-06-05'
            AND loan_dt<='2025-09-21'
    )
;



-- SELECT
--     count(id) 
-- FROM
--     indonesia_ods.ods_microloan_account_base_df
-- WHERE
--     dt='2025-11-05'
--     AND is_deleted=0
--     AND id IN (
--         SELECT
--             user_account_id
--         FROM
--             risk_data.ascore_clients_overall_dpd_req_id
--         WHERE
--             d40_10 IN (0, 1)
--             AND req_dt>='2025-06-05'
--             AND loan_dt<='2025-09-21'
--     )
-- ;


----- digi score 
-- @张旭辉 digiscore的 产品回溯2w免费：  短信特征
-- 将测试样例发送至邮箱：xiajingjing@rong360.com
-- excel格式
-- 回溯测试格式 ：
-- name（姓名）,phone（手机号，去国号62， 8开头，AES加密）,idcard（证件号 AES加密）,npwp(税卡号，选填）、loan_dt（回溯时间 yyyy-mm-dd) 


add jar obs://opay-datalake-idn/public_udf/hiveudf-1.3-SNAPSHOT.jar;
create temporary function aes256cbc_decrypt as "com.opay.bigdata.Aes256cbcDecryptOldUdf";
create temporary function aes256cbc_encrypt as "com.opay.bigdata.Aes256cbcEncryptOldUdf";

SELECT
    id AS user_account_id,
    aes256cbc_encrypt (
        UPPER(realname),
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS name_aes, --- 姓名大写之后加密
    aes256cbc_encrypt (
        SUBSTR(
            aes256cbc_decrypt_fun (mobile, mobile___key___iv),
            2
        ),
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS mobile_aes, --- 去掉 0, 变成 8 开头的字符，再加密
    aes256cbc_encrypt (
        aes256cbc_decrypt_fun (`identity`, mobile___key___iv),
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS identity_aes --- 身份证加密
FROM
    indonesia_ods.ods_microloan_account_base_df
WHERE
    dt='2025-11-18'
    AND is_deleted=0
    AND id IN (
        SELECT
            user_account_id
        FROM
            risk_data.ascore_clients_overall_dpd_req_id
        WHERE
            d40_10 IN (0, 1)
            AND req_dt>='2025-09-13'
            AND loan_dt<='2025-09-21'
    )
;

-- 3206020606780004
-- 0895329326646
-- HENDI


add jar obs://opay-datalake-idn/public_udf/hiveudf-1.3-SNAPSHOT.jar;
create temporary function aes256cbc_decrypt as "com.opay.bigdata.Aes256cbcDecryptOldUdf";
create temporary function aes256cbc_encrypt as "com.opay.bigdata.Aes256cbcEncryptOldUdf";
SELECT
    aes256cbc_encrypt (
        UPPER('HENDI'),
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS name_aes, --- 姓名大写之后加密
    aes256cbc_encrypt (
        '895329326646',
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS mobile_aes, --- 去掉 0, 变成 8 开头的字符，再加密
    aes256cbc_encrypt (
        '3206020606780004',
        'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6',
        '1234567890123456'
    ) AS identity_aes --- 身份证加密
    ;




SELECT
    id AS user_account_id,
    MD5(
        CAST(
            CONCAT(
                '62', substr(aes256cbc_decrypt_fun(mobile, mobile___key___iv), 2)
            ) AS BIGINT
        )
    ) AS mobile_md5, --- 合并上62变成 628 之后加密
    MD5(aes256cbc_decrypt_fun (`identity`, mobile___key___iv)) AS identity_md5  --- 身份证加密
FROM
    indonesia_ods.ods_microloan_account_base_df
WHERE
    dt='2025-11-06'
    AND is_deleted=0
    AND id IN (
        SELECT
            user_account_id
        FROM
            risk_data.ascore_clients_overall_dpd_req_id
        WHERE
            d40_10 IN (0, 1)
            AND req_dt>='2025-09-13'
            AND loan_dt<='2025-09-21'
    )
;



SELECT
    id AS user_account_id,
    MD5(UPPER(realname)) AS name_md5,  --- 姓名大写之后加密
    MD5(
        CONCAT(
            '0', substr(aes256cbc_decrypt_fun(mobile, mobile___key___iv), 2)
        )
    ) AS mobile_md5, --- 合并上0变成 08 之后加密
    MD5(
        substr(aes256cbc_decrypt_fun(mobile, mobile___key___iv), 2)
    ) AS social_security_mobile_md5, --- 去掉0，变成8 之后加密
    MD5(aes256cbc_decrypt_fun (`identity`, mobile___key___iv)) AS identity_md5  --- 身份证加密
FROM
    indonesia_ods.ods_microloan_account_base_df
WHERE
    dt='2025-12-24'
    AND is_deleted=0
    AND id IN (
        SELECT
            user_account_id
        FROM
            risk_data.ascore_clients_overall_dpd_req_id
        WHERE
            d40_10 IN (0, 1)
            AND req_dt>='2025-09-13'
            AND loan_dt<='2025-09-21'
    )
;
