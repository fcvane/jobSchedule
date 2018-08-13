
--全国汇聚
insert into metric_gather_area_0813_tmp(gather_id,metric_id,time_dim,time_type,area_id,spec_id,option_spec_id,metric_value,note)
	with t as
 (SELECT 3200005 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         '000102000000000000004519' area_id,
         null as spec_id,
         null as option_spec_id,
         round(avg(to_number(t.FINISH_TIME - t.create_time) * 24), 2) metric_value,
         '全国统计投诉的电路平均处理时长' note
    FROM (SELECT a.FINISH_TIME, a.create_time
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                   FROM WTA_BCC_IMP_INFO a
                   JOIN WTA_BCC_IMP_INFO_RELA_RES b
                     ON a.info_id = b.info_id
                    and a.res_type_id = 7637) a
          
              ON a.res_id = l.link_id) t)
SELECT seq_metric_gather_area.nextval gather_id,
       t.METRIC_ID,
       t.TIME_DIM,
       t.TIME_TYPE,
       t.AREA_ID,
       t.SPEC_ID,
       t.OPTION_SPEC_ID,
       case
         when t.METRIC_VALUE is null then
          0
         else
          METRIC_VALUE
       end METRIC_VALUE,
       t.NOTE
  FROM t;




--------省份 汇聚

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
 (SELECT 3200005 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t.area_id area_id,
         null as spec_id,
         null as option_spec_id,
         avg(t.FINISH_TIME - t.create_time) metric_value,
         '省份统计投诉的电路平均处理时长' note
    FROM (SELECT a.FINISH_TIME, a.create_time, l.a_province_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                   FROM WTA_BCC_IMP_INFO a
                   JOIN WTA_BCC_IMP_INFO_RELA_RES b
                     ON a.info_id = b.info_id
                    and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.a_province_id is not null
          union
          SELECT a.FINISH_TIME, a.create_time, l.z_province_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                    FROM WTA_BCC_IMP_INFO a
                    JOIN WTA_BCC_IMP_INFO_RELA_RES b
                      ON a.info_id = b.info_id
                     and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.z_province_id is not null) t
   group by t.area_id)
SELECT seq_metric_gather_area.nextval gather_id,
       t.METRIC_ID,
       t.TIME_DIM,
       t.TIME_TYPE,
       t.AREA_ID,
       t.SPEC_ID,
       t.OPTION_SPEC_ID,
       case
         when t.METRIC_VALUE is null then
          0
         else
          METRIC_VALUE
       end METRIC_VALUE,
       t.NOTE
  FROM t;





--地市汇聚：
insert into metric_gather_area
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
 (SELECT 3200005 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t.area_id area_id,
         null as spec_id,
         null as option_spec_id,
         avg(t.FINISH_TIME - t.create_time) metric_value,
         '地市统计投诉的电路平均处理时长' note
    FROM (SELECT a.FINISH_TIME, a.create_time, l.a_city_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                   FROM WTA_BCC_IMP_INFO a
                   JOIN WTA_BCC_IMP_INFO_RELA_RES b
                     ON a.info_id = b.info_id
                    and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.a_city_id is not null
          union
          SELECT a.FINISH_TIME, a.create_time, l.z_city_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                    FROM WTA_BCC_IMP_INFO a
                    JOIN WTA_BCC_IMP_INFO_RELA_RES b
                      ON a.info_id = b.info_id
                     and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.z_city_id is not null) t
   group by t.area_id)
SELECT seq_metric_gather_area.nextval gather_id,
       t.METRIC_ID,
       t.TIME_DIM,
       t.TIME_TYPE,
       t.AREA_ID,
       t.SPEC_ID,
       t.OPTION_SPEC_ID,
       case
         when t.METRIC_VALUE is null then
          0
         else
          METRIC_VALUE
       end METRIC_VALUE,
       t.NOTE
  FROM t;



---区县 汇聚
insert into metric_gather_area
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
 (SELECT 3200005 metric_id,
         to_char(sysdate, 'YYYYMM') time_dim,
         2 time_type,
         t.area_id area_id,
         null as spec_id,
         null as option_spec_id,
         avg(t.FINISH_TIME - t.create_time) metric_value,
         '区县统计投诉的电路平均处理时长' note
    FROM (SELECT a.FINISH_TIME, a.create_time, l.a_country_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                   FROM WTA_BCC_IMP_INFO a
                   JOIN WTA_BCC_IMP_INFO_RELA_RES b
                     ON a.info_id = b.info_id
                    and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.a_country_id is not null
          union
          SELECT a.FINISH_TIME, a.create_time, l.z_country_id area_id
            from wta_topo_res_link l
            join (SELECT a.FINISH_TIME, a.create_time, b.res_id
                    FROM WTA_BCC_IMP_INFO a
                    JOIN WTA_BCC_IMP_INFO_RELA_RES b
                      ON a.info_id = b.info_id
                     and a.res_type_id = 7637) a
              ON a.res_id = l.link_id
           where l.z_country_id is not null) t
   group by t.area_id)
SELECT seq_metric_gather_area.nextval gather_id,
       t.METRIC_ID,
       t.TIME_DIM,
       t.TIME_TYPE,
       t.AREA_ID,
       t.SPEC_ID,
       t.OPTION_SPEC_ID,
       case
         when t.METRIC_VALUE is null then
          0
         else
          METRIC_VALUE
       end METRIC_VALUE,
       t.NOTE
  FROM t;
