### Data Flow
1. **Job Submission:**
    - A client submits a job via the `/jobs/` endpoint of the `where_is_it_api`.
    - The job details are stored in PostgreSQL and sent to the "to-scrape" queue.
2. **Scraping Process:**
    - The `where_is_it_scraper` picks up the job, scrapes the required data from Rotten Tomatoes, and stores the raw HTML bytes in PostgreSQL.
    - The raw data is then sent to the "to-format" queue.
3. **Formatting Process:**
    - The `where_is_it_formatter` processes the HTML bytes, extracts necessary information, stores it in its database, and then places the Base64 formatted HTML in Redis against the `job_request_id`.
4. **Retrieval of Results:**
    - Clients can query the status or results of their job using the `GET /job/{job_id}` endpoint on `where_is_it_api`, which retrieves the processed data from Redis.
