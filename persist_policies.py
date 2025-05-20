import uuid, os
from sqlmodel import SQLModel, Field, create_engine, Session, Column, String, JSON, UUID

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    ""
)


class ExtractedPolicies(SQLModel, table=True):
    __tablename__ = "abstract_with_extracted_policies"
    id: str = Field(default=None, primary_key=True)
    abstract: str = Field(sa_column=Column(String))
    extracted_data: dict = Field(sa_column=Column(JSON))


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SQLModel.metadata.create_all(engine)


def persist_policies(extracted_policy, text) -> int:
    """
    Persist the article metadata in the database via sqlalchemy.
    
    Args:
        article (PaperTaxonomy): The article metadata to persist
        
    Returns:
        int: The ID of the newly created article record
    """
    with Session(engine) as session:
        # Convert the article to a dictionary

        # Create a new ArticleMetadata instance
        print(f"Extracted policy: {extracted_policy}")
        db_article = ExtractedPolicies(
            id=uuid.uuid4().__str__(),
            abstract=text,
            extracted_data=extracted_policy
        )

        # Add and commit to database
        session.add(db_article)
        session.commit()
        session.refresh(db_article)

        return db_article.id