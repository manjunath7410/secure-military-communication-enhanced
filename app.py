from flask import Flask, render_template, request, jsonify
import hashlib
import math
import time

app = Flask(__name__)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    shift = int(shift) % 26
    if decrypt:
        shift = -shift
    result = []
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)


def atbash_cipher(text: str) -> str:
    result = []
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr(90 - (ord(char) - 65)))
        elif "a" <= char <= "z":
            result.append(chr(122 - (ord(char) - 97)))
        else:
            result.append(char)
    return "".join(result)


def rot13_cipher(text: str) -> str:
    return caesar_cipher(text, 13)


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    key = "".join(c for c in key.upper() if c.isalpha())
    if not key:
        raise ValueError("Vigenere key must contain at least one letter.")

    result, key_index = [], 0
    for char in text:
        if char.isalpha() and char.isascii():
            base = 65 if char.isupper() else 97
            k = ord(key[key_index % len(key)]) - 65
            if decrypt:
                k = -k
            result.append(chr((ord(char) - base + k) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def transform(text, algorithm, key="", decrypt=False):
    algorithm = algorithm.lower()
    if algorithm == "caesar":
        return caesar_cipher(text, int(key), decrypt)
    if algorithm == "atbash":
        return atbash_cipher(text)
    if algorithm == "rot13":
        return rot13_cipher(text)
    if algorithm == "vigenere":
        return vigenere_cipher(text, str(key), decrypt)
    raise ValueError("Unsupported cipher.")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/encrypt")
def encrypt():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    algorithm = data.get("algorithm", "caesar")
    key = data.get("key", data.get("shift", 3))

    if not isinstance(message, str):
        return jsonify({"error": "Message must be text."}), 400
    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        result = transform(message, algorithm, key, False)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid key or cipher settings."}), 400

    return jsonify({
        "result": result,
        "algorithm": algorithm,
        "integrity_hash": sha256(message)
    })


@app.post("/api/decrypt")
def decrypt():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    algorithm = data.get("algorithm", "caesar")
    key = data.get("key", data.get("shift", 3))

    if not isinstance(message, str):
        return jsonify({"error": "Ciphertext must be text."}), 400
    if not message:
        return jsonify({"error": "Ciphertext cannot be empty."}), 400

    try:
        result = transform(message, algorithm, key, True)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid key or cipher settings."}), 400

    return jsonify({
        "result": result,
        "algorithm": algorithm,
        "integrity_hash": sha256(result)
    })


@app.post("/api/attack")
def attack():
    data = request.get_json(silent=True) or {}
    ciphertext = data.get("message", "")
    algorithm = data.get("algorithm", "caesar")

    if not isinstance(ciphertext, str) or not ciphertext:
        return jsonify({"error": "Ciphertext is required."}), 400
    if algorithm.lower() != "caesar":
        return jsonify({"error": "Brute-force attack is demonstrated for Caesar Cipher only."}), 400

    candidates = []
    common_words = {"THE", "AND", "THIS", "ATTACK", "MEET", "AT", "TO", "HELLO", "WORLD", "IS", "OF", "IN"}
    for shift in range(26):
        candidate = caesar_cipher(ciphertext, shift, decrypt=True)
        words = set(re.findall(r"[A-Za-z]+", candidate.upper()))
        score = len(words & common_words)
        candidates.append({"key": shift, "text": candidate, "score": score})

    candidates.sort(key=lambda x: (-x["score"], x["key"]))
    return jsonify({"candidates": candidates, "warning": "Caesar Cipher has only 26 possible shifts."})


@app.post("/api/hash")
def hash_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str):
        return jsonify({"error": "Message must be text."}), 400
    return jsonify({"sha256": sha256(message)})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "secure-military-communication", "version": "2.0"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
