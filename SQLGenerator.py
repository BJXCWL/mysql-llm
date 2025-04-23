import re
from openai import OpenAI

class SQLGenerator:
    """
    封装了使用 OpenAI deepseek-chat 模型，将自然语言查询转换为 SQL 的功能。
    Usage:
        generator = SQLGenerator(api_key, base_url)
        sql = generator.generate_sql(schema, query)
    """
    def __init__(self, api_key: str, base_url: str = None, model: str = "deepseek-chat"):
        self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        self.model = model

    def generate_prompt(self, schema: str, query: str) -> str:
        """
        根据数据库 schema 和用户的自然语言查询，生成用于 LLM 的提示。
        """
        return f"""
                    You are an AI assistant that converts natural language queries into SQL.
                    Given the following SQL database schema:

                    <schema>
                    {schema}
                    </schema>

                    Convert the following natural language query into SQL:
                    <query>
                    {query}
                    </query>

                    Provide only the SQL query in your response, enclosed within <sql> tags.
                """

    def generate_sql(self, schema: str, query: str, max_tokens: int = 1000) -> str:
        """
        调用 OpenAI 接口，将自然语言查询转换为 SQL。
        返回值为带有 <sql> 标签的完整响应字符串。
        """
        prompt = self.generate_prompt(schema, query)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content