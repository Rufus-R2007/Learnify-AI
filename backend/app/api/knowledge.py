"""
Knowledge API endpoints for Learnify AI.
Allows inspecting and exploring verified syllabus knowledge records and FAQs.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.schemas import KnowledgeRecord, KnowledgeListResponse
from app.database import (
    get_all_knowledge,
    get_knowledge_by_id,
    search_knowledge,
    get_all_faqs,
)

router = APIRouter()


@router.get("/", response_model=KnowledgeListResponse)
async def list_knowledge(
    search: Optional[str] = Query(None, description="Optional search term to filter records"),
    unit: Optional[int] = Query(None, description="Filter by syllabus unit (1-5)"),
) -> KnowledgeListResponse:
    """
    List verified educational knowledge records.
    Supports optional keyword search and unit filtering.
    """
    try:
        if search:
            tokens = search.lower().split()
            records_data = search_knowledge(tokens)
        else:
            records_data = get_all_knowledge()

        if unit is not None:
            records_data = [r for r in records_data if r.get("unit") == unit]

        records = [
            KnowledgeRecord(
                id=r["id"],
                title=r["title"],
                content=r["content"],
                keywords=r.get("keywords"),
                topic_id=r.get("topic_id"),
                topic_name=r.get("topic_name"),
                unit=r.get("unit"),
                source_id=r.get("source_id"),
                source_name=r.get("source_name"),
                source_desc=r.get("source_desc"),
                relevance_score=r.get("relevance_score"),
            )
            for r in records_data
        ]

        return KnowledgeListResponse(total=len(records), records=records)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge records: {str(e)}"
        )


@router.get("/faqs")
async def list_faqs():
    """List system FAQs."""
    try:
        return {"faqs": get_all_faqs()}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving FAQs: {str(e)}"
        )


@router.get("/{record_id}", response_model=KnowledgeRecord)
async def get_knowledge(record_id: str) -> KnowledgeRecord:
    """Retrieve a single knowledge record by ID."""
    record = get_knowledge_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Knowledge record with ID '{record_id}' not found"
        )

    return KnowledgeRecord(
        id=record["id"],
        title=record["title"],
        content=record["content"],
        keywords=record.get("keywords"),
        topic_id=record.get("topic_id"),
        topic_name=record.get("topic_name"),
        unit=record.get("unit"),
        source_id=record.get("source_id"),
        source_name=record.get("source_name"),
        source_desc=record.get("source_desc"),
    )
