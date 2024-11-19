```
insert into temu_sku_detail_todo (create_time, last_time, goods_id, goods_name)
SELECT 
	now( ) AS create_time,
	create_time AS last_time,
	goods_id,
	title AS goods_name
FROM
	temu_sku;
```