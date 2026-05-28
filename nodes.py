import sqlite3
from state import State
from llm_client import getStructuredLLM
from prompts import getSchemaPrompt

def generationNode(state: State) -> dict:
    requirement = state.get("requirement")
    errors = state.get("errors", [])
    current_iteration = state.get("iterations", 0)
    
    print(f"Generation Node - Iteration {current_iteration+1}")
    error_context = ""
    if errors:
        latest_error = errors[-1]
        error_context = f"CRITICAL: Your previous attempt failed with these errors:\n{latest_error}\n\nFix the SQL and regenerate."
    
    prompt = getSchemaPrompt()
    structuredLLM = getStructuredLLM()
    chain = prompt | structuredLLM

    try:
        result = chain.invoke({
            "requirement": requirement,
            "error_context": error_context
        })
        print("Generation successful.")
        return {
            "schemaOutput": result,
            "iterations": current_iteration + 1,
        }
    except Exception as e:
        print(f"Generation failed with error: {e}")
        return {
            "errors": errors + [str(e)],
            "iterations": current_iteration + 1,
        }

def validationNode(state: State) -> dict:
    schema_output = state.get("schemaOutput")
    errors = state.get("errors", [])
    print("Validation Node - Validating generated schema.")
    if not schema_output or not schema_output.raw_sql:
        print("No schema output to validate.")
        return {
            "is_Valid": False,
            "errors": errors + ["No schema output to validate."]
        }
    raw_sql = schema_output.raw_sql
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    try:
        cursor.executescript(raw_sql)
        conn.commit()

        print("Validation successful. Schema is valid.")

        return {
            "is_Valid": True
        }
    except sqlite3.OperationalError as e:
        error_message = f"SQLite OperationalError: {str(e)}"
        return {
            "is_Valid": False,
            "errors": errors + [error_message]
        }
    finally:
        conn.close()