--带参数的hql
use test_db;
select * from test0828 where dt='${hivevar:v_date}';