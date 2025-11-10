"""Status schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class JobStatus(BaseModel):
    """Status information for a conversion job."""

    job_id: str = Field(..., description="Unique job identifier")
    filename: str = Field(..., description="Original filename")
    status: str = Field(
        ..., description="Job status: queued, processing, completed, failed"
    )
    progress: int = Field(default=0, description="Progress percentage (0-100)")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    download_url: str | None = Field(None, description="Download URL when completed")
    error: str | None = Field(None, description="Error message if job failed")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class BatchStatusResponse(BaseModel):
    """Response model for batch status request."""

    jobs: list[JobStatus] = Field(..., description="List of job statuses")

    @property
    def active_jobs(self) -> list[JobStatus]:
        """Get list of active (queued or processing) jobs."""
        return [job for job in self.jobs if job.status in ["queued", "processing"]]

    @property
    def completed_jobs(self) -> list[JobStatus]:
        """Get list of completed jobs."""
        return [job for job in self.jobs if job.status == "completed"]

    @property
    def failed_jobs(self) -> list[JobStatus]:
        """Get list of failed jobs."""
        return [job for job in self.jobs if job.status == "failed"]
