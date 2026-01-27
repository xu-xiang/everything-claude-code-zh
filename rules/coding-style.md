# 代码风格 (Coding Style)

## 不可变性 (Immutability)（至关重要）

始终创建新对象，严禁修改原对象 (Mutation)：

```javascript
// 错误：修改原对象 (Mutation)
function updateUser(user, name) {
  user.name = name  // 直接修改了原对象！
  return user
}

// 正确：不可变性 (Immutability)
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## 文件组织

提倡“多而小”的文件，而非“少而大”的文件：
- 高内聚，低耦合
- 建议每文件 200-400 行，最大不超过 800 行
- 从大型组件中提取工具函数 (Utilities)
- 按功能/领域 (Feature/Domain) 组织，而非按类型 (Type) 组织

## 错误处理

始终进行全面的错误处理：

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('Operation failed:', error)
  throw new Error('Detailed user-friendly message')
}
```

## 输入校验

始终校验用户输入：

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

## 代码质量自检清单

在标记工作完成之前：
- [ ] 代码易读且命名良好
- [ ] 函数体量小（<50 行）
- [ ] 文件内容聚焦（<800 行）
- [ ] 无深度嵌套（>4 层）
- [ ] 具备完善的错误处理
- [ ] 不存在 console.log 语句
- [ ] 不存在硬编码 (Hardcoded) 数值
- [ ] 不存在修改原对象 (Mutation) 操作（已采用不可变模式）
