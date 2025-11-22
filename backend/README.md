# DefenderC2-backend

Backend service for DefenderC2 project using FastAPI.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    *   Windows: `venv\Scripts\activate`
    *   Linux/Mac: `source venv/bin/activate`

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

Run the start script:

```bash
chmod +x start.sh
./start.sh
```

The server will start at `http://127.0.0.1:8000`.

## API Usage

### Health Check

```bash
curl -X GET http://127.0.0.1:8000/api/v1/health
```

Response:
```json
{"status": "ok"}
```

### Generate Code

```bash
curl -X POST http://127.0.0.1:8000/api/v1/codes \
  -H "Content-Type: application/json" \
  -d '{"owner": "admin", "ttl_seconds": 3600}'
```

Response:
```json
{"central_id": "1A2B3C4D5E6F", "expires_at": "2023-10-27T10:00:00+00:00"}
```

## Testing

Run tests with pytest:

```bash
pytest
```
