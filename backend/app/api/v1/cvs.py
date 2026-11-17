from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.v1.uploads import temporary_copy, validate_upload
from app.core.config import Settings, get_settings
from app.schemas.cv import CandidateProfile
from app.services.cv_parsing import UnreadableDocumentError, UnsupportedFormatError, parse_cv

router = APIRouter(prefix="/cvs", tags=["CV"])


@router.post(
    "/parse",
    response_model=CandidateProfile,
    summary="Parse an uploaded CV into a structured profile",
    responses={
        413: {"description": "File is larger than the upload limit"},
        415: {"description": "Unsupported file format"},
        422: {"description": "The document could not be read"},
    },
)
def parse_uploaded_cv(
    file: Annotated[UploadFile, File(description="CV as PDF, DOCX or TXT")],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CandidateProfile:
    """Nothing is stored: the file is parsed and the temporary copy is deleted."""
    suffix = validate_upload(file, settings)
    with temporary_copy(file, suffix) as path:
        try:
            return parse_cv(path, file_name=file.filename or "cv", today=settings.reference_date)
        except UnsupportedFormatError as error:
            raise HTTPException(415, str(error)) from error
        except UnreadableDocumentError as error:
            raise HTTPException(422, str(error)) from error
