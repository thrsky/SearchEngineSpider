-- msql数据库初始化脚本

-- 新建数据库
CREATE database articleSpider;

use articleSpider;

create table jobbole_article(
  `title` VARCHAR(200) NOT NULL COMMENT '标题',
  `create_date` DATE COMMENT '时间',
  `url` VARCHAR(300) NOT NULL COMMENT '文章URL',
  `url_object_id` VARCHAR(50) NOT NULL COMMENT '加密后的文章URL',
  `front_image_url` VARCHAR(300),
  `front_image_path` VARCHAR(200) COMMENT '图片存储路径',
  `zan` INT(11) DEFAULT 0 COMMENT '点赞数',
  `remark` INT(11) DEFAULT 0 COMMENT '评论数',
  `collect` INT(11) DEFAULT 0 COMMENT '收藏数',
  `tags` VARCHAR(255) COMMENT '文章标签',
  `content` LONGTEXT COMMENT '文章正文',
  PRIMARY KEY (url_object_id)
)ENGINE = InnoDB DEFAULT CHARSET=utf8