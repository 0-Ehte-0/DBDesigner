from pydantic import BaseModel, Field
from typing import List, Optional

# Column Class
class ColumnSchema(BaseModel):
    name: str = Field(description="The exact name of the database column")
    # 'data_type' is a required string. We explicitly ask for standard SQL types.
    data_type: str = Field(description="The SQL data type like VARCHAR(255), INTEGER, TIMESTAMP")
    # 'constraints' is an optional string. It defaults to None if the LLM doesn't provide it.
    constraints: Optional[str] = Field(description="SQL constraints like PRIMARY KEY, NOT NULL", default=None)

# Table Class
class TableSchema(BaseModel):
    # 'table_name' is a required string for the name of the table
    table_name: str = Field(description="The name of the database table")
    # 'columns' requires a list of the ColumnSchema objects we defined above
    columns: List[ColumnSchema] = Field(description="List of columns belonging to this table")

# Root Class
class DatabaseSchema(BaseModel):
    # 'tables' requires a list of TableSchema objects, nesting our previous models
    tables: List[TableSchema] = Field(description="All tables required for the requested database layout")
    # 'raw_sql' is a required string where the LLM writes the final executable SQLite script
    raw_sql: str = Field(description="The complete, valid SQLite SQL script to create these tables")