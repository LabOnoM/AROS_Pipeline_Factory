# Web Project Builder - 技术参考

## 技术栈

### 前端
- Bootstrap 5.3.3 (CDN): `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css`
- Bootstrap JS Bundle: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js`
- ECharts 5.5.0 (CDN): `https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js`

### 后端
- Python Flask >= 3.0
- SQLite (内置，无需额外安装)

### 测试
- pytest >= 8.0

## 项目结构

```
project-name/
├── app.py              # Flask 主应用
├── requirements.txt    # Python 依赖
├── database.db         # SQLite 数据库 (运行时生成)
├── .gitignore
├── static/
│   ├── css/style.css   # 自定义样式
│   ├── js/main.js      # 前端逻辑 + ECharts
│   └── img/            # 图片资源
├── templates/
│   ├── base.html       # 基础模板 (含 CDN 引入)
│   └── index.html      # 首页
└── tests/
    └── test_app.py     # 测试用例
```

## 四个角色职责

### 1. 前端 (Frontend)
- HTML 页面结构，使用 Jinja2 模板继承
- Bootstrap 组件：导航栏、卡片、表格、表单、按钮
- ECharts 图表渲染
- Fetch API 与后端交互

### 2. 后端 (Backend)
- Flask 路由和视图函数
- SQLite 数据库 CRUD 操作
- RESTful API 设计 (`/api/` 前缀)
- 数据验证和错误处理

### 3. UI 设计 (UI Design)
- Bootstrap 响应式布局 (栅格系统)
- 卡片式内容组织
- 一致的配色方案 (Bootstrap primary)
- 移动端适配

### 4. 测试设计 (Testing)
- pytest 单元测试
- Flask test_client 集成测试
- 临时数据库隔离测试环境
- 覆盖 CRUD 全流程

## 常用 ECharts 图表类型

- `type: "bar"` - 柱状图
- `type: "line"` - 折线图
- `type: "pie"` - 饼图
- `type: "scatter"` - 散点图

## Flask API 模式

```python
@app.route("/api/resource", methods=["GET"])
def list_resource():
    # 查询并返回 JSON

@app.route("/api/resource", methods=["POST"])
def create_resource():
    # 从 request.get_json() 获取数据，插入数据库

@app.route("/api/resource/<int:id>", methods=["PUT"])
def update_resource(id):
    # 更新指定记录

@app.route("/api/resource/<int:id>", methods=["DELETE"])
def delete_resource(id):
    # 删除指定记录
```
