---
name: secure-html-delivery
description: Encrypt a standalone HTML document using AES-256-GCM for secure external delivery.
license: MIT
skill-author: Antigravity
---
# Secure HTML Delivery

Package an HTML document into a standalone, AES-256-GCM encrypted file that decrypts in the browser via a URL hash token.

## When to Use

- Use this skill to securely package grant proposals or sensitive data for external reviewers.
- Use this skill when you need to share results without requiring the recipient to have special software or accounts (just a browser and the URL with the token).

## Key Features

- Client-side decryption using WebCrypto API.
- Generates a standalone HTML file containing ciphertext, IV, and auth tag.
- Password/token is never sent to the server.

## Dependencies

- `Python`: `3.10+`
- `cryptography`

## Example Usage

```bash
python scripts/main.py --input report.html --token "MySecretToken123" --output secure_report.html --title "Grant Proposal"
```

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input` | string | - | Yes | Input HTML file path |
| `--token` | string | - | Yes | Encryption token/passphrase |
| `--output` | string | - | Yes | Output HTML file path |
| `--title` | string | "Secure Document" | No | Title for the HTML wrapper |
