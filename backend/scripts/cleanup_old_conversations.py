"""
Cleanup script for stale conversations.

Deletes LangGraph checkpoint history (the full chat memory) plus our own
`conversation_activity` tracking row for any thread_id that hasn't sent a
message in more than INACTIVITY_DAYS days.

Meant to run on a schedule (see .github/workflows/cleanup-conversations.yml)
so anonymous visitor chat history doesn't pile up forever in Postgres.

Usage:
    uv run python scripts/cleanup_old_conversations.py
"""

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from app.config import get_settings

INACTIVITY_DAYS = 30

settings = get_settings()

pool = ConnectionPool(
    conninfo=settings.database_url,
    max_size=5,
    kwargs={"autocommit": True, "prepare_threshold": 0},
    check=ConnectionPool.check_connection,
)

with pool.connection() as conn:
    rows = conn.execute(
        """
        SELECT thread_id FROM conversation_activity
        WHERE last_seen < now() - make_interval(days => %s)
        """,
        (INACTIVITY_DAYS,),
    ).fetchall()

stale_thread_ids = [row[0] for row in rows]

if not stale_thread_ids:
    print("No stale conversations to clean up.")
else:
    checkpointer = PostgresSaver(pool)
    for thread_id in stale_thread_ids:
        checkpointer.delete_thread(thread_id)
        with pool.connection() as conn:
            conn.execute(
                "DELETE FROM conversation_activity WHERE thread_id = %s",
                (thread_id,),
            )
    print(f"Deleted {len(stale_thread_ids)} stale conversation(s) (inactive > {INACTIVITY_DAYS} days).")

pool.close()
