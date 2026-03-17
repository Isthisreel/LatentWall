# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

### How to Report

1. Email the maintainers at the address listed on the [GitHub profile](https://github.com/Isthisreel) with the subject line: `[SECURITY] LatentWall Vulnerability Report`
2. Include a description of the vulnerability, steps to reproduce, and any potential impact.
3. You will receive an acknowledgement within 72 hours and a resolution timeline within 7 days.

### Scope

The following are in scope for security reports:

- Backend API (`backend/`) — FastAPI server, WebSocket endpoints, CORS configuration
- API key handling and secret management
- Dependencies with known CVEs (please include the CVE number if applicable)

### Out of Scope

- Vulnerabilities in third-party services (Odyssey API, Vosk, etc.)
- Issues that require physical access to the machine
- Social engineering attacks

## Security Best Practices for Deployment

- **Never commit real API keys or private keys** to source control.
- **Set `CORS_ORIGINS`** in your `.env` file to your specific frontend URL(s). If `CORS_ORIGINS` is not set the server logs a warning and falls back to `*` (local dev only). Example for production: `CORS_ORIGINS=https://your-app.example.com`
- **Rotate credentials immediately** if you suspect they have been exposed. Run `git log --all --full-history -S "ody_" -S "sk-" -S "AIza"` to audit git history for accidentally committed secrets.
- **Enable GitHub Secret Scanning, Dependabot, and CodeQL** on this repository for automated vulnerability detection.
