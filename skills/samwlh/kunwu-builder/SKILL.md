# Kunwu Builder 控制技能

控制 Kunwu Builder (坤吾) 工业仿真软件的 HTTP API。

## 基础信息

- **软件名称**: Kunwu Builder (坤吾)
- **API 地址**: `http://127.0.0.1:16888`
- **认证方式**: 无（本地访问）
- **请求方式**: POST (HTTP)
- **Content-Type**: application/json

## 工具

### `kunwu_call`

调用 Kunwu Builder HTTP API。

**参数:**
- `endpoint` (string, 必填): API 端点路径，如 `/model/create`
- `method` (string, 可选): HTTP 方法，默认 `POST`
- `data` (object, 可选): 请求体 JSON 数据

**返回:** API 响应 JSON

## 功能分类

### 1. 模型管理
- 创建模型 (`/model/create`)
- 设置姿态 (`/model/set_pose`)
- 渲染颜色 (`/model/set_render`)
- 导出模型 (`/model/export`)
- 获取属性 (`/GetModelInfo`, `/GetAllModelInfo`)
- 获取层级树 (`/models/tree`)
- 获取场景 JSON (`/scene/get_scene_json`)
- 设置层级关系 (`/model/set_parent`) - 父子关系/解除关系
- 销毁物体 (`/model/destroy`) - 支持批量销毁
- 销毁组件 (`/model/destroy_component`)
- 装配 (`/model/assemble`) - 装配到指定位置

### 2. 机器人控制
- 获取位姿 (`/query/robot_pos`, `/GetRobotLink`)
- 设置位姿 (`/SetRobotLink`)
- 获取轨迹 (`/GetRobotTrackInfo`)
- 逆解计算 (`/RobotSolveIK`)
- 附加轴 (`/GetRobotExtraLink`, `/GetGroundTrackInfo`)
- 连续运动点 (`/motion/ConsecutiveWalkPoints`)

### 3. 物流设备
- 内置设备 (`/motion/IndustrialEquipment`)
- 自定义设备 (`/motion/CustomEquipmentCommand`, `/motion/CustomEquipmentQuery`)
- 到位信号 (`/motion/rollbed`)
- 传送带距离 (`/GetConveyorMoveDistance`)

### 4. 相机设备
- 拍照 (`/sbt/sensor`) - 支持原始图、深度图、点云
- 相机列表 (`/sensor/queryCameralist`)

### 5. 传感器与物流
- 传感器状态 (`/logistic/sensor`, `/GetSensorStatus`)
- 零件到位 (`/logistic/steel`)
- 编码器值 (`/logistic/encoder`)

### 6. 场景管理
- 重置场景 (`/ResetScene`)
- 切换模式 (`/ChangeMode`) - 0:场景构建 1:行为信号 2:机器人 3:数字孪生
- 导入 CAD (`/import/cad_2d`)
- 更新碰撞 (`/UpdateCollider`)
- 创建点位 (`/CreatePoints`)
- 场景提示 (`/SceneTipsShow`)
- **获取场景 JSON** (`/scene/get_scene_json`) - 2026-03-14 新增解析函数

### 7. 行为控制（2026-03-14 更新）
- 添加/更新行为 (`/behavior/add`) - 支持从属运动 (`dependentTargetId`)
- 获取行为参数 (`/behavior/get`)
- 获取行为配置列表 (`/behavior/list`) - 新增，获取模型及子节点的行为配置
- 删除行为 (`/behavior/delete`)
- **Helper 函数**: 
  - `createRotaryJoint()` - 支持从属旋转
  - `createLinearJoint()` - 支持从属直线运动
  - `createLinearJointWithDependent()` - 便捷创建从动臂
  - `createBoxJoint()` - 参数化方形
  - `getBehaviorList()` - 获取行为配置列表

### 8. 进度与提示（新增）
- AI 场景进度 (`/ShowGenerateSceneProgress`)
- 通用进度条 (`/view/show_progress`)

### 9. 批量执行（新增）
- 批量执行接口 (`/batch/execute`) - 原子执行多个命令

### 10. 排产接口（新增）
- 排产结果回传 (`/scheduling/return_result`)

### 11. 模型库管理（2026-03-13 更新 - 已验证✅）
- 获取本地模型库 (`/model/library/local`) - 支持模糊搜索
- 获取远程模型库 (`/model/library/remote`) - 556+ 云端模型
- 下载模型 (`/model/download`) - 可自动创建到场景
- 删除本地模型 (`/model/library/delete`)
- 获取分类列表 (`/model/library/categories`)
- 收藏模型 (`/model/library/favorite`)
- 获取收藏列表 (`/model/library/favorites`)

## 使用示例

### 基础操作

**创建模型**
```
kunwu_call endpoint="/model/create" data='{"id":"纸箱","rename":"纸箱_01","position":[10,20,30],"eulerAngle":[10,0,0]}'
```

**创建参数化方形模型**（2026-03-14 更新）
```
// 2 个参数（长、宽）- 方形模型默认支持
kunwu_call endpoint="/model/create" data='{"id":"方形","rename":"我的方形","position":[0,0,0],"eulerAngle":[0,0,0],"parameterizationCfg":[{"type":0,"value":2000},{"type":1,"value":1000}]}'

// 3 个参数（长、宽、高）- 如果模型支持
kunwu_call endpoint="/model/create" data='{"id":"方形","rename":"我的方形","position":[0,0,0],"eulerAngle":[0,0,0],"parameterizationCfg":[{"type":0,"value":2000},{"type":1,"value":1000},{"type":2,"value":500}]}'
```

**控制辊床**
```
kunwu_call endpoint="/motion/IndustrialEquipment" data='{"id":"conveyer1","type":0,"command":1,"data":{"target":"1-3"}}'
```

**相机拍照**
```
kunwu_call endpoint="/sbt/sensor" data='{"id":"camera1","type":1}'
```

**获取机器人位姿**
```
kunwu_call endpoint="/GetRobotLink" data='{"id":"r1"}'
```

### 模型库操作（2026-03-13 更新）

**查询云端模型库**
```
kunwu_call endpoint="/model/library/remote" data='{"pageNum":1,"pageSize":10}'
```

**模糊搜索本地模型**
```
kunwu_call endpoint="/model/library/local" data='{"name":"robot","fuzzy":true}'
```

**下载模型并创建到场景**
```
kunwu_call endpoint="/model/download" data='{"id":"纸箱","createInScene":true,"position":[0,0,0],"eulerAngle":[0,0,0],"rename":"my_box"}'
```

### 层级与销毁（2026-03-13 更新）

**设置父子关系**
```
kunwu_call endpoint="/model/set_parent" data='{"childId":"子物体 modelId","parentId":"父物体 modelId","childUseModeId":true,"parentUseModeId":true}'
```

**解除父子关系**
```
kunwu_call endpoint="/model/set_parent" data='{"childId":"子物体 modelId","parentId":null,"childUseModeId":true}'
```

**销毁单个物体**
```
kunwu_call endpoint="/model/destroy" data='{"id":"物体 modelId","useModeId":true}'
```

**批量销毁物体**
```
kunwu_call endpoint="/model/destroy" data='{"ids":["modelId1","modelId2"],"useModeId":true}'
```

### 高级功能

**批量执行命令**
```
kunwu_call endpoint="/batch/execute" data='{"atomic":true,"stopOnError":false,"commands":[{"url":"/GetModelInfo","body":{"id":"Cube"}},{"url":"/models/tree","body":{"rootId":"scene"}}]}'
```

**添加行为组件**
```
kunwu_call endpoint="/behavior/add" data='{"id":"model_001","behavioralType":1,"referenceAxis":0,"minValue":-1000,"maxValue":1000,"runSpeed":200}'
```

**装配到指定位置**
```
kunwu_call endpoint="/model/assemble" data='{"id":"零件","targetId":"装配位置","offset":[0,0,0,0,0,0]}'
```

### 场景 JSON 解析（2026-03-14 更新）

**获取场景 JSON**（软件已修复，直接返回对象）
```javascript
// 直接使用 getSceneJson() - 已自动解析
const scene = await getSceneJson();
console.log(scene.AppVersion);  // "1.4.4"
console.log(scene.modeldataList);  // 模型数组
console.log(scene.sceneCameraTransformData);  // 相机位置
console.log(scene.processFlowGroupDataList);  // 流程数据
console.log(scene.workflowTableDataList);  // 工作流数据
```

**说明：**
- 软件修复前：返回字符串，需要手动 `JSON.parse()` 并处理 `Infinity`/`NaN`
- 软件修复后：直接返回已解析的对象，无需额外处理
- `getSceneJsonParsed()` 作为别名保留，兼容旧代码

### 夹具行为配置（2026-03-14 新增，2026-03-14 18:50 更新）

**完整指南：从结构分析到配置**

#### 步骤 1: 获取夹具层级结构

```javascript
const tree = await callAPI('/models/tree', { rootId: 'scene', useModeId: true, includeRoot: true });

// 查找目标夹具
function findGripper(models, name) {
  for (const m of models) {
    if (m.modelName === name) return m;
    if (m.children) {
      const found = findGripper(m.children, name);
      if (found) return found;
    }
  }
  return null;
}

const gripper = findGripper(tree.data.models, 'DH_PGE_100_26');
console.log('子节点:', gripper.children.map(c => c.modelName));
```

#### 步骤 2: 分析结构确定轴向和行程

```javascript
// 分析两个夹爪的相对位置
const child1 = gripper.children[0];
const child2 = gripper.children[1];

const dx = child2.transform[0] - child1.transform[0];
const dy = child2.transform[1] - child1.transform[1];
const dz = child2.transform[2] - child1.transform[2];

// 判断主要轴向
const absDx = Math.abs(dx), absDy = Math.abs(dy), absDz = Math.abs(dz);
const maxDelta = Math.max(absDx, absDy, absDz);

let axis;
if (maxDelta === absDx) axis = dx > 0 ? ReferenceAxis.X_POSITIVE : ReferenceAxis.X_NEGATIVE;
else if (maxDelta === absDy) axis = dy > 0 ? ReferenceAxis.Y_POSITIVE : ReferenceAxis.Y_NEGATIVE;
else axis = dz > 0 ? ReferenceAxis.Z_POSITIVE : ReferenceAxis.Z_NEGATIVE;

// 计算行程（基于 boundSize 的 1/3）
const axisIndex = [0, 1, 2][maxDelta === absDx ? 0 : maxDelta === absDy ? 1 : 2];
const travel = child1.boundSize[axisIndex];
const minVal = 0;
const maxVal = Math.round(travel / 3);  // 33% boundSize（经验值）
```

#### 步骤 3: 配置主动臂和从动臂（相对运动）

```javascript
// 轴向相反关系表
const oppositeAxis = {
  0: 1,  // X+ → X-
  1: 0,  // X- → X+
  2: 3,  // Y+ → Y-
  3: 2,  // Y- → Y+
  4: 5,  // Z+ → Z-
  5: 4   // Z- → Z+
};

const arm1Path = gripper.modelName + '/' + child1.modelName;
const arm2Path = gripper.modelName + '/' + child2.modelName;

// 配置主动臂
await createLinearJoint(arm1Path, axis, minVal, maxVal, 100, false);

// 配置从动臂（相反方向！）
const dependentAxis = oppositeAxis[axis];
await callAPI('/behavior/add', {
  id: arm2Path,
  useModeId: false,
  behavioralType: 3,  // TranslationDependent
  referenceAxis: dependentAxis,  // 相反方向
  minValue: minVal,
  maxValue: maxVal,
  runSpeed: 100,
  isHaveElectricalMachinery: true,
  dependentTargetId: arm1Path,
  dependentTargetUseModeId: false
});
```

#### 配置要点总结

**1. 层级路径格式**
```
父节点名称/子节点名称          // 如：DH_PGE_100_26/NONE3
父节点名称/中间节点/孙节点      // 如：DH_RGD_5_14/1/NONE2
```

**2. 轴向判断规则**
- 分析两个夹爪的相对位置（ΔX, ΔY, ΔZ）
- 选择差值最大的轴作为运动轴向
- 根据正负值确定方向（X+ 或 X-）

**3. 行程计算（2026-03-14 21:20 更新）**
- 基于子节点的 `boundSize`（包围盒尺寸）
- 取运动轴向尺寸的 **1/3** 作为行程范围（经验值）
- 公式：`maxVal = Math.round(boundSize[axisIndex] / 3)`
- 根据实际运动方向设置正负值

**行程计算演进：**
- 初始版本：100% boundSize（行程过大，夹爪移动过度）
- 第一版优化：50% boundSize（仍然偏大）
- 最终版本：**33% boundSize**（保守合理，适合精细夹持）

**4. 相对运动配置**
| 主动臂轴向 | 从动臂轴向 | 说明 |
|------------|------------|------|
| X+ (0) | X- (1) | X 轴相对运动 |
| X- (1) | X+ (0) | X 轴相对运动 |
| Y+ (2) | Y- (3) | Y 轴相对运动 |
| Y- (3) | Y+ (2) | Y 轴相对运动 |
| Z+ (4) | Z- (5) | Z 轴相对运动 |
| Z- (5) | Z+ (4) | Z 轴相对运动 |

**5. 行为类型**
- **主动臂**: `behavioralType: 1` (Translation)
- **从动臂**: `behavioralType: 3` (TranslationDependent)
- **从属目标**: `dependentTargetId` 指向主动臂路径

#### 完整示例（DH_PGE_100_26）

```javascript
const { callAPI, createLinearJoint, ReferenceAxis } = await import('./kunwu-tool.js');

// 1. 获取层级树
const tree = await callAPI('/models/tree', { rootId: 'scene' });

// 2. 找到夹具
const gripper = tree.data.models.find(m => m.modelName === 'DH_PGE_100_26');

// 3. 分析结构
const child1 = gripper.children[0];  // NONE3
const child2 = gripper.children[1];  // NONE4
const dy = child2.transform[1] - child1.transform[1];  // ΔY = -13mm

// 4. 确定参数
const axis = dy < 0 ? ReferenceAxis.Y_NEGATIVE : ReferenceAxis.Y_POSITIVE;  // Y-
const maxVal = child1.boundSize[1];  // 46mm (Y 方向尺寸)

// 5. 配置
const arm1Path = 'DH_PGE_100_26/NONE3';
const arm2Path = 'DH_PGE_100_26/NONE4';

await createLinearJoint(arm1Path, ReferenceAxis.Y_NEGATIVE, 0, 46, 100, false);
await createLinearJoint(arm2Path, ReferenceAxis.Y_POSITIVE, 0, 46, 100, false, arm1Path);

// 6. 验证
const v1 = await callAPI('/behavior/get', { id: arm1Path, useModeId: false });
const v2 = await callAPI('/behavior/get', { id: arm2Path, useModeId: false });
console.log('主动臂:', v1.data.referenceAxis, '从动臂:', v2.data.referenceAxis);
```

## 错误码

| Code | 说明 |
|------|------|
| 200 | 请求成功 |
| 301 | 资源永久转移 |
| 400 | 请求失败/错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 注意事项

1. 软件必须运行在本地，端口 16888
2. 所有请求都是 POST，Content-Type: application/json
3. 成功响应：`{"code": 200, "msg": "OK"}`
4. 失败响应：`{"code": 400, "msg": "Bad Request"}`
5. 详细 API 参考：`api-reference.md`
6. **参数化模型**：不同模型支持的参数数量不同，"方形"默认支持 2 个参数（长、宽）
7. **场景 JSON**：软件修复后直接返回已解析的对象，使用 `getSceneJson()` 即可
8. **🔑 夹具行为配置四大核心原则（必须遵守！2026-03-16 最终版）**：

### 原则 1：轴向判断原则（bounding 最大轴方法）⚠️
**使用 bounding 最大轴确定运动轴向，这是最可靠的方法！**

```javascript
const boundSize = child1.boundSize;  // [sizeX, sizeY, sizeZ]
const maxSize = Math.max(boundSize[0], boundSize[1], boundSize[2]);

let axisIndex, activeAxis, dependentAxis;

if (maxSize === boundSize[0]) {
  // X 轴是最大轴 → X 轴开合
  axisIndex = 0;
  activeAxis = dx < 0 ? ReferenceAxis.X_POSITIVE : ReferenceAxis.X_NEGATIVE;
  dependentAxis = dx < 0 ? ReferenceAxis.X_NEGATIVE : ReferenceAxis.X_POSITIVE;
} else if (maxSize === boundSize[1]) {
  // Y 轴是最大轴 → Y 轴开合
  axisIndex = 1;
  activeAxis = dy < 0 ? ReferenceAxis.Y_POSITIVE : ReferenceAxis.Y_NEGATIVE;
  dependentAxis = dy < 0 ? ReferenceAxis.Y_NEGATIVE : ReferenceAxis.Y_POSITIVE;
} else {
  // Z 轴是最大轴 → Z 轴开合
  axisIndex = 2;
  activeAxis = dz < 0 ? ReferenceAxis.Z_POSITIVE : ReferenceAxis.Z_NEGATIVE;
  dependentAxis = dz < 0 ? ReferenceAxis.Z_NEGATIVE : ReferenceAxis.Z_POSITIVE;
}
```

**为什么 bounding 最大轴方法更可靠？**
- ✅ 直接反映夹爪的物理结构
- ✅ 不受 transform 坐标系统影响
- ✅ 避免 ΔX 和 ΔY 接近时的误判
- ✅ 符合夹具设计原理（运动方向通常是最长轴）

**实测案例：**
- DH_PGI_140_80：boundSize [**52**, 22, 16.7] → X 轴开合（ΔY=34.7mm 但 ΔX=40mm 更大）
- DH_PGE_100_26：boundSize [18.5, **46**, 19.5] → Y 轴开合
- DH_PGS_5_5：boundSize [**13**, 19, 22.5] → X 轴开合（子关节"1"和"2"）

### 原则 2：轴向反向原则
**主从关节的轴向必须相反，才能形成夹紧动作！**

| 主动臂轴向 | 从动臂轴向 | 说明 |
|-----------|-----------|------|
| X+ (0) | X- (1) | 相向运动夹紧 |
| Y+ (2) | Y- (3) | 相向运动夹紧 |
| Z+ (4) | Z- (5) | 相向运动夹紧 |

**错误示例** ❌：两个夹爪都沿 X+ 运动 → 同向移动，无法夹紧  
**正确示例** ✅：一个 X+ 一个 X- → 相向移动，夹紧工件

### 原则 3：行程计算原则
**运动行程 = boundingBox 在轴向上长度 × 1/3**

```javascript
const travel = boundSize[axisIndex] / 3;
// 例：boundSize[0] = 52mm → 行程 = 52/3 ≈ 17mm
```

**为什么是 1/3？**
- 保留余量防止过行程
- 避免夹爪碰撞
- 实际夹持行程通常小于理论最大值

**实测案例：**
- boundSize = 52mm → 行程 = 52/3 ≈ 17mm
- boundSize = 46mm → 行程 = 46/3 ≈ 15mm
- boundSize = 40mm → 行程 = 40/3 ≈ 13mm
- boundSize = 22mm → 行程 = 22/3 ≈ 7mm
- boundSize = 13mm → 行程 = 13/3 ≈ 4mm

### 原则 4：联动配置原则（⚠️ 最关键！）
**从动关节必须配置 `dependentTargetId` 指向主动关节，否则无法联动！**

```javascript
// 主动关节
await callAPI('/behavior/add', {
  id: '夹具名称/主动关节',
  useModeId: false,
  behavioralType: 1,            // 直线运动（主动）
  referenceAxis: activeAxis,
  minValue: 0,
  maxValue: travel,
  runSpeed: 80,
  targetValue: travel / 2
  // dependentTargetId: null (默认)
});

// 从动关节 ⚠️ 必须配置 dependentTargetId！
await callAPI('/behavior/add', {
  id: '夹具名称/从动关节',
  useModeId: false,
  behavioralType: 3,            // 直线联动（从动）
  referenceAxis: dependentAxis, // 与主动关节相反！
  minValue: 0,
  maxValue: travel,
  runSpeed: 80,
  targetValue: travel / 2,
  // ⚠️ 关键：必须指定 dependentTargetId！
  dependentTargetId: '夹具名称/主动关节',  // 使用层级路径
  dependentTargetUseModeId: false
});
```

**验证要点：**
- 配置后检查 `dependentTargetId` 不为 null
- 应该显示为 UUID 或模型名称
- 使用 `/behavior/list` 验证

9. **🔑 完整配置流程（7 步，必须按顺序执行！）**：

### 步骤 1: 查询层级结构
```javascript
const tree = await callAPI('/models/tree', {});
// 找到夹具的子关节（运动臂）
```

### 步骤 2: 分析子关节位置
```javascript
// 读取 transform 数组 [x, y, z, rx, ry, rz]
const child1 = gripper.children[0];  // 主动臂
const child2 = gripper.children[1];  // 从动臂

// 计算相对位置
const dx = child2.transform[0] - child1.transform[0];  // ΔX
const dy = child2.transform[1] - child1.transform[1];  // ΔY
const dz = child2.transform[2] - child1.transform[2];  // ΔZ
```

### 步骤 3: 确定轴向（⚠️ 重要：使用 bounding 最大轴方法）
```javascript
// 方法 1：通过 transform 计算相对位置（可能不准确）
const maxDelta = Math.max(Math.abs(dx), Math.abs(dy), Math.abs(dz));
let axisIndex, activeAxis, dependentAxis;

if (maxDelta === Math.abs(dx)) {
  axisIndex = 0;
  activeAxis = dx < 0 ? ReferenceAxis.X_POSITIVE : ReferenceAxis.X_NEGATIVE;
  dependentAxis = dx < 0 ? ReferenceAxis.X_NEGATIVE : ReferenceAxis.X_POSITIVE;
} else if (maxDelta === Math.abs(dy)) {
  axisIndex = 1;
  activeAxis = dy < 0 ? ReferenceAxis.Y_POSITIVE : ReferenceAxis.Y_NEGATIVE;
  dependentAxis = dy < 0 ? ReferenceAxis.Y_NEGATIVE : ReferenceAxis.Y_POSITIVE;
} else {
  axisIndex = 2;
  activeAxis = dz < 0 ? ReferenceAxis.Z_POSITIVE : ReferenceAxis.Z_NEGATIVE;
  dependentAxis = dz < 0 ? ReferenceAxis.Z_NEGATIVE : ReferenceAxis.Z_POSITIVE;
}

// 方法 2：通过 bounding 最大轴确定（✅ 更可靠！2026-03-16 更新）
// 原则：夹爪的运动轴向通常是 bounding 尺寸最大的轴
const boundSize = child1.boundSize;  // [sizeX, sizeY, sizeZ]
const maxSize = Math.max(boundSize[0], boundSize[1], boundSize[2]);

if (maxSize === boundSize[0]) {
  // X 轴是最大轴
  axisIndex = 0;
  activeAxis = dx < 0 ? ReferenceAxis.X_POSITIVE : ReferenceAxis.X_NEGATIVE;
  dependentAxis = dx < 0 ? ReferenceAxis.X_NEGATIVE : ReferenceAxis.X_POSITIVE;
} else if (maxSize === boundSize[1]) {
  // Y 轴是最大轴
  axisIndex = 1;
  activeAxis = dy < 0 ? ReferenceAxis.Y_POSITIVE : ReferenceAxis.Y_NEGATIVE;
  dependentAxis = dy < 0 ? ReferenceAxis.Y_NEGATIVE : ReferenceAxis.Y_POSITIVE;
} else {
  // Z 轴是最大轴
  axisIndex = 2;
  activeAxis = dz < 0 ? ReferenceAxis.Z_POSITIVE : ReferenceAxis.Z_NEGATIVE;
  dependentAxis = dz < 0 ? ReferenceAxis.Z_NEGATIVE : ReferenceAxis.Z_POSITIVE;
}
```

### 步骤 4: 计算行程
```javascript
// 行程 = boundingBox 在轴向上长度 × 1/3
const travel = boundSize[axisIndex] / 3;
// 例：boundSize[0] = 52mm → 行程 = 52/3 ≈ 17mm
```

### 步骤 5: 配置主动关节
```javascript
await callAPI('/behavior/add', {
  id: '夹具名称/主动关节名称',  // 使用层级路径
  useModeId: false,
  behavioralType: 1,            // 直线运动（主动）
  referenceAxis: activeAxis,    // 轴向（根据步骤 3）
  minValue: 0,
  maxValue: travel,             // 行程（步骤 4）
  runSpeed: 80,
  targetValue: travel / 2
});
```

### 步骤 6: 配置从动关节（⚠️ 必须配置 dependentTargetId！）
```javascript
await callAPI('/behavior/add', {
  id: '夹具名称/从动关节名称',   // 使用层级路径
  useModeId: false,
  behavioralType: 3,            // 直线联动（从动）
  referenceAxis: dependentAxis, // 轴向（与主动关节相反！）
  minValue: 0,
  maxValue: travel,
  runSpeed: 80,
  targetValue: travel / 2,
  // ⚠️ 关键：必须指定 dependentTargetId！
  dependentTargetId: '夹具名称/主动关节名称',  // ✅ 使用层级路径
  dependentTargetUseModeId: false
});
```

### 步骤 7: 验证配置
```javascript
const result = await callAPI('/behavior/list', {
  id: '夹具 modelId',
  useModeId: true
});

// 验证要点：
// 1. 父模型 hasBehavior: false
// 2. 主动关节 behavioralType: 1, dependentTargetId: null
// 3. 从动关节 behavioralType: 3, dependentTargetId: "xxx-xxx-xxx" (不为 null!)
// 4. 主从轴向相反（如 X+ 对 X-）
```

9. **🔑 核心原则（必须遵守）**：
   - **轴向反向原则**：主从关节的轴向必须相反，才能形成夹紧动作
     - 主动臂沿 `X+` → 从动臂必须沿 `X-`
     - 主动臂沿 `Y+` → 从动臂必须沿 `Y-`
     - 主动臂沿 `Z+` → 从动臂必须沿 `Z-`
   - **行程计算原则**：运动行程 = boundingBox 在轴向上长度 × 1/3
     - 例：boundSize[1] = 22mm → 行程 = 22/3 ≈ 7mm
     - 原因：保留余量防止过行程和碰撞
   - **联动配置原则**：从动关节必须配置 `dependentTargetId` 指向主动关节
     - 使用层级路径：`'夹具名称/主动关节名称'`
     - 设置 `dependentTargetUseModeId: false`
     - 验证时检查 `dependentTargetId` 不为 null
     - 原理：两个夹爪相向运动才能夹紧工件
   - **行程计算原则**：运动行程 = boundingBox 在轴向上长度 × 1/3
     - 例：夹爪 Y 方向尺寸 46mm → 行程 = 46 × 1/3 ≈ 15mm
     - 例：夹爪 X 方向尺寸 150mm → 行程 = 150 × 1/3 = 50mm
     - 原因：保留余量防止过行程和碰撞
   - **配置流程**：
     1. `/models/tree` 获取层级结构和子关节名称
     2. 读取 `transform` 计算相对位置，确定轴向
     3. 读取 `boundSize` 计算行程（× 1/3）
     4. 配置主动臂（behavioralType: 1）
     5. 配置从动臂（behavioralType: 3 + dependentTargetId + 反向轴向）
     6. `/behavior/list` 验证配置

## 更新日志

### 2026-03-16 (16:20) - 设备装配规则纠正和总结
- ✅ **装配规则纠正** - 重要原则：
  - ✅ **机器人 -> 底座**（机器人安装在底座上）
  - ✅ **机器人 -> 桁架**（机器人直接安装在桁架上）
  - ❌ **底座 -> 桁架**（错误！底座和桁架都是支撑结构，不应互相装配）
- ✅ **正确的装配层级**：
  ```
  场景
  ├── 地轨/底座（支撑结构，直接放置在地面）
  │   └── 机器人（装配到底座 assemble 点）
  │       └── 夹具/相机（装配到机器人末端）
  │
  ├── 桁架（支撑结构，直接放置在地面）
  │   └── Main 自由臂（内置机器人）
  │       └── 抓手（装配到自由臂末端）
  │
  └── 相机支架（支撑结构，直接放置在地面）
      └── 相机（装配到支架 assemble 点）
  ```
- ✅ **装配规则测试完成** - 三大装配规则已验证
  1. **规则 1**: 相机 -> 相机支架 ✅
  2. **规则 2**: 机器人相机系统（机器人->机器人底座/地轨，夹具->机器人）✅
  3. **规则 3**: 桁架系统（桁架抓手->桁架两个自由臂）✅
- ✅ **多装配位选择规则**（HandleModelAssemble 处理逻辑）：
  1. 先筛选"兼容装配位" - 遍历 parentModel.AssembleItemsType
  2. 优先级选择：
     - **优先 1**: assemblePosName（按名称匹配，忽略大小写）
     - **优先 2**: assemblePosIndex >= 0（必须是兼容位）
     - **优先 3**: 自动选择（先找兼容且空闲位，无空闲取首兼容位）
  3. 占用处理：
     - replaceExisting=false: 返回 409（不替换）
     - replaceExisting=true: 先卸下旧模型，再装新模型
- ✅ **装配 API 使用示例**：
  ```javascript
  // 装配到指定装配位（推荐方式）
  await callAPI('/model/assemble', {
    childId: '子模型 modelId',
    parentId: '父模型 modelId',
    assemblePosIndex: 0,  // 第一个装配位
    replaceExisting: false
  });
  
  // 或按名称指定装配位
  await callAPI('/model/assemble', {
    childId: '子模型 modelId',
    parentId: '父模型 modelId',
    assemblePosName: 'cameraPoint',  // 装配位名称
    replaceExisting: false
  });
  ```
- ✅ **实测案例**：
  - 2D 相机_01 装配到 相机支架_01 (assemblePosIndex: 0) ✅
  - 相机支架有两个装配位（Link1 和 Link2 各一个 assemble 点）
  - LR_MATE_200ID_7L 装配到 方形底座 (assemblePosIndex: 0) ✅
  - 桁架抓手_01/02 装配到 桁架 Main 自由臂 ✅

### 2026-03-16 (14:15) - 完整经验总结：四大原则 + 配置检查清单
- ✅ **最终确认** - 所有经验已通过多次实测验证，配置完全正确
- ✅ 更新 SKILL.md 注意事项：
  - **四大核心原则**（必须遵守！）：
    1. **轴向判断原则**：使用 bounding 最大轴确定运动轴向 ⚠️
    2. **轴向反向原则**：主从关节轴向必须相反
    3. **行程计算原则**：行程 = boundSize ÷ 3
    4. **联动配置原则**：从动关节必须配置 dependentTargetId ⚠️
  - **完整 7 步配置流程**（必须按顺序执行）
  - **配置检查清单**（逐项检查）
- ✅ 实测验证（全部成功）：
  - 夹具_小型气动 (DH_PGS_5_5): X 轴开合，行程 4mm ✅
  - 夹具_大型气动 (DH_PGI_140_80): X 轴开合，行程 17mm ✅（修正后）
  - 夹具 C_电动中型 (DH_PGE_100_26): Y 轴开合，行程 15mm ✅
  - 夹具 D_旋转型 (DH_RGD_5_14): X 轴开合，行程 13mm ✅
- ✅ 关键教训：
  - bounding 最大轴方法最可靠（避免 transform 误判）
  - dependentTargetId 必须配置（否则无法联动）
  - 所有经验必须记录在 Skill 文档中（不能只在 MEMORY.md）

### 2026-03-16 (14:00) - 轴向判断方法更新：bounding 最大轴原则
- ✅ **重要修正** - 夹具_大型气动 (DH_PGI_140_80) 轴向配置错误修正
  - 错误：通过 transform 的 ΔY (34.7mm) 判断为 Y 轴开合 ❌
  - 正确：通过 bounding 最大轴 (52mm) 判断为 X 轴开合 ✅
- ✅ 更新轴向判断方法：
  - **方法 1**：通过 transform 计算相对位置（可能不准确）
  - **方法 2**：通过 bounding 最大轴确定（✅ 更可靠！）
- ✅ 核心原则更新为**四大原则**：
  1. **轴向判断原则**：使用 bounding 最大轴确定运动轴向 ⚠️
  2. **轴向反向原则**：主从关节轴向必须相反
  3. **行程计算原则**：行程 = boundSize ÷ 3
  4. **联动配置原则**：从动关节必须配置 dependentTargetId

### 2026-03-16 (11:50) - 完整配置流程：dependentTargetId 必须配置
- ✅ **关键发现** - 从动关节必须配置 `dependentTargetId` 指向主动关节，否则无法联动
- ✅ 更新 SKILL.md - 添加完整的 7 步配置流程：
  1. 查询层级树
  2. 分析子关节位置（transform 数组）
  3. 确定轴向（基于相对位置）
  4. 计算行程（boundSize ÷ 3）
  5. 配置主动关节（behavioralType: 1）
  6. 配置从动关节（behavioralType: 3 + **dependentTargetId**）
  7. 验证配置（检查 dependentTargetId 不为 null）
- ✅ 更新 SKILL_USAGE.md - 添加：
  - 完整配置示例（含 dependentTargetId）
  - 配置检查清单（必须逐项检查）
  - 常见问题排查
  - 配置记录模板
- ✅ 核心原则（三大原则）：
  1. **轴向反向原则**：主从关节轴向必须相反
  2. **行程计算原则**：行程 = boundSize ÷ 3
  3. **联动配置原则**：从动关节必须配置 dependentTargetId ⚠️

### 2026-03-16 (11:00) - 关键经验固化：轴向反向和行程计算
- ✅ **核心经验总结** - 基于多次测试失败后积累的关键经验：
  - **轴向反向原则**：主从关节轴向必须相反（X+ 对 X-，Y+ 对 Y-），否则无法夹紧
  - **行程计算原则**：行程 = boundingBox 轴向长度 × 1/3（保留余量防碰撞）
- ✅ 更新 SKILL.md 注意事项 - 将经验记录在第 9 条，确保不会忘记
- ✅ 实测验证：
  - 夹具_大型气动：NONE1 (Y+, 60mm) + NONE2 (Y-, 60mm) ✅
  - 夹具_机械式：gripper1 (X+, 400mm) + gripper2 (X-, 400mm) ✅
- ✅ 教训：这些关键经验不能只在 MEMORY.md，必须记录在 Skill 文档中

### 2026-03-14 (18:50) - 夹具行为配置完整指南
- ✅ **经验积累** - 基于 5 个夹具（DH 系列 + Mechanical Gripper）的实测经验
- ✅ 更新文档 - 补充完整配置流程：
  - 步骤 1: 获取夹具层级结构
  - 步骤 2: 分析结构确定轴向和行程
  - 步骤 3: 配置主动臂和从动臂（相对运动）
- ✅ 新增配置要点总结：
  - 层级路径格式（支持多级路径）
  - 轴向判断规则（基于相对位置）
  - 行程计算方法（基于 boundSize）
  - 相对运动配置（轴向相反关系表）
- ✅ 添加完整示例代码（DH_PGE_100_26）
- ✅ 实测验证：5/5 夹具配置成功，全部实现相对运动

### 2026-03-14 (17:30) - 模型定位与层级路径支持
- ✅ **API 重大更新** - 经理已完成模型定位统一方案
  - 新增 `/models/search` - 搜索模型，返回 modelId 和 hierarchyPath
  - 支持层级路径格式：`id: "父节点/子节点"`
  - 409 歧义处理 - 重名时返回候选列表
  - `TryResolveModelTransform()` - 统一解析模型位置
- ✅ 新增 `searchModel()` 函数 - 封装 `/models/search` 接口
- ✅ 更新 `createLinearJoint()` - 支持 `useModeId` 参数（true=modelId, false=路径/名称）
- ✅ 更新 `createLinearJointWithDependent()` - 支持层级路径
- ✅ 更新文档 - 补充三种配置方式：
  - 方式 1: 层级路径（推荐，简洁）
  - 方式 2: modelId 直达（最稳定）
  - 方式 3: Helper 函数（简化调用）

### 2026-03-14 (16:30) - 夹具行为配置专题
- ✅ 新增 `/behavior/list` 接口支持 - `getBehaviorList()` 函数
- ✅ 更新 `addBehavior()` - 支持 `dependentTargetId` 和 `dependentTargetUseModeId` 参数
- ✅ 更新 `createLinearJoint()` - 支持从属运动（自动设置 behavioralType=3）
- ✅ 更新 `createRotaryJoint()` - 支持从属旋转
- ✅ 新增 `createLinearJointWithDependent()` - 便捷创建从动臂
- ✅ 测试验证：成功创建并配置 4 个夹具（DH 系列），主动臂 + 从动臂联动
- ✅ 更新文档：补充夹具行为配置示例和注意事项

### 2026-03-14 (下午)
- ✅ **软件修复验证** - `/scene/get_scene_json` 接口已修复，直接返回已解析的 JSON 对象
- ✅ 更新 `getSceneJson()` - 适配新返回格式（`data.projectData`），无需二次解析
- ✅ `getSceneJsonParsed()` 作为别名保留，兼容旧代码

### 2026-03-14 (上午)
- ✅ 修复 `createBoxJoint()` - 高度参数改为可选，支持 2 参数或 3 参数调用
- ✅ 新增 `getSceneJsonParsed()` - 解析 Unity 导出的非标准 JSON 场景数据（软件修复前使用）
- ✅ 更新文档：补充参数化模型和场景 JSON 解析的使用说明

### 2026-03-13
- ✅ 新增模型库管理功能（本地/远程/下载/收藏）
- ✅ 新增层级关系管理（父子关系/批量销毁）
- ✅ 新增行为控制 Helper 函数
- ✅ 新增批量执行、进度条等辅助功能
