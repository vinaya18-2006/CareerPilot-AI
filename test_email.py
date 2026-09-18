from services.email_service import send_job_email
import pandas as pd

test_jobs = pd.DataFrame([
    {
        "title": "Python Developer",
        "company": "Test Company",
        "location": "Bangalore",
        "url": "https://example.com/job"
    }
])

print("📧 Testing email...")

result = send_job_email(test_jobs)

if result:
    print("✅ EMAIL TEST PASSED")
else:
    print("❌ EMAIL TEST FAILED")