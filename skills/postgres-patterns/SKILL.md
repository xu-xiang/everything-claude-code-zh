---
name: postgres-patterns
description: PostgreSQL 数据库模式，涵盖查询优化、模式设计、索引和安全性。基于 Supabase 最佳实践。
---

# PostgreSQL 模式（Patterns）

PostgreSQL 最佳实践快速参考。如需详细指导，请使用 `database-reviewer` 智能体（Agent）。

## 何时激活

- 编写 SQL 查询或迁移（Migrations）
- 设计数据库模式（Schemas）
- 排除慢查询故障
- 实现行级安全性（Row Level Security, RLS）
- 设置连接池（Connection Pooling）

## 快速参考

### 索引备忘单（Index Cheat Sheet）

| 查询模式 | 索引类型 | 示例 |
|--------------|------------|---------|
| `WHERE col = value` | B-tree（默认） | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | 复合索引（Composite） | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| 时序范围（Time-series ranges） | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### 数据类型快速参考

| 用例 | 正确类型 | 避免使用 |
|----------|-------------|-------|
| ID | `bigint` | `int`, 随机 UUID |
| 字符串 | `text` | `varchar(255)` |
| 时间戳 | `timestamptz` | `timestamp` |
| 金额 | `numeric(10,2)` | `float` |
| 标志位（Flags） | `boolean` | `varchar`, `int` |

### 常用模式

**复合索引顺序：**
```sql
-- 等值列（Equality columns）在前，范围列（Range columns）在后
CREATE INDEX idx ON orders (status, created_at);
-- 适用于：WHERE status = 'pending' AND created_at > '2024-01-01'
```

**覆盖索引（Covering Index）：**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- 避免在执行 SELECT email, name, created_at 时进行表查找（Table lookup）
```

**部分索引（Partial Index）：**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- 索引体积更小，仅包含活动用户
```

**RLS 策略（已优化）：**
```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- 包裹在 SELECT 中！
```

**UPSERT（更新插入）：**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**游标分页（Cursor Pagination）：**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) 复杂度，对比 OFFSET 的 O(n) 复杂度
```

**队列处理：**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

### 反模式（Anti-Pattern）检测

```sql
-- 查找未建立索引的外键
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- 查找慢查询
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- 检查表膨胀（Table bloat）
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### 配置模板

```sql
-- 连接限制（根据 RAM 调整）
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- 超时设置
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- 监控
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 安全默认设置
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## 相关内容

- 智能体（Agent）：`database-reviewer` - 完整的数据库审查工作流
- 技能（Skill）：`clickhouse-io` - ClickHouse 分析模式
- 技能（Skill）：`backend-patterns` - API 和后端模式

---

*基于 [Supabase Agent Skills](https://github.com/supabase/agent-skills) (MIT 许可证)*
