-- Bj35 Bot v2 数据库结构
-- 版本号: 1.0.0
-- 创建日期: 2025-05-14
-- 作者: AptS:1547

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

-- 用户信息表
CREATE TABLE IF NOT EXISTS userinfo (
    uid SERIAL PRIMARY KEY,
    wecom TEXT,
    wecom_id TEXT,
    name TEXT,
    password TEXT,
    department TEXT,
    position TEXT,
    mobile TEXT,
    language TEXT,
    email TEXT,
    avatar_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为 userinfo 表创建更新触发器
CREATE TRIGGER update_userinfo_modtime
BEFORE UPDATE ON userinfo
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 目标位置表 - 存储系统中所有可用的位置信息
CREATE TABLE IF NOT EXISTS target_locations (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为 target_locations 表创建更新触发器
CREATE TRIGGER update_target_locations_modtime
BEFORE UPDATE ON target_locations
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 注: 上面的target_locations表对应settings.py中的TARGET_LIST

-- 此处可以添加更多表定义
-- 例如日志表、配置表等
