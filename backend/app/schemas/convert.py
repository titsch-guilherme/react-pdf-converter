"""Conversion schemas."""

from pydantic import BaseModel, Field


class JobInfo(BaseModel):
    """Information about a conversion job."""

    job_id: str = Field(..., description="Unique job identifier")
    filename: str = Field(..., description="Original filename")
    status: str = Field(
        ..., description="Job status: queued, processing, completed, failed"
    )
    error: str | None = Field(None, description="Error message if job failed")


class ConversionResponse(BaseModel):
    """Response model for batch conversion request."""

    jobs: list[JobInfo] = Field(..., description="List of created conversion jobs")

    @property
    def successful_jobs(self) -> list[JobInfo]:
        """Get list of successfully queued jobs."""
        return [job for job in self.jobs if job.status == "queued"]

    @property
    def failed_jobs(self) -> list[JobInfo]:
        """Get list of jobs that failed to start."""
        return [job for job in self.jobs if job.status == "failed"]
