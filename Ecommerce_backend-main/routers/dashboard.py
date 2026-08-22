from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import datetime
import re

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

LOG_FILE = "logs/app.log"

def read_recent_logs(lines=500):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
        return all_lines[-lines:]
    except FileNotFoundError:
        return []

LOG_PATTERN = re.compile(
    r"log_requests:\d+ - (?P<method>\w+) (?P<path>\S+) \| Status: (?P<status>\d+) \| Duration: (?P<duration>[\d.]+)ms"
)

def parse_logs(lines):
    requests = []
    errors = []

    for line in lines:
        match = LOG_PATTERN.search(line)
        if not match:
            continue

        status = int(match.group("status"))
        duration = float(match.group("duration"))
        method = match.group("method")
        path = match.group("path")

        entry = {
            "method": method,
            "path": path,
            "status": status,
            "duration_ms": duration,
        }
        requests.append(entry)

        if status >= 400:
            errors.append({**entry, "raw": line.strip()})

    return requests, errors

def compute_stats(requests, errors):
    total = len(requests)
    if total == 0:
        return {
            "total_requests": 0,
            "avg_response_time_ms": 0,
            "error_count": 0,
            "error_rate_percent": 0,
        }

    total_duration = sum(r["duration_ms"] for r in requests)
    avg_duration = total_duration / total
    error_count = len(errors)
    error_rate = (error_count / total) * 100

    return {
        "total_requests": total,
        "avg_response_time_ms": round(avg_duration, 2),
        "error_count": error_count,
        "error_rate_percent": round(error_rate, 2),
    }

def check_system_health():
    health = {}

    try:
        from database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health["database"] = "healthy"
    except Exception:
        health["database"] = "unhealthy"

    try:
        from core.cache import redis_client
        redis_client.ping()
        health["redis"] = "healthy"
    except Exception:
        health["redis"] = "unhealthy"

    return health

@router.get("/stats")
def get_dashboard_stats():
    lines = read_recent_logs()
    requests, errors = parse_logs(lines)
    stats = compute_stats(requests, errors)
    health = check_system_health()

    recent_errors = [e["raw"] for e in errors[-10:]]

    return {
        "stats": stats,
        "health": health,
        "recent_errors": recent_errors,
    }

@router.get("", response_class=HTMLResponse)
def get_dashboard_page():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>API Monitoring Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        h1 { color: #333; }
        .cards { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 180px; }
        .card .label { font-size: 13px; color: #888; margin-bottom: 6px; }
        .card .value { font-size: 28px; font-weight: bold; }
        .healthy { color: green; }
        .unhealthy { color: red; }
        table { width: 100%; background: white; border-collapse: collapse; border-radius: 8px; overflow: hidden; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #eee; font-size: 13px; }
        th { background: #fafafa; }
    </style>
</head>
<body>
    <h1>API Monitoring Dashboard</h1>
    <div class="cards" id="cards"></div>
    <h3>Recent Errors</h3>
    <table>
        <thead><tr><th>Log Line</th></tr></thead>
        <tbody id="errors"></tbody>
    </table>

    <script>
        async function loadStats() {
            const res = await fetch('/dashboard/stats');
            const data = await res.json();

            const cards = document.getElementById('cards');
            cards.innerHTML = `
                <div class="card"><div class="label">Total Requests</div><div class="value">${data.stats.total_requests}</div></div>
                <div class="card"><div class="label">Avg Response Time</div><div class="value">${data.stats.avg_response_time_ms} ms</div></div>
                <div class="card"><div class="label">Error Rate</div><div class="value">${data.stats.error_rate_percent}%</div></div>
                <div class="card"><div class="label">Database</div><div class="value ${data.health.database}">${data.health.database}</div></div>
                <div class="card"><div class="label">Redis</div><div class="value ${data.health.redis}">${data.health.redis}</div></div>
            `;

            const errors = document.getElementById('errors');
            errors.innerHTML = data.recent_errors.map(e => `<tr><td>${e}</td></tr>`).join('');
        }

        loadStats();
        setInterval(loadStats, 5000);
    </script>
</body>
</html>
"""