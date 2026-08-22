# Baga Ink Canonical JSON Test Vectors

Each vector directory contains:

- `input.json`: UTF-8 JSON input;
- `canonical.hex`: expected RFC 8785 canonical UTF-8 bytes encoded as lowercase hex;
- `sha256.txt`: expected digest as `sha256:<lowercase hex>`.

These vectors are language-independent conformance assets. Signed Baga statements MUST produce exactly these bytes. TUF metadata does not use these vectors.
