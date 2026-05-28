from langgraph.graph import StateGraph, END
from state import State
from nodes import generationNode, validationNode

def routerAfterValidation(state: State) -> str:
    isValid = state.get("is_Valid", False)
    iterations = state.get("iterations", 0)

    if isValid:
        print("Validation successful. Ending process.")
        return END
    
    if not isValid and iterations < 3:
        print(f"Validation failed. Iteration {iterations}/3. Retrying generation.")
        return "generation"

    print("Validation failed after 3 iterations. Ending process.")
    return END

def buildGraph():
    workflow = StateGraph(State)
    workflow.add_node("generation", generationNode)
    workflow.add_node("validation", validationNode)

    workflow.set_entry_point("generation")
    workflow.add_edge("generation", "validation")

    workflow.add_conditional_edges(
        "validation",
        routerAfterValidation,
        {
            "generation": "generation",
            END: END
        }
    )

    app = workflow.compile()
    return app

schema_designer_app = buildGraph()