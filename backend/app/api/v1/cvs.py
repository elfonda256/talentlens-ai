import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.schemas.cv import CandidateProfile
from app.services.cv_parsing import (
    SUPPORTED_SUFFIXES,
    UnreadableDocumentError,
    UnsupportedFormatError,
    parse_cv,
)

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
    file_name = file.filename or "cv"
    suffix = Path(file_name).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(
            415,
            f"Format {suffix or 'tanpa ekstensi'} tidak didukung. Gunakan PDF, DOCX, atau TXT.",
        )
    if file.size is not None and file.size > settings.max_upload_bytes:
        raise HTTPException(
            413,
            f"Ukuran berkas melebihi {settings.max_upload_mb} MB.",
        )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / f"upload{suffix}"
        with tmp_path.open("wb") as target:
            shutil.copyfileobj(file.file, target)
        try:
            return parse_cv(tmp_path, file_name=file_name, today=settings.reference_date)
        except UnsupportedFormatError as error:
            raise HTTPException(415, str(error)) from error
        except UnreadableDocumentError as error:
            raise HTTPException(422, str(error)) from error
