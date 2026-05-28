from typing import TypedDict, List, Optional
from schema import DatabaseSchema

class State(TypedDict):
    requirement: str
    schemaOutput: Optional[DatabaseSchema] = None
    errors: List[str]
    iterations: int
    is_Valid: bool
    