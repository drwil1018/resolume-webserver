# Docker Connection to Resolume

When running in Docker, the backend needs to connect to Resolume Avenue running on your host machine.

## How It Works

- The backend container uses `host.docker.internal` instead of `localhost` to connect to Resolume Avenue
- This special DNS name resolves to the host machine's IP from inside Docker containers
- The switch happens automatically during container build via `config.docker.py`

## Troubleshooting Connection Issues

If you encounter connection errors like:

```
HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /api/v1/...
```

Make sure:

1. **Resolume Avenue is running** on your host machine
2. **Web Server is enabled** in Resolume: View → Preferences → OSC/Web
3. **Port 8080** is set in Resolume's Web Server settings

## Testing the Connection

Run the included test script to verify connectivity:

```bash
./test-resolume-connection.sh
```

If test #1 succeeds but test #2 fails, the Docker configuration is working as expected.

## Manual Fix

If you need to manually change the API URL, edit `backend/config.docker.py` and rebuild:

```bash
docker-compose build backend
docker-compose up -d
```
