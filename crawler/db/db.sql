create schema apesk1 collate utf8_bin;

create table advantage_item
(
	advantage_name varchar(50) null,
	advantage_desc varchar(1000) null comment 'xxx的盖洛普五项优势',
	advantage_desc_more_info varchar(20000) null comment '思维'
)
comment '记录36项优势的描述';

create table advantage_score_item
(
	id int null comment '评估人id',
	name varchar(500) null comment '评估人姓名',
	submit_time varchar(50) null comment '提交时间',
	advantage_id int null comment '优势id',
	advantage_name varchar(100) null comment '优势名称',
	score int null comment '分数',
	url varchar(200) null comment 'url字段',
	constraint advantage_score_item_id_advantage_id_uindex
		unique (id, advantage_id)
)
comment '记录评估人的每一项优势与分数';

