-- Bj35 Bot v2 数据库结构
-- 版本号: 1.0.0
-- 创建日期: 2025-05-17
-- 作者: AptS:1547
-- 说明: 此文件仅包含基础结构，详细表定义已移至迁移文件

-- 创建自动更新 updated_at 的触发器函数
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 迁移版本表 - 用于跟踪数据库结构的版本
CREATE TABLE IF NOT EXISTS migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL UNIQUE,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- 注: 详细表结构定义已移至迁移文件目录 sql/migrations/
-- 初始结构: V1.0.0__init_schema.sql
-- 任务记录功能: V1.0.1__添加任务记录功能.sql
