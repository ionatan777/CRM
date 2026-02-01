from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.db.session import get_db
from app.models.backup import BackupJob, BackupStatus
from app.services.backup_service import BackupService
from app.api.deps import get_current_user
import uuid

router = APIRouter()

@router.post("/", status_code=202)
def create_backup(
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create Job Record
    job = BackupJob(tenant_id=current_user.tenant_id, status=BackupStatus.PENDING)
    db.add(job)
    db.commit()
    db.refresh(job)

    # Trigger Async Task
    background_tasks.add_task(run_backup_task, db, current_user.tenant_id, job.id)

    return {"job_id": job.id, "status": "pending"}

def run_backup_task(db: Session, tenant_id: uuid.UUID, job_id: uuid.UUID):
    # Wrapper to run service
    service = BackupService(db)
    service.perform_backup(tenant_id, job_id)

@router.get("/{job_id}")
def get_backup(
    job_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(BackupJob).filter(
        BackupJob.id == uuid.UUID(job_id),
        BackupJob.tenant_id == current_user.tenant_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Backup not found")
    
    if job.status == BackupStatus.PENDING:
        return {"status": "pending"}
    
    if job.status == BackupStatus.FAILED:
        return {"status": "failed"}

    return FileResponse(job.file_path, media_type='application/json', filename=f"backup-{job_id}.json")
