from pydantic import BaseModel, ConfigDict
from app.esquemas.capitulo import ChapterOut
from app.esquemas.pagina import PageOut

class ChapterWithPagesOut(BaseModel):
    chapter: ChapterOut
    pages: list[PageOut]

    model_config = ConfigDict(from_attributes=True)  