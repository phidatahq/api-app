from phi.storage.conversation.postgres import PgConversationStorage

from db.session import db_url

pdf_conversation_storage = PgConversationStorage(
    table_name="pdf_conversations",
    db_url=db_url,
    schema="llm",
)
