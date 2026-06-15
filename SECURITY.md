# Security Policy

LLMgram OSS is a public demo extraction. Do not submit credentials, private DMs, X/Twitter cookies, FTP settings, analytics secrets, subscriber databases, deployment logs or production data.

Recommended checks before publishing:

```bash
python -m compileall app.py
pytest -q
gitleaks detect --no-git --source .
```
