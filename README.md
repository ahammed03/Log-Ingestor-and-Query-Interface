# Log-Ingestor-and-Query-Interface




This project provides a system to ingest logs and query them based on various attributes. It includes functionalities for logging data ingestion via API and a user interface for querying logs.

## Features

### Log Ingestion

- Receive log data via API endpoint for storage.
- Validate and store log attributes like level, message, timestamp, etc.

### Query Interface

- Interface to query logs based on multiple criteria such as level, timestamp, message, etc.
- Pagination for navigating through logs.

## Setup

### Prerequisites

- Python 
- Django
- Tailwind CSS (for interface styling)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dyte-submissions/november-2023-hiring-ahammed03.git
    cd log_ingestor_project
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the server:

    ```bash
    python manage.py runserver 3000
    ```

## Usage

### Log Ingestion

- **Endpoint:** `/ingest/`
- **Method:** POST
- **Data Format:**

    ```json
    {
      "level": "error",
      "message": "Failed to connect to DB",
      "resourceId": "server-1234",
      "timestamp": "2023-09-15T08:00:00Z",
      "traceId": "abc-xyz-123",
      "spanId": "span-456",
      "commit": "5e5342f",
      "metadata": {
        "parentResourceId": "server-0987"
      }
    }
    ```

- **Response:**

    - `200 OK`: Log ingested successfully
    - `400 Bad Request`: Invalid or missing attributes in log data
    - `500 Internal Server Error`: Error during ingestion

### Query Interface

- **Endpoint:** `/query/`
- **Parameters:**
    - `level`: Filter logs by log level
    - `start_date`, `end_date`: Filter logs within a specific date range
    - Other available parameters for filtering logs
- **Response:** Display matching logs with pagination.

## Technologies Used

- Python
- Django
- Tailwind CSS

### Scripts

#### PowerShell

Use this script to post data through PowerShell:

```powershell
# Sample log data
$logData = '{
    "level": "error",
    "message": "Failed to connect to DB",
    "resourceId": "server-1234",
    "timestamp": "2023-09-15T08:00:00Z",
    "traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}'

# Define your endpoint where you want to send the log data
$endpoint = "http://127.0.0.1:3000/ingest/"

# Send the log data using Invoke-RestMethod at regular intervals
while ($true) {
    Invoke-RestMethod -Uri $endpoint -Method POST -Body $logData -ContentType 'application/json'
    Start-Sleep -Seconds 10  # Adjust the time interval as needed
}
```
###BASH

```bash
# Sample log data in a JSON file
echo '{
    "level": "error",
    "message": "Failed to connect to DB",
    "resourceId": "server-1234",
    "timestamp": "2023-09-15T08:00:00Z",
    "traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}' > log_data.json

# Define your endpoint URL
endpoint="http://127.0.0.1:3000/ingest/"

# Continuously send log data every 10 seconds
while true
do
    curl -X POST -H "Content-Type: application/json" -d @log_data.json $endpoint
    sleep 10  # Adjust the time interval as needed
done
```






