-- Bj35 Bot v2 数据库结构
-- 版本号: 1.0.1
-- 创建日期: 2025-05-17
-- 作者: AptS:1547
-- 本文件定义了任务记录表的结构

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
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_target_locations_modtime') THEN
        CREATE TRIGGER update_target_locations_modtime
        BEFORE UPDATE ON target_locations
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_column();
    END IF;
END$$;

-- 任务记录表 - 存储所有任务的记录
CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN task_history.id IS '记录ID';
COMMENT ON COLUMN task_history.task_id IS '任务ID';
COMMENT ON COLUMN task_history.user_id IS '用户ID';
COMMENT ON COLUMN task_history.status IS '任务状态';
COMMENT ON COLUMN task_history.created_at IS '创建时间';
COMMENT ON COLUMN task_history.updated_at IS '更新时间';

-- 为 task_history 表创建更新触发器
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_task_history_modtime') THEN
        CREATE TRIGGER update_task_history_modtime
        BEFORE UPDATE ON task_history
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_column();
    END IF;
END$$;
