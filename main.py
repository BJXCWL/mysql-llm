from MySQLClient import MySQLClient
from SQLGenerator import SQLGenerator
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    db = MySQLClient(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT')),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASS'),
        database=os.getenv('MYSQL_DB')
    )
    schema = db.get_schema_info()
    sql_generator = SQLGenerator(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv('OPENAI_BASE_URL'),
        model=os.getenv('MODEL')
    )
    sql = sql_generator.generate_sql(schema, '查看所有用户的提交记录信息（只显示重要信息，不要显示所有信息）')
    result = db.run_sql(sql)
    print(result)

if __name__ == "__main__":
    main()