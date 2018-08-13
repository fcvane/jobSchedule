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
   (select 5210005 metric_id,
           to_char(sysdate, 'YYYYMM') time_dim,
           2 time_type,
           m.CUST_MANAGER_id archives_id,
           null as area_id,
           null as spec_id,
           null as option_spec_id,
           COUNT(m.link_id) metric_value,
           '以客户经理为维度，统计故障的电路数量' note
      FROM (SELECT t.link_id,
                   t.cust_id,
                   t.is_out_time,
                   t.area_id,
                   q.CUST_MANAGER_id
              FROM (SELECT l.link_id,
                           l.cust_id,
                           a.REGION_ID area_id,
                           a.is_out_time
                      from wta_topo_res_link l
                       join (SELECT a.info_id,
                                       b.res_id,
                                       a.REGION_ID,
                                       a.is_out_time
                                  FROM WTA_BCC_IMP_INFO a
                                  LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                    ON a.info_id = b.info_id
                                 WHERE a.res_type_id = 173
                                   AND b.res_id IS NOT NULL) a
                        ON a.res_id = l.link_id ) t
               JOIN pub_cust q
                ON t.cust_id = q.cust_id) m
     GROUP BY m.CUST_MANAGER_id)
  select seq_METRIC_VALUE_CUST.nextval Metric_Value_Id, t.* from t;
commit;