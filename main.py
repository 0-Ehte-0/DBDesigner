from graph import schema_designer_app

def main():
    normal_requirement = "I need a database to manage a library. It should have tables for Books, Authors, and Borrowers. The Books table should include columns for title, publication year, and author_id. The Authors table should include columns for name and birthdate. The Borrowers table should include columns for name and contact information. Ensure that the author_id in the Books table is a foreign key referencing the Authors table."
    
    nightmare_requirement = """
    Build a university academic tracking system.
    We need a Departments table, a Professors table, and a Courses table.
    
    Rules:
    A Department has a Head_Professor_ID referencing the Professors table.
    A Professor has a Department_ID referencing the Departments table.
    
    Courses must use a composite primary key made of two columns: Department_Code and Course_Number (e.g., CS and 101).
    
    Professors and Courses have a many-to-many relationship called 'Teaching_Assignments'. 
    This assignment table must also track the 'Semester' the course is taught.
    """
    mock_initial_state = {
        "requirement" : nightmare_requirement,
        "schemaOutput": None,
        "errors": [],
        "iterations": 0,
        "is_Valid": False
    }

    updated_state = schema_designer_app.invoke(mock_initial_state)

    print("Updated State after Generation & Validation:")
    print("Iterations:", updated_state.get("iterations"))
    if "schemaOutput" in updated_state and updated_state["is_Valid"]:
        print("Generated Schema Output:")
        for table in updated_state["schemaOutput"].tables:
            print(f"Table: {table.table_name}")
            for column in table.columns:
                print(f"  Column: {column.name}, Type: {column.data_type}, Constraints: {column.constraints}")
    else:
        print("Failed to generate schema.")

if __name__ == "__main__":
    main()