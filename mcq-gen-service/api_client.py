import requests
import asyncio
import os
from typing import Any, Dict, Optional

# Get service URLs from environment variables, with fallbacks to localhost
PARSE_DOC_SERVICE_URL = os.environ.get('PARSE_DOC_SERVICE_URL', 'http://127.0.0.1:8000')
REACT_AGENT_SERVICE_URL = os.environ.get('REACT_AGENT_SERVICE_URL', 'http://127.0.0.1:8003')
PROMPT_TEMPLATE_SERVICE_URL = os.environ.get('PROMPT_TEMPLATE_SERVICE_URL', 'http://127.0.0.1:8004')
FORMAT_SERVICE_URL = os.environ.get('FORMAT_SERVICE_URL', 'http://127.0.0.1:8005')

async def run_in_executor(executor, func, *args, **kwargs):
    return await asyncio.get_event_loop().run_in_executor(executor, lambda: func(*args, **kwargs))

async def parse_doc(executor, files: Dict) -> Dict[str, Any]:
    """Parse a document using the document parsing service"""
    try:
        response = await run_in_executor(
            executor,
            requests.post,
            f'{PARSE_DOC_SERVICE_URL}/parse-doc',
            files=files,
            timeout=1000.0
        )
        return response.json()
    except requests.Timeout:
        return {"error": f"Connection to parse-doc service timed out. Make sure the service is running at {PARSE_DOC_SERVICE_URL}"}
    except requests.ConnectionError:
        return {"error": f"Failed to connect to parse-doc service. Make sure the service is running at {PARSE_DOC_SERVICE_URL}"}
    except Exception as e:
        return {"error": f"An error occurred while parsing document: {str(e)}"}

async def create_vector_store(executor, store_id: str, content: str) -> Dict[str, Any]:
    """Create a vector store from parsed document content"""
    try:
        vector_store_response = await run_in_executor(
            executor,
            requests.post,
            f'{REACT_AGENT_SERVICE_URL}/create-vector-store',
            json={"store_id": store_id, "content": content},
            timeout=1000.0
        )
        return vector_store_response.json()
    except Exception as e:
        print(f"Warning: Failed to create vector store: {str(e)}")
        return {"error": f"Failed to create vector store: {str(e)}"}

async def create_query_engine_tool(executor, store_id: str, type: str, number_of_answers: int) -> Dict[str, Any]:
    """Create a query engine tool using the react-agent-service"""
    try:
        response = await run_in_executor(
            executor,
            requests.post,
            f'{REACT_AGENT_SERVICE_URL}/create-query-engine-tool',
            params={"store_id": store_id, "type": type, "number_of_answers": number_of_answers},
            timeout=1000.0
        )
        return response.json()
    except requests.Timeout:
        return {"error": f"Connection to react-agent-service timed out. Make sure the service is running at {REACT_AGENT_SERVICE_URL}"}
    except requests.ConnectionError:
        return {"error": f"Failed to connect to react-agent-service. Make sure the service is running at {REACT_AGENT_SERVICE_URL}"}
    except Exception as e:
        return {"error": f"An error occurred while creating query engine tool: {str(e)}"}

async def create_mcq(executor, store_id: str, topic: str, quantity: int, difficulty: str,
                     number_of_answers: int, recheck: bool, type: str) -> Dict[str, Any]:
    """Create a vector store from parsed document content"""
    try:
        mcq_response = await run_in_executor(
            executor,
            requests.post,
            f'{REACT_AGENT_SERVICE_URL}/mcq-gen',
            params={
                "store_id": store_id,
                "topic": topic,
                "quantity": quantity,
                "difficulty": difficulty,
                "number_of_answers": number_of_answers,
                "recheck": recheck,
                "type": type
            },
            timeout=1000.0
        )
        return mcq_response.json()
    except Exception as e:
        print(f"Warning: Failed to create vector store: {str(e)}")
        return {"error": f"Failed to create vector store: {str(e)}"}