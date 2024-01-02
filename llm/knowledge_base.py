from phi.knowledge.combined import CombinedKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFKnowledgeBase
from phi.vectordb.pgvector import PgVector

from db.session import db_url

url_pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://www.family-action.org.uk/content/uploads/2019/07/meals-more-recipes.pdf"],
    # Store this knowledge base in llm.url_pdf_documents
    vector_db=PgVector(
        collection="url_pdf_documents",
        db_url=db_url,
        schema="llm",
    ),
    num_documents=2,
)

local_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/pdfs",
    # Store this knowledge base in llm.local_pdf_documents
    vector_db=PgVector(
        collection="local_pdf_documents",
        db_url=db_url,
        schema="llm",
    ),
    num_documents=3,
)

pdf_knowledge_base = CombinedKnowledgeBase(
    sources=[
        url_pdf_knowledge_base,
        local_pdf_knowledge_base,
    ],
    # Store this knowledge base in llm.pdf_documents
    vector_db=PgVector(
        collection="pdf_documents",
        db_url=db_url,
        schema="llm",
    ),
    num_documents=2,
)
