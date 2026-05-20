# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import argparse
import os
import sys
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def main():
    parser = argparse.ArgumentParser(description="Secure HTML Delivery - Encrypt HTML into standalone AES-256-GCM file")
    parser.add_argument("--input", required=True, help="Input HTML file path")
    parser.add_argument("--token", required=True, help="Encryption token/passphrase")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--title", default="Secure Document", help="Document title for the encrypted HTML wrapper")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        sys.exit(1)

    with open(args.input, 'rb') as f:
        html_content = f.read()

    # Derive 256-bit key using SHA-256
    key = hashlib.sha256(args.token.encode('utf-8')).digest()

    # Generate 12-byte IV
    iv = os.urandom(12)

    # Encrypt payload
    aesgcm = AESGCM(key)
    encrypted_with_tag = aesgcm.encrypt(iv, html_content, None)

    # In cryptography's AESGCM, the auth tag is the last 16 bytes
    ciphertext = encrypted_with_tag[:-16]
    auth_tag = encrypted_with_tag[-16:]

    # Encode to base64
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
    auth_tag_b64 = base64.b64encode(auth_tag).decode('utf-8')

    # Generate Output HTML template
    new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>{args.title}</title>
    <style>
        body {{ margin: 0; background-color: #0d1117; color: white; font-family: -apple-system, system-ui, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center; }}
        .lock-container {{ border: 1px solid #30363d; padding: 3rem; border-radius: 8px; background: #161b22; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        h2 {{ margin-top: 0; color: #58a6ff; }}
        .icon {{ font-size: 3rem; margin-bottom: 1rem; }}
        p {{ color: #8b949e; line-height: 1.5; font-size: 0.95rem; }}
        .error {{ color: #f85149; margin-top: 1rem; font-weight: bold; display: none; }}
    </style>
</head>
<body>
    <div class="lock-container">
        <div class="icon">🔒</div>
        <h2>Encrypted Document</h2>
        <p>{args.title} is secured via AES-256-GCM. <br><br>Please scan the official QR code or provide the token in the URL to decrypt and view the document.</p>
        <p class="error" id="errorMsg">Access Denied: Invalid or missing token.</p>
    </div>

    <script>
        const ciphertextB64 = "{ciphertext_b64}";
        const ivB64 = "{iv_b64}";
        const authTagB64 = "{auth_tag_b64}";

        // Utility to convert Base64 to Uint8Array
        function b64ToArrayBuffer(base64) {{
            var binary_string = window.atob(base64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {{
                bytes[i] = binary_string.charCodeAt(i);
            }}
            return bytes.buffer;
        }}

        async function decryptPayload(token) {{
            try {{
                // Hash token to form 256-bit key
                const encoder = new TextEncoder();
                const keyMaterial = await window.crypto.subtle.digest("SHA-256", encoder.encode(token));
                
                // Import key
                const cryptoKey = await window.crypto.subtle.importKey(
                    "raw",
                    keyMaterial,
                    "AES-GCM",
                    false,
                    ["decrypt"]
                );

                // Prepare ciphertext: GCM appends auth tag to ciphertext in WebCrypto
                const ctBuffer = b64ToArrayBuffer(ciphertextB64);
                const tagBuffer = b64ToArrayBuffer(authTagB64);
                const combined = new Uint8Array(ctBuffer.byteLength + tagBuffer.byteLength);
                combined.set(new Uint8Array(ctBuffer), 0);
                combined.set(new Uint8Array(tagBuffer), ctBuffer.byteLength);

                // Decrypt
                const decryptedBuffer = await window.crypto.subtle.decrypt(
                    {{ name: "AES-GCM", iv: b64ToArrayBuffer(ivB64) }},
                    cryptoKey,
                    combined.buffer
                );

                // Decode string and overwrite document
                const decryptedStr = new TextDecoder().decode(decryptedBuffer);
                document.open();
                document.write(decryptedStr);
                document.close();
            }} catch (err) {{
                console.error(err);
                document.getElementById('errorMsg').style.display = 'block';
            }}
        }}

        function checkAndDecrypt() {{
            const hash = window.location.hash;
            if (hash && hash.startsWith('#token=')) {{
                // Hide error message initially
                document.getElementById('errorMsg').style.display = 'none';
                const tokenUrl = hash.replace('#token=', '');
                decryptPayload(tokenUrl);
            }} else {{
                document.getElementById('errorMsg').style.display = 'block';
            }}
        }}

        // Execution Check
        window.onload = checkAndDecrypt;
        window.addEventListener('hashchange', checkAndDecrypt);
    </script>
</body>
</html>
"""

    with open(args.output, 'w') as f:
        f.write(new_html)

    print(f"Successfully generated encrypted HTML at: {args.output}")

if __name__ == "__main__":
    main()
