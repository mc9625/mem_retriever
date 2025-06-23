# declarative_memory_api.py - ENGLISH VERSION

from cat.mad_hatter.decorators import plugin, endpoint
from cat.auth.permissions import check_permissions, AuthResource, AuthPermission
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from cat.log import log
import time
import json

class DeclarativeMemorySettings(BaseModel):
    """Settings for the declarative memory endpoint."""
    
    default_k: int = Field(
        default=5,
        title="Default number of results",
        description="Default number of results to return",
        ge=1,
        le=50
    )
    
    default_threshold: float = Field(
        default=0.7,
        title="Default similarity threshold",
        description="Default similarity threshold for results",
        ge=0.0,
        le=1.0
    )
    
    max_k: int = Field(
        default=20,
        title="Maximum number of results",
        description="Maximum number of results that can be requested",
        ge=1,
        le=100
    )
    
    enable_metadata_filter: bool = Field(
        default=True,
        title="Enable metadata filters",
        description="Allow filtering results by metadata"
    )
    
    enable_content_preview: bool = Field(
        default=True,
        title="Enable content preview",
        description="Include content preview in results"
    )
    
    preview_length: int = Field(
        default=200,
        title="Preview length",
        description="Number of characters for content preview",
        ge=50,
        le=1000
    )

@plugin
def settings_model():
    """Returns the plugin settings model."""
    return DeclarativeMemorySettings

# Pydantic models for requests and responses
class MemorySearchRequest(BaseModel):
    """Model for memory search request."""
    
    query: str = Field(
        description="Search query for declarative memory",
        min_length=1,
        max_length=1000
    )
    
    k: Optional[int] = Field(
        default=None,
        description="Number of results to return",
        ge=1,
        le=100
    )
    
    threshold: Optional[float] = Field(
        default=None,
        description="Similarity threshold (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    metadata_filter: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadata filters (e.g. {'source': 'document.pdf'})"
    )
    
    include_scores: bool = Field(
        default=True,
        description="Include similarity scores in results"
    )
    
    include_metadata: bool = Field(
        default=True,
        description="Include metadata in results"
    )

class MemoryResult(BaseModel):
    """Model for a single memory result."""
    
    content: str = Field(description="Document content")
    content_preview: Optional[str] = Field(description="Content preview")
    score: Optional[float] = Field(description="Similarity score")
    metadata: Optional[Dict[str, Any]] = Field(description="Document metadata")
    document_id: Optional[str] = Field(description="Document ID")

class MemorySearchResponse(BaseModel):
    """Model for search response."""
    
    query: str = Field(description="Query used for search")
    results: List[MemoryResult] = Field(description="Search results")
    total_results: int = Field(description="Total number of results found")
    search_time_ms: float = Field(description="Search time in milliseconds")
    parameters: Dict[str, Any] = Field(description="Parameters used for search")
    embedder_info: Dict[str, Any] = Field(description="Information about the embedder used")

@endpoint.get("/declarative-memory/search")
def search_declarative_memory_get(
    query: str,
    k: Optional[int] = None,
    threshold: Optional[float] = None,
    include_scores: bool = True,
    include_metadata: bool = True,
    stray=check_permissions(AuthResource.MEMORY, AuthPermission.READ)
) -> MemorySearchResponse:
    """
    Search declarative memory via GET request.
    
    Args:
        query: Search query
        k: Number of results (optional)
        threshold: Similarity threshold (optional)
        include_scores: Include similarity scores
        include_metadata: Include metadata
        
    Returns:
        MemorySearchResponse: Search results
    """
    
    request_data = MemorySearchRequest(
        query=query,
        k=k,
        threshold=threshold,
        include_scores=include_scores,
        include_metadata=include_metadata
    )
    
    return _perform_memory_search(request_data, stray)

@endpoint.post("/declarative-memory/search")
def search_declarative_memory_post(
    request: MemorySearchRequest,
    stray=check_permissions(AuthResource.MEMORY, AuthPermission.READ)
) -> MemorySearchResponse:
    """
    Search declarative memory via POST request with advanced filters.
    
    Args:
        request: Search parameters
        
    Returns:
        MemorySearchResponse: Search results
    """
    
    return _perform_memory_search(request, stray)

def _perform_memory_search(request: MemorySearchRequest, stray) -> MemorySearchResponse:
    """
    Performs declarative memory search using the correct API.
    
    Args:
        request: Search parameters
        stray: StrayCat object
        
    Returns:
        MemorySearchResponse: Search results
    """
    
    start_time = time.time()
    
    try:
        # Load plugin settings
        settings = stray.mad_hatter.get_plugin().load_settings()
        
        # Determine search parameters
        k = request.k if request.k is not None else settings.get("default_k", 5)
        threshold = request.threshold if request.threshold is not None else settings.get("default_threshold", 0.7)
        
        # Validate parameters
        max_k = settings.get("max_k", 20)
        if k > max_k:
            raise ValueError(f"Requested number of results ({k}) exceeds maximum allowed ({max_k})")
        
        # Log search request
        log.info(f"Searching declarative memory for user {stray.user_id}: '{request.query}' (k={k}, threshold={threshold})")
        
        # STEP 1: Convert query to embedding using Cat's embedder
        log.info("Converting query to embedding...")
        query_embedding = stray.embedder.embed_query(request.query)
        log.info(f"Query embedding generated, size: {len(query_embedding)}")
        
        # STEP 2: Search declarative memory with correct API
        log.info("Searching declarative memory with embedding...")
        
        # Search parameters
        search_params = {
            "embedding": query_embedding,
            "k": k,
            "threshold": threshold
        }
        
        # NOTE: metadata_filter is not directly supported by recall_memories_from_embedding
        # but we can filter after retrieval
        memory_results = stray.memory.vectors.declarative.recall_memories_from_embedding(**search_params)
        
        log.info(f"Found {len(memory_results) if memory_results else 0} results before filtering")
        
        # STEP 3: Process and filter results
        results = []
        
        if memory_results:
            for doc_with_score in memory_results:
                try:
                    # Format: (Document, score)
                    doc = doc_with_score[0]
                    score = doc_with_score[1] if len(doc_with_score) > 1 else None
                    
                    # Apply metadata filters if specified
                    if (request.metadata_filter and 
                        settings.get("enable_metadata_filter", True)):
                        
                        doc_metadata = getattr(doc, 'metadata', {})
                        
                        # Check if document passes filters
                        filter_passed = True
                        for filter_key, filter_value in request.metadata_filter.items():
                            if filter_key not in doc_metadata:
                                filter_passed = False
                                break
                            
                            # Support for simple pattern matching
                            if isinstance(filter_value, str) and filter_value.startswith("*"):
                                if not str(doc_metadata[filter_key]).endswith(filter_value[1:]):
                                    filter_passed = False
                                    break
                            elif doc_metadata[filter_key] != filter_value:
                                filter_passed = False
                                break
                        
                        if not filter_passed:
                            continue
                    
                    # Create content preview if enabled
                    content = getattr(doc, 'page_content', str(doc))
                    content_preview = None
                    
                    if settings.get("enable_content_preview", True):
                        preview_length = settings.get("preview_length", 200)
                        content_preview = (content[:preview_length] + "..." 
                                         if len(content) > preview_length 
                                         else content)
                    
                    # Extract metadata
                    metadata = getattr(doc, 'metadata', {}) if request.include_metadata else None
                    
                    # Build result
                    result = MemoryResult(
                        content=content,
                        content_preview=content_preview,
                        score=float(score) if (request.include_scores and score is not None) else None,
                        metadata=metadata,
                        document_id=metadata.get("id") if metadata else None
                    )
                    
                    results.append(result)
                    
                except Exception as e:
                    log.error(f"Error processing memory result: {e}")
                    continue
        
        # Calculate search time
        search_time_ms = (time.time() - start_time) * 1000
        
        # Log final results
        log.info(f"Returning {len(results)} results after filtering in {search_time_ms:.2f}ms for user {stray.user_id}")
        
        # Build response
        response = MemorySearchResponse(
            query=request.query,
            results=results,
            total_results=len(results),
            search_time_ms=search_time_ms,
            parameters={
                "k": k,
                "threshold": threshold,
                "metadata_filter": request.metadata_filter,
                "include_scores": request.include_scores,
                "include_metadata": request.include_metadata
            },
            embedder_info={
                "name": stray.memory.vectors.declarative.embedder_name,
                "size": stray.memory.vectors.declarative.embedder_size,
                "embedding_dimensions": len(query_embedding)
            }
        )
        
        return response
        
    except ValueError as e:
        log.warning(f"Validation error in memory search for user {stray.user_id}: {str(e)}")
        raise e
        
    except Exception as e:
        log.error(f"Error in declarative memory search for user {stray.user_id}: {str(e)}")
        import traceback
        log.error(f"Full traceback: {traceback.format_exc()}")
        raise Exception(f"Error during search: {str(e)}")

@endpoint.get("/declarative-memory/stats")
def get_memory_stats(
    stray=check_permissions(AuthResource.MEMORY, AuthPermission.READ)
) -> Dict[str, Any]:
    """
    Returns declarative memory statistics.
    
    Returns:
        Dict: Memory statistics
    """
    
    try:
        # Basic statistics
        stats = {
            "user_id": stray.user_id,
            "memory_type": "declarative",
            "timestamp": time.time(),
            "embedder_info": {
                "name": stray.memory.vectors.declarative.embedder_name,
                "size": stray.memory.vectors.declarative.embedder_size
            }
        }
        
        # Try to get document count
        try:
            # Direct method if available
            if hasattr(stray.memory.vectors.declarative, 'get_all_points'):
                all_points = stray.memory.vectors.declarative.get_all_points()
                stats["total_documents"] = len(all_points) if all_points else 0
            else:
                stats["total_documents"] = "method_not_available"
                
            # Collection info
            stats["collection_name"] = stray.memory.vectors.declarative.collection_name
            
        except Exception as e:
            log.warning(f"Could not retrieve document count: {e}")
            stats["total_documents"] = "error_counting"
            stats["count_error"] = str(e)
        
        log.info(f"Memory stats retrieved for user {stray.user_id}")
        
        return stats
        
    except Exception as e:
        log.error(f"Error retrieving memory stats for user {stray.user_id}: {str(e)}")
        raise Exception(f"Error retrieving statistics: {str(e)}")

@endpoint.get("/declarative-memory/collections")
def get_memory_collections(
    stray=check_permissions(AuthResource.MEMORY, AuthPermission.READ)
) -> Dict[str, Any]:
    """
    Returns information about available memory collections.
    
    Returns:
        Dict: Collections information
    """
    
    try:
        collections_info = {}
        
        # Declarative memory information
        try:
            collections_info["declarative"] = {
                "name": stray.memory.vectors.declarative.collection_name,
                "embedder_name": stray.memory.vectors.declarative.embedder_name,
                "embedder_size": stray.memory.vectors.declarative.embedder_size,
                "description": "Long term factual memory"
            }
        except Exception as e:
            collections_info["declarative"] = {"error": str(e)}
        
        # Episodic memory information
        try:
            collections_info["episodic"] = {
                "name": stray.memory.vectors.episodic.collection_name,
                "embedder_name": stray.memory.vectors.episodic.embedder_name,
                "embedder_size": stray.memory.vectors.episodic.embedder_size,
                "description": "Conversation and interaction memory"
            }
        except Exception as e:
            collections_info["episodic"] = {"error": str(e)}
        
        # Procedural memory information
        try:
            collections_info["procedural"] = {
                "name": stray.memory.vectors.procedural.collection_name,
                "embedder_name": stray.memory.vectors.procedural.embedder_name,
                "embedder_size": stray.memory.vectors.procedural.embedder_size,
                "description": "Tools and procedures memory"
            }
        except Exception as e:
            collections_info["procedural"] = {"error": str(e)}
        
        log.info(f"Collections info retrieved for user {stray.user_id}")
        
        return {
            "collections": collections_info,
            "user_id": stray.user_id,
            "timestamp": time.time()
        }
        
    except Exception as e:
        log.error(f"Error retrieving collections info for user {stray.user_id}: {str(e)}")
        raise Exception(f"Error retrieving information: {str(e)}")

# Utility endpoint for testing connection
@endpoint.get("/declarative-memory/health")
def health_check() -> Dict[str, str]:
    """
    Health check for declarative memory endpoint.
    
    Returns:
        Dict: Service status
    """
    
    return {
        "status": "healthy",
        "service": "declarative-memory-api",
        "version": "1.0.0",
        "timestamp": str(time.time())
    }