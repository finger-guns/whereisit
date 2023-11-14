JOB_REQUEST_STATUS_ENUM = {
    "create": """
    CREATE TYPE job_request_status_enum AS ENUM (
    'PENDING',
    'PROCESSING',
    'COMPLETED',
    'FAILED'
    );
    """,
}
