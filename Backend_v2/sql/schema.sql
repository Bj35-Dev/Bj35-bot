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

COMMENT ON COLUMN migrations.id IS '迁移ID';
COMMENT ON COLUMN migrations.version IS '迁移版本号';
COMMENT ON COLUMN migrations.applied_at IS '应用时间';
COMMENT ON COLUMN migrations.description IS '迁移描述';


-- 角色类型 - 用于存储用户角色
CREATE TYPE role_type AS ENUM (
    'superadmin', 'admin', 'user'
);

-- 用户信息表
CREATE TABLE IF NOT EXISTS userinfo (
    uid SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role role_type DEFAULT 'user',
    name TEXT,
    email TEXT,
    mobile TEXT,
    wecom_id TEXT,
    department TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN userinfo.uid IS '用户ID';
COMMENT ON COLUMN userinfo.username IS '用户名';
COMMENT ON COLUMN userinfo.password IS '密码';
COMMENT ON COLUMN userinfo.role IS '用户角色';
COMMENT ON COLUMN userinfo.name IS '用户名称';
COMMENT ON COLUMN userinfo.email IS '电子邮箱';
COMMENT ON COLUMN userinfo.mobile IS '手机号码';
COMMENT ON COLUMN userinfo.wecom_id IS '企业微信ID';
COMMENT ON COLUMN userinfo.department IS '部门';
COMMENT ON COLUMN userinfo.avatar_url IS '头像URL';
COMMENT ON COLUMN userinfo.created_at IS '创建时间';
COMMENT ON COLUMN userinfo.updated_at IS '更新时间';

-- 为 userinfo 表创建更新触发器
CREATE TRIGGER update_userinfo_modtime
BEFORE UPDATE ON userinfo
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 默认账户
INSERT INTO userinfo (username, password, role, name, email, mobile, wecom_id, department)
VALUES (
    'admin',
    '$argon2id$v=19$m=65536,t=3,p=4$chpaKFJG+eAWQsohRlqBcw$xfEARKtzemVIlkqM0FjeSUShTuJpgHNW+L6n0pMLkew',
    'superadmin',
    '管理员',
    'admin@example.com',
    '1234567890',
    'wecom_id', 
    'default_department'
)

-- 目标位置表 - 存储系统中所有可用的位置信息
CREATE TABLE IF NOT EXISTS target_locations (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN target_locations.id IS '位置ID';
COMMENT ON COLUMN target_locations.location IS '位置名称';
COMMENT ON COLUMN target_locations.description IS '位置描述';
COMMENT ON COLUMN target_locations.is_active IS '是否激活';
COMMENT ON COLUMN target_locations.created_at IS '创建时间';
COMMENT ON COLUMN target_locations.updated_at IS '更新时间';

-- 为 target_locations 表创建更新触发器
CREATE TRIGGER update_target_locations_modtime
BEFORE UPDATE ON target_locations
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 注: 上面的target_locations表对应settings.py中的TARGET_LIST

-- 此处可以添加更多表定义
-- 例如日志表、配置表等
