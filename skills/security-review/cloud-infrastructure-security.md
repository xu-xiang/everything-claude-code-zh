| name | description |
|------|-------------|
| cloud-infrastructure-security | 当部署到云平台、配置基础设施、管理 IAM 策略、设置日志/监控或实现 CI/CD 流水线时，请使用此技能。提供符合最佳实践的云安全检查清单。 |

# 云与基础设施安全技能 (Cloud & Infrastructure Security Skill)

此技能旨在确保云基础设施、CI/CD 流水线（CI/CD Pipeline）和部署配置遵循安全最佳实践，并符合行业标准。

## 何时激活

- 将应用程序部署到云平台（AWS, Vercel, Railway, Cloudflare）
- 配置身份与访问管理（IAM）角色和权限
- 设置 CI/CD 流水线（CI/CD Pipeline）
- 实现基础设施即代码（Infrastructure as Code, IaC，如 Terraform, CloudFormation）
- 配置日志记录（Logging）与监控（Monitoring）
- 在云环境中管理机密（Secrets）
- 设置 CDN 与边缘安全
- 实现容灾（Disaster Recovery）与备份策略

## 云安全检查清单

### 1. IAM 与访问控制 (IAM & Access Control)

#### 最小特权原则 (Principle of Least Privilege)

```yaml
# ✅ 正确：最小权限
iam_role:
  permissions:
    - s3:GetObject  # 仅读取权限
    - s3:ListBucket
  resources:
    - arn:aws:s3:::my-bucket/*  # 仅限特定存储桶

# ❌ 错误：权限过大
iam_role:
  permissions:
    - s3:*  # 所有 S3 操作
  resources:
    - "*"  # 所有资源
```

#### 多因素身份验证 (Multi-Factor Authentication, MFA)

```bash
# 务必为 root/管理员账户启用 MFA
aws iam enable-mfa-device \
  --user-name admin \
  --serial-number arn:aws:iam::123456789:mfa/admin \
  --authentication-code1 123456 \
  --authentication-code2 789012
```

#### 验证步骤

- [ ] 生产环境中不使用 root 账户
- [ ] 所有特权账户均启用 MFA
- [ ] 服务账号（Service accounts）使用角色（Roles），而非长期凭据
- [ ] IAM 策略遵循最小特权原则
- [ ] 定期进行访问权限审查
- [ ] 轮换或移除未使用的凭据

### 2. 机密管理 (Secrets Management)

#### 云端机密管理器 (Cloud Secrets Managers)

```typescript
// ✅ 正确：使用云端机密管理器
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManager({ region: 'us-east-1' });
const secret = await client.getSecretValue({ SecretId: 'prod/api-key' });
const apiKey = JSON.parse(secret.SecretString).key;

// ❌ 错误：硬编码或仅存在于环境变量中
const apiKey = process.env.API_KEY; // 无法轮换，无法审计
```

#### 机密轮换 (Secrets Rotation)

```bash
# 为数据库凭据设置自动轮换
aws secretsmanager rotate-secret \
  --secret-id prod/db-password \
  --rotation-lambda-arn arn:aws:lambda:region:account:function:rotate \
  --rotation-rules AutomaticallyAfterDays=30
```

#### 验证步骤

- [ ] 所有机密均存储在云端机密管理器中（如 AWS Secrets Manager, Vercel Secrets）
- [ ] 数据库凭据已启用自动轮换
- [ ] API 密钥至少每季度轮换一次
- [ ] 代码、日志或错误消息中不包含机密
- [ ] 已为机密访问启用审计日志

### 3. 网络安全 (Network Security)

#### VPC 与防火墙配置 (VPC and Firewall Configuration)

```terraform
# ✅ 正确：受限的安全组
resource "aws_security_group" "app" {
  name = "app-sg"
  
ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # 仅限内部 VPC
  }
  
egres s {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 仅允许 HTTPS 出站
  }
}

# ❌ 错误：对互联网开放
resource "aws_security_group" "bad" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 所有端口，所有 IP！
  }
}
```

#### 验证步骤

- [ ] 数据库不可通过公网访问
- [ ] SSH/RDP 端口仅限制在 VPN/堡垒机访问
- [ ] 安全组遵循最小特权原则
- [ ] 已配置网络 ACL（Network ACLs）
- [ ] 已启用 VPC 流日志（VPC flow logs）

### 4. 日志记录与监控 (Logging & Monitoring)

#### CloudWatch/日志配置 (CloudWatch/Logging Configuration)

```typescript
// ✅ 正确：全面的日志记录
import { CloudWatchLogsClient, CreateLogStreamCommand } from '@aws-sdk/client-cloudwatch-logs';

const logSecurityEvent = async (event: SecurityEvent) => {
  await cloudwatch.putLogEvents({
    logGroupName: '/aws/security/events',
    logStreamName: 'authentication',
    logEvents: [{
      timestamp: Date.now(),
      message: JSON.stringify({
        type: event.type,
        userId: event.userId,
        ip: event.ip,
        result: event.result,
        // 严禁记录敏感数据
      })
    }]
  });
};
```

#### 验证步骤

- [ ] 所有服务均启用了 CloudWatch/日志记录
- [ ] 已记录失败的身份验证尝试
- [ ] 管理员操作已审计
- [ ] 已配置日志保留策略（合规性要求通常为 90 天以上）
- [ ] 为可疑活动配置了告警
- [ ] 日志采用集中化存储且具备防篡改能力

### 5. CI/CD 流水线安全 (CI/CD Pipeline Security)

#### 安全流水线配置 (Secure Pipeline Configuration)

```yaml
# ✅ 正确：安全的 GitHub Actions 工作流
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read  # 最小权限
      
    steps:
      - uses: actions/checkout@v4
      
      # 扫描机密
      - name: Secret scanning
        uses: trufflesecurity/trufflehog@main
        
      # 依赖项审计
      - name: Audit dependencies
        run: npm audit --audit-level=high
        
      # 使用 OIDC，而非长期令牌
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: us-east-1
```

#### 供应链安全 (Supply Chain Security)

```json
// package.json - 使用 lock 文件和完整性检查
{
  "scripts": {
    "install": "npm ci",  // 使用 ci 以获得可复现的构建
    "audit": "npm audit --audit-level=moderate",
    "check": "npm outdated"
  }
}
```

#### 验证步骤

- [ ] 使用 OIDC 代替长期凭据
- [ ] 在流水线中进行机密扫描
- [ ] 依赖项漏洞扫描
- [ ] 容器镜像扫描（如适用）
- [ ] 强制执行分支保护规则
- [ ] 合并前必须进行代码审查
- [ ] 强制执行签名提交（Signed commits）

### 6. Cloudflare 与 CDN 安全 (Cloudflare & CDN Security)

#### Cloudflare 安全配置

```typescript
// ✅ 正确：带有安全响应头的 Cloudflare Workers
export default {
  async fetch(request: Request): Promise<Response> {
    const response = await fetch(request);
    
    // 添加安全响应头
    const headers = new Headers(response.headers);
    headers.set('X-Frame-Options', 'DENY');
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('Permissions-Policy', 'geolocation=(), microphone=()');
    
    return new Response(response.body, {
      status: response.status,
      headers
    });
  }
};
```

#### WAF 规则

```bash
# 启用 Cloudflare WAF 托管规则
# - OWASP 核心规则集
# - Cloudflare 托管规则集
# - 速率限制规则
# - 机器人保护
```

#### 验证步骤

- [ ] 已启用 WAF 并配置了 OWASP 规则
- [ ] 已配置速率限制（Rate limiting）
- [ ] 机器人保护（Bot protection）已激活
- [ ] 已启用 DDoS 防护
- [ ] 已配置安全响应头
- [ ] 已启用 SSL/TLS 严格模式

### 7. 备份与容灾 (Backup & Disaster Recovery)

#### 自动化备份

```terraform
# ✅ 正确：RDS 自动化备份
resource "aws_db_instance" "main" {
  allocated_storage     = 20
  engine               = "postgres"
  
  backup_retention_period = 30  # 保留 30 天
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  
  deletion_protection = true  # 防止误删
}
```

#### 验证步骤

- [ ] 已配置每日自动化备份
- [ ] 备份保留时间符合合规性要求
- [ ] 已启用时间点恢复（Point-in-time recovery）
- [ ] 每季度进行备份测试
- [ ] 已记录容灾计划文档
- [ ] 已定义并测试 RPO（恢复点目标）和 RTO（恢复时间目标）

## 部署前云安全检查表 (Pre-Deployment Cloud Security Checklist)

在任何生产环境云部署之前：

- [ ] **IAM**：不使用 root 账户，启用 MFA，执行最小特权策略
- [ ] **机密 (Secrets)**：所有机密均存放在带轮换机制的云端机密管理器中
- [ ] **网络 (Network)**：受限的安全组，无公网数据库
- [ ] **日志 (Logging)**：启用带保留策略的 CloudWatch/日志记录
- [ ] **监控 (Monitoring)**：为异常活动配置告警
- [ ] **CI/CD**：OIDC 认证、机密扫描、依赖项审计
- [ ] **CDN/WAF**：启用带 OWASP 规则的 Cloudflare WAF
- [ ] **加密 (Encryption)**：数据在静态（at rest）和传输（in transit）中均已加密
- [ ] **备份 (Backups)**：带有恢复测试的自动化备份
- [ ] **合规性 (Compliance)**：满足 GDPR/HIPAA 等要求（如适用）
- [ ] **文档 (Documentation)**：基础设施已记录文档，创建了运行手册（Runbooks）
- [ ] **事件响应 (Incident Response)**：已制定安全事件响应计划

## 常见的云安全错误配置 (Common Cloud Security Misconfigurations)

### S3 存储桶暴露

```bash
# ❌ 错误：公共存储桶
aws s3api put-bucket-acl --bucket my-bucket --acl public-read

# ✅ 正确：具有特定访问权限的私有存储桶
aws s3api put-bucket-acl --bucket my-bucket --acl private
aws s3api put-bucket-policy --bucket my-bucket --policy file://policy.json
```

### RDS 公网访问

```terraform
# ❌ 错误
resource "aws_db_instance" "bad" {
  publicly_accessible = true  # 绝不要这样做！
}

# ✅ 正确
resource "aws_db_instance" "good" {
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.db.id]
}
```

## 资源 (Resources)

- [AWS 安全最佳实践](https://aws.amazon.com/security/best-practices/)
- [CIS AWS 基础基准](https://www.cisecurity.org/benchmark/amazon_web_services)
- [Cloudflare 安全文档](https://developers.cloudflare.com/security/)
- [OWASP 云安全](https://owasp.org/www-project-cloud-security/)
- [Terraform 安全最佳实践](https://www.terraform.io/docs/cloud/guides/recommended-practices/)

**请记住**：云端配置错误是导致数据泄露的主要原因。一个暴露的 S3 存储桶或权限过大的 IAM 策略就可能危害您的整个基础设施。请务必遵循最小特权原则和纵深防御原则。
