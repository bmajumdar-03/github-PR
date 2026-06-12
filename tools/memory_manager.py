# tools/memory_manager.py

import os
import json
from pathlib import Path

MEMORY_FILE_PATH = Path("/usr/local/google/home/bmajumdar/Glovo_githubPR/.memory_store.json")

class ADKMemoryService:
    """
    Coordinates semantic storage. Configured to fallback to a structured local JSON database 
    to preserve state across runtime execution sessions.
    """
    @staticmethod
    def store_memory(memory_entry: dict):
        """Saves structured feedback to persistent storage."""
        database = []
        if MEMORY_FILE_PATH.exists():
            try:
                with open(MEMORY_FILE_PATH, 'r') as f:
                    database = json.load(f)
            except json.JSONDecodeError:
                database = []

        # Avoid duplicates based on unique comment_id
        existing_ids = {item.get("comment_id") for item in database if "comment_id" in item}
        if memory_entry.get("comment_id") not in existing_ids:
            database.append(memory_entry)
            with open(MEMORY_FILE_PATH, 'w') as f:
                json.dump(database, f, indent=2)
            return f"Stored constraint successfully: {memory_entry.get('identified_error')}"
        return "Constraint already registered in memory bank."

    @staticmethod
    def retrieve_relevant_constraints(target_file_path: str) -> list:
        """Searches long-term memory for negative constraints matching a specific file or context."""
        if not MEMORY_FILE_PATH.exists():
            return []

        try:
            with open(MEMORY_FILE_PATH, 'r') as f:
                database = json.load(f)
        except Exception:
            return []

        # Basic exact-path or cross-cutting global rule matching
        matched_constraints = []
        for entry in database:
            affected = entry.get("affected_file", "")
            if affected == "global" or affected in target_file_path or target_file_path in affected:
                matched_constraints.append(entry)
        return matched_constraints

def persist_feedback_to_memory(feedback_json_str: str) -> str:
    """Parses a structured JSON list of feedback and records each as a long-term memory entry."""
    try:
        feedback_list = json.loads(feedback_json_str)
        stored_count = 0
        for item in feedback_list:
            res = ADKMemoryService.store_memory(item)
            if "successfully" in res:
                stored_count += 1
        return f"Successfully imported {stored_count} new constraints into long-term memory."
    except Exception as e:
        return f"Failed to ingest feedback: {str(e)}"

def retrieve_negative_constraints(target_file: str) -> str:
    """Returns constraints associated with the target file to shape prompting instructions."""
    constraints = ADKMemoryService.retrieve_relevant_constraints(target_file)
    if not constraints:
        return "No historical negative constraints found for this scope."
    return json.dumps(constraints, indent=2)