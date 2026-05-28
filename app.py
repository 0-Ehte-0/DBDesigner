import streamlit as st
from graph import schema_designer_app
from state import State

st.set_page_config(page_title="AI Schema Architect", layout="wide")

st.title("Dynamic Data Schema Architect")
st.markdown("An autonomous local AI agent that designs, compiles, and self-corrects SQLite databases.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("System Requirements")
    user_requirement = st.text_area(
        "Describe your database architecture:",
        height=150,
        placeholder="e.g., A university system with composite keys for Courses, and a many-to-many relationship between Professors and Departments..."
    )
    
    generate_button = st.button("Generate Architecture", type="primary")

with col2:
    st.subheader("Agent Execution Logs")
    log_container = st.empty()

if generate_button and user_requirement:
    initial_state: State = {
        "requirement": user_requirement,
        "schemaOutput": None,
        "errors": [],
        "iterations": 0,
        "is_Valid": False
    }
    
    # CRITICAL FIX: Accumulate state dynamically as the stream yields updates
    current_state = initial_state.copy()
    
    with col2:
        with log_container.container():
            st.info("Agent Initialized. Booting graph execution...")
            
            # Explicitly request updates to ensure compatibility across LangGraph versions
            for event in schema_designer_app.stream(initial_state, stream_mode="updates"):
                for node_name, node_data in event.items():
                    # Merge the incoming node delta into our tracking state
                    current_state.update(node_data)
                    
                    if node_name == "generation":
                        current_iter = current_state.get("iterations", 1)
                        st.markdown(f"🔄 **Loop {current_iter}:** Generation Node executed.")
                        
                        if "errors" in node_data and len(node_data["errors"]) > 0:
                            st.warning("LLM output failed Pydantic parsing. Retrying...")
                    
                    elif node_name == "validation":
                        is_valid = node_data.get("is_Valid", current_state.get("is_Valid"))
                        
                        st.markdown("⚙️ **Validator Node:** Compiling SQL in RAM...")
                        
                        if is_valid:
                            st.success("Compilation Successful! Zero syntax errors.")
                        else:
                            error_list = current_state.get("errors", [])
                            latest_error = error_list[-1] if len(error_list) > 0 else "Unknown Compilation Error"
                            st.error(f"Compilation Failed. Intercepted Traceback:\n\n`{latest_error}`")
                            st.info("Routing back to Generation Node for self-correction...")

    # Evaluate the manually accumulated state rather than just the final delta
    with col1:
        st.subheader("Final Execution Result")
        
        if current_state.get("is_Valid"):
            st.success(f"Architecture stabilized after {current_state.get('iterations')} iteration(s).")
            
            st.markdown("### Compiled SQLite Script")
            st.code(current_state["schemaOutput"].raw_sql, language="sql")
            
            st.markdown("### Schema Table Structure")
            for table in current_state["schemaOutput"].tables:
                with st.expander(f"Table: {table.table_name}"):
                    for col in table.columns:
                        constraint_text = col.constraints if col.constraints else "None"
                        st.markdown(f"- `{col.name}` ({col.data_type}) | Constraints: {constraint_text}")
                        
        else:
            st.error("Execution Terminated: Agent hit the maximum iteration limit without compiling a valid schema.")
            st.markdown("### Final Traceback Logs")
            for i, err in enumerate(current_state.get("errors", [])):
                st.code(f"Loop {i+1}:\n{err}", language="text")