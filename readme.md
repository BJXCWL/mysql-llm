# 文本生成 SQL

## 项目简介
一个基于 MySQL + 大语言模型（LLM）的 SQL 自动生成与执行工具，支持：

- **数据库模式自动读取**：动态获取当前 MySQL 实例中所有表及字段信息
- **自然语言转 SQL**：通过深度学习模型（如 OpenAI deepseek-chat）将用户的中文/英文查询转换为标准 SQL
- **SQL 执行与结果展示**：在 MySQL 上执行生成的 SQL，并返回 Pandas DataFrame 形式的查询结果
- **标签化 SQL 提取**：支持在输入中使用 `<sql>…</sql>` 包裹多句 SQL 片段，自动提取并执行

## 主要功能
1. `MySQLClient`
   - 初始化、关闭 MySQL 连接
   - 获取数据库所有表及列的模式信息 (`get_schema_info`)
   - 原生游标执行任意 SQL 返回 `pandas.DataFrame` (`run_sql`)
2. `SQLGenerator`
   - 基于 OpenAI `deepseek-chat` 模型，自动将自然语言转为 SQL，结果封装在 `<sql>` 标签中
   - 可自定义模型名称、`max_tokens` 等参数
3. 主脚本 `main.py`
   - 组合以上两者：读取模式、生成 SQL、执行查询、打印输出

## 仓库结构
```
├── MySQLClient.py     # MySQLClient 类实现
├── SQLGenerator.py    # 封装 OpenAI 转 SQL 的类
├── main.py            # 演示脚本：一键跑通完整流程
├── requirements.txt   # 依赖列表
└── README.md          # 项目说明文档
```

## 环境配置
1. 克隆代码并创建虚拟环境：
   ```bash
   git clone <repo_url>
   cd <repo_dir>
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate  # Windows
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量（建议在项目根目录创建 `.env`）：
   ```ini
   # MySQL 配置
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASS=xxxxxxxxxxxxxxxx
   MYSQL_DB=xxxxxxxxxxx

   # OpenAI/Deepseek 配置
   OPENAI_API_KEY=sk-xxxxxx
   OPENAI_BASE_URL=https://api.deepseek.com
   ```

## 快速开始
在 `.env` 配置完毕后，直接运行：
```bash
python main.py
```
脚本会：
1. 连接 MySQL 并打印所有表结构
2. 以示例自然语言查询生成 SQL
3. 执行生成的 SQL 并打印查询结果

若要自定义查询内容，可编辑 `main.py` 中的
```python
natural_query = "你希望执行的自然语言查询"
```

## 自定义调用示例
```python
from MySQLClient import MySQLClient
from SQLGenerator import SQLGenerator

# 初始化
db = MySQLClient(
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASS'),
    database=os.getenv('MYSQL_DB')
)
sql_generator = SQLGenerator(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    model=os.getenv('MODEL')
)
# 获取模式、生成 SQL、执行并拿到 DataFrame
schema = db.get_schema_info()
query = "获取所有用户名称及其最新一次提交状态"
sql_text = generator.generate_sql(schema, query)
df = db.run_sql(sql_text)
print(df)

# 关闭连接
db.close()
```

## 依赖
- Python ≥ 3.8
- pymysql
- pandas
- openai  （或 deepseek SDK）
- python-dotenv（可选，用于 .env 加载）

可通过 `pip install -r requirements.txt` 一键安装。

## 参考
 - Anthropics Cookbook: https://github.com/anthropics/anthropic-cookbook/tree/main/skills/text_to_sql
 - OpenAI API 文档


