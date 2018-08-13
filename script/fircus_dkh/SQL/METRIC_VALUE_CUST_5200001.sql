
insert into METRIC_VALUE_CUST_0813_tmp
  (Metric_Value_Id,
   metric_id,
   time_dim,
   time_type,
   archives_id,
   area_id,
   spec_id,
   option_spec_id,
   metric_value,
   notes)
  with t as
   (select 5200001 metric_id,
           to_char(sysdate, 'YYYYMM') time_dim,
           2 time_type,
           m.cust_id archives_id,
           null as area_id,
           null as spec_id,
           null as option_spec_id,
           ROUND(COUNT(decode(m.is_out_time, 1, null, m.link_id)) /
                 count(m.link_id),
                 4) * 100 metric_value,
           '客户投诉的电路处理及时率' note
      FROM (SELECT l.link_id, l.cust_id, a.REGION_ID area_id, a.is_out_time
              from wta_topo_res_link l
              left join (SELECT a.info_id,
                               b.res_id,
                               a.REGION_ID,
                               a.is_out_time
                          FROM WTA_BCC_IMP_INFO a
                          JOIN WTA_BCC_IMP_INFO_RELA_RES b
                            ON a.info_id = b.info_id
                         WHERE a.res_type_id = 7637
                           AND b.res_id IS NOT NULL) a
                ON a.res_id = l.link_id
								where l.cust_id is not null ) m
     GROUP BY m.cust_id)
  select seq_METRIC_VALUE_CUST.nextval Metric_Value_Id, t.* from t;
	commit
;