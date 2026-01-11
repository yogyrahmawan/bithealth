from typing import Dict, Any
from langgraph.graph import StateGraph, END

from models import WorkflowState, QueryResult
from services.document_service import DocumentService
from exceptions import WorkflowError

class WorkflowService:
    """Service for managing LangGraph workflows"""

    def __init__(self, document_service: DocumentService):
        self.document_service = document_service
        self.workflow = None
        self._build_workflow()

    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(dict)

        # Add nodes
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate_answer", self._generate_answer_node)

        # Set entry point
        workflow.set_entry_point("retrieve")

        # Add edges
        workflow.add_edge("retrieve", "generate_answer")
        workflow.add_edge("generate_answer", END)

        # Compile workflow
        self.workflow = workflow.compile()

    def _retrieve_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve documents node"""
        try:
            query = state["query"]
            result = self.document_service.query_documents(query, top_k=5)

            state["retrieved_docs"] = [doc.dict() for doc in result.documents]
            state["processing_steps"] = state.get("processing_steps", []) + ["Retrieved documents"]
            return state
        except Exception as e:
            state["error"] = f"Retrieval failed: {str(e)}"
            raise WorkflowError(f"Workflow retrieval failed: {str(e)}")

    def _generate_answer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate answer node"""
        if state.get("error"):
            state["final_answer"] = f"Error occurred: {state['error']}"
            return state

        retrieved_docs = state.get("retrieved_docs", [])
        if not retrieved_docs:
            state["final_answer"] = "No relevant documents found."
        else:
            # Simple answer generation - in real app, use LLM
            top_doc = retrieved_docs[0]
            content = top_doc.get("content", "")
            state["final_answer"] = f"Based on the document: {content[:200]}..."

        state["processing_steps"] = state.get("processing_steps", []) + ["Generated final answer"]
        return state

    def execute_query(self, query: str) -> QueryResult:
        """Execute a query through the workflow"""
        try:
            initial_state = {
                "query": query,
                "retrieved_docs": [],
                "final_answer": "",
                "processing_steps": [],
                "error": None
            }

            final_state = self.workflow.invoke(initial_state)

            # Convert back to QueryResult
            from ..models import RetrievedDocument
            retrieved_docs = [
                RetrievedDocument(**doc) for doc in final_state.get("retrieved_docs", [])
            ]

            return QueryResult(
                query=query,
                documents=retrieved_docs,
                answer=final_state.get("final_answer", ""),
                processing_time=0.0  # Would need to track this properly
            )
        except Exception as e:
            raise WorkflowError(f"Workflow execution failed: {str(e)}")

    def is_healthy(self) -> bool:
        """Check if workflow is ready"""
        return self.workflow is not None
