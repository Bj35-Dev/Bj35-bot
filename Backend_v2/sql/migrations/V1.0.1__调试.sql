-- Bj35 Bot v2 数据库结构
-- 版本号: 1.0.1
-- 创建日期: 2025-05-14
-- 作者: AptS:1547
-- 这是一个测试 migration 的文件

DROP TABLE IF EXISTS test_table;
CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE test_table
ADD COLUMN description TEXT;

DROP TABLE IF EXISTS test_table;

-- 迁移系统使用示例