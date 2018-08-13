--全国,汇聚
insert into metric_gather_area_0813_tmp(gather_id,metric_id,time_dim,time_type,area_id,spec_id,option_spec_id,metric_value,note)
with t as
 (SELECT 3210008 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         '000102000000000000004519' area_id,
         null as spec_id,
         null option_spec_id,
         COUNT(distinct t.cust_id) metric_value,
         '全国统计告警电路客户数' note
    FROM (SELECT l.cust_id
            from wta_topo_res_link l
            left join (SELECT a.info_id, b.res_id
                        FROM WTA_BCC_IMP_INFO a
                        LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                          ON a.info_id = b.info_id
                       WHERE a.res_type_id = 672
                         AND b.res_id IS NOT NULL) a
              on a.res_id = l.link_id) t
   group by '000102000000000000004519')
SELECT seq_metric_gather_area.nextval gather_id, t.* FROM t;

--省份,汇聚
insert into metric_gather_area_0813_tmp
  (gather_id,
   metric_id,
   time_dim,
   time_type,
   area_id,
   spec_id,
   option_spec_id,
   metric_value,
   note)
  with t as
 (SELECT 3210008 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t. area_id,
         null as spec_id,
         null option_spec_id,
         COUNT(distinct t.cust_id) metric_value,
         '省份统计告警电路客户数' note
    FROM (SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.a_province_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                  
                      ON a.res_id = l.link_id
                   where l.a_province_id is not null) t
          
          UNION
          SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.z_province_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                  
                      ON a.res_id = l.link_id
                   where l.z_province_id is not null) t) t
   GROUP BY t.area_id)
SELECT seq_metric_gather_area.nextval gather_id, t.* FROM t;


---地市 汇聚
insert into metric_gather_area_0813_tmp
  (gather_id,
   metric_id,
   time_dim,
   time_type,
   area_id,
   spec_id,
   option_spec_id,
   metric_value,
   note)
  with t as
 (SELECT 3210008 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t. area_id,
         null as spec_id,
         null option_spec_id,
         COUNT(distinct t.cust_id) metric_value,
         '地市统计告警电路客户数' note
    FROM (SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.a_city_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                  
                      ON a.res_id = l.link_id
                   where l.a_city_id is not null) t
          
          UNION
          SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.z_city_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                      ON a.res_id = l.link_id
                   where l.z_city_id is not null) t) t
   GROUP BY t.area_id)
SELECT seq_metric_gather_area.nextval gather_id, t.* FROM t;


      

-------区县 ，汇聚
insert into metric_gather_area_0813_tmp
  (gather_id,
   metric_id,
   time_dim,
   time_type,
   area_id,
   spec_id,
   option_spec_id,
   metric_value,
   note)
  with t as
 (SELECT 3210008 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t. area_id,
         null as spec_id,
         null option_spec_id,
         COUNT(distinct t.cust_id) metric_value,
         '区县统计告警电路客户数' note
    FROM (SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.a_country_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                  
                      ON a.res_id = l.link_id
                   where l.a_country_id is not null) t
          
          UNION
          SELECT t.link_id, t.cust_id, t.area_id
            FROM (SELECT l.link_id, l.cust_id, l.z_country_id area_id
                    from wta_topo_res_link l
                    left join (SELECT a.info_id, b.res_id
                                FROM WTA_BCC_IMP_INFO a
                                LEFT JOIN WTA_BCC_IMP_INFO_RELA_RES b
                                  ON a.info_id = b.info_id
                               WHERE a.res_type_id = 672
                                 AND b.res_id IS NOT NULL) a
                  
                      ON a.res_id = l.link_id
                   where l.z_country_id is not null) t) t
   GROUP BY t.area_id)
SELECT seq_metric_gather_area.nextval gather_id, t.* FROM t;