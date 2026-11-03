# NVIDIA SimReady 3D 仿真资产库 · 中文选型目录

> 收录 **2,595** 个经 Meshopt 网格压缩与 WebP 贴图优化的 NVIDIA SimReady 高质量仿真资产。  
> 采用经典左右工程分栏布局、支持纯净无图标设计、明暗主题无缝切换、中英双语毫秒级检索、活动关节筛选、多语言代码生成与 CSV 数据导出。

---

## 1. 项目背景与解决的痛点

### 什么是 NVIDIA SimReady 资产？
**NVIDIA SimReady** 是 NVIDIA 为数字孪生（Omniverse）、物理仿真与具身智能（Isaac Sim / 机器人强化学习）打造的工业级标准化 3D 资产库。每个资产不仅包含高精度网格与 PBR 材质，更包含严格的物理刚体、碰撞凸包（Collision Hulls）、物理材质以及铰接运动关节（Joints）。

### 痛点与本工具的解决方式
1. **体积巨大、分发极慢**：原版 SimReady 资产以 OpenUSD / Blender 工程存储，全库原始体积高达 **228.1 GB**，单个装配体动辄数百兆，难以在网页端快速选型。
   * **解决方案**：基于 `codepawl/simready-glb`，采用 `EXT_meshopt_compression` 与 `EXT_texture_webp` 深度压缩，全集缩减至仅 **3.2 GB**（压缩比高达 **72×**），单模型仅数 MB，实现浏览器秒开。
2. **缺乏系统中文分类与命名**：原库为英文工程命名，非英语母语工程师选型检索困难。
   * **解决方案**：建立 10 大产业体系映射与 192 个主分类 100% 汉化词典，利用专业词根智能重构清晰自然的中文品名。
3. **开箱即用、零环境依赖**：
   * **解决方案**：生成单一自包含 HTML 页面，内嵌全量元数据，**无需安装 Node.js、Python 或任何后端服务，双击即可在任意浏览器直接打开使用**。

---

## 2. 核心功能特性

| 功能模块 | 说明 |
| :--- | :--- |
| **左右工程分栏布局** | 左侧 320px 固态控制面板（关键词搜索、参数筛选、细分类下拉、10 大领域纵向导航），右侧主视图区。 |
| **纯净工程视觉风格** | 去除全部装饰性 Emoji 图标，采用简洁专业、高对比度的 CAD / 工程控制台风格。 |
| **明暗主题切换** | 顶部提供 `暗色模式` 与 `亮色模式` 一键无缝切换，基于 CSS 变量深度适配，并支持 `localStorage` 本地状态记忆。 |
| **10 大产业体系导航** | 汽车汽修、工业工具、仓储物流、食品生鲜、餐饮厨具、医疗器械、办公设施、安全消防、机器人与自动化、装饰杂项。 |
| **全量 2,595 模型汉化** | 192 个主分类与 2,595 个资产名全量中文汉化（如：`气动棘轮扳手 (A01)`、`发动机凸轮轴 (A01)`、`立式液压千斤顶 (A01)` 等）。 |
| **物理关节一键筛选** | 一键过滤出库中 **929 个带有铰接可动机构的物理模型**，适配机器人仿真交互与机构运动分析。 |
| **多维度排序** | 支持按文件体积（升/降序）、多边形面数（降序）、可动关节数（降序）灵活排序。 |
| **双视图自由切换** | 支持「网格卡片视图」（直观查看 3D 渲染缩略图）与「详细表格视图」（密集工程参数比对）。 |
| **多语言代码一键生成** | 点击模型卡片弹窗即提供 **Three.js**（含 Meshopt 配置）、**Python**（HuggingFace Hub 下载）与 **HF CLI** 命令行调用代码。 |
| **数据导出为 CSV** | 支持将当前筛选/搜索出的模型清单（含中文名、英文 ID、体积、面数、下载链接）一键导出为 Excel 兼容的 `.csv` 表格。 |

---

## 3. 文件结构

```text
AIagent项目/
├── SimReady_3D模型汉化选型目录.html   # [核心交付物] 单文件自包含的汉化选型目录网页（双击即用）
├── generate_catalog.py               # [生成脚本] 数据解析、词汇汉化规则与单文件 HTML 编译生成器
├── assets_cache.json                 # [本地缓存] 包含 2,595 个 SimReady 模型的原始规格元数据
└── README.md                         # [项目说明] 本说明文档
```

---

## 4. 快速上手

### 方式一：直接在浏览器中使用（推荐）
在 Windows 资源管理器或任意系统文件管理器中直接双击：
```text
SimReady_3D模型汉化选型目录.html
```
页面将在您的默认浏览器（Chrome、Edge、Safari、Firefox 等）中即时打开。

### 方式二：重新生成或修改配置
若需调整汉化词典、分类映射或新增功能，可运行随附的生成脚本：
```bash
python generate_catalog.py
```
脚本将自动解析并更新输出最新的 `SimReady_3D模型汉化选型目录.html`。

---

## 5. 代码集成指南

由于本资产库采用了现代 Web GLTF 标准的高级网格压缩算法（Meshopt），在加载时请参考以下方式引入解码器：

### 1. Web 前端开发 (Three.js)

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

// 初始化 GLTFLoader 并绑定 MeshoptDecoder 解码器
const loader = new GLTFLoader();
loader.setMeshoptDecoder(MeshoptDecoder);

// 加载指定模型（从 HuggingFace CDN 直链加载）
const modelUrl = 'https://huggingface.co/datasets/codepawl/simready-glb/resolve/main/glb/handTool_air_ratchet_a01.glb';

loader.load(modelUrl, (gltf) => {
  scene.add(gltf.scene);
  console.log('模型加载成功:', gltf.scene);
}, (xhr) => {
  console.log(`加载进度: ${(xhr.loaded / xhr.total * 100).toFixed(1)}%`);
}, (error) => {
  console.error('模型加载失败:', error);
});
```

### 2. Python 批量或单文件下载

```python
from huggingface_hub import hf_hub_download

# 下载单个优化后的轻量 GLB 模型到本地
file_path = hf_hub_download(
    repo_id="codepawl/simready-glb",
    filename="glb/engineComponent_camshaft_a01.glb",
    repo_type="dataset",
    local_dir="./models"
)
print(f"模型已保存至: {file_path}")
```

### 3. Hugging Face CLI 命令行下载

```bash
# 下载指定分类（如所有食品类模型）
hf download codepawl/simready-glb --repo-type dataset --include "glb/food_*" --local-dir ./simready-glb

# 下载完整优化数据集 (~3.2 GB)
hf download codepawl/simready-glb --repo-type dataset --local-dir ./simready-glb
```

---

## 6. 数据统计速览

* **全库模型总量**：`2,595` 个
* **原始工程总容量**：`228.1 GB`
* **优化后 GLB 总容量**：`3.2 GB`
* **整体压缩比**：`~72×`
* **含物理活动铰接关节模型**：`929` 个
* **涵盖细分类别**：`192` 个
* **覆盖产业领域**：`10` 个

---

## 7. 鸣谢与数据来源

* **原始 3D 资产**：[NVIDIA SimReady Assets](https://huggingface.co/datasets/nvidia/simready-assets)
* **Web GLB 轻量化工程**：[codepawl/simready-glb](https://huggingface.co/datasets/codepawl/simready-glb)
* **官方在线 Viewer**：[codepawl/simready-glb-viewer](https://huggingface.co/spaces/codepawl/simready-glb-viewer)

