# Secure Military Communication System v2

Educational Flask project demonstrating:
- Separate encryption and decryption workflows
- Caesar, Vigenère, Atbash and ROT13
- Caesar brute-force cryptanalysis lab
- SHA-256 integrity fingerprints
- Responsive security-focused UI
- `/health` deployment health endpoint

## Local run
```bash
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Production
Gunicorn is included for Linux hosting:
```bash
gunicorn app:app
```

## Important
This is an academic cryptography demonstration. Classical ciphers such as Caesar,
Vigenère, Atbash and ROT13 are not appropriate for real military or production
security. Real systems should use modern authenticated encryption and proper key
management.
