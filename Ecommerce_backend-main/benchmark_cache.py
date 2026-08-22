import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def time_request():
    start = time.perf_counter()
    response = requests.get(f"{BASE_URL}/products/")
    end = time.perf_counter()
    duration_ms = (end - start) * 1000
    return duration_ms, response.status_code

print("Benchmarking GET /products/ (Cache-Aside pattern)\n")

duration1, status1 = time_request()
print(f"Call 1 (expected: cache MISS, hits database):")
print(f"  Status: {status1} | Time: {duration1:.2f} ms\n")

duration2, status2 = time_request()
print(f"Call 2 (expected: cache HIT, hits Redis):")
print(f"  Status: {status2} | Time: {duration2:.2f} ms\n")

duration3, status3 = time_request()
print(f"Call 3 (expected: cache HIT, hits Redis):")
print(f"  Status: {status3} | Time: {duration3:.2f} ms\n")

improvement = ((duration1 - duration2) / duration1) * 100
print(f"Performance improvement (Call 1 → Call 2): {improvement:.1f}% faster")
print(f"Raw difference: {duration1 - duration2:.2f} ms saved per request")