# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | ✅        |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in this project, please follow the responsible disclosure process below.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

1. **GitHub Private Vulnerability Reporting**: Use GitHub's built-in private advisory feature to report the issue confidentially:  
   [Report a vulnerability](../../security/advisories/new)

2. **Include in your report**:
   - A description of the vulnerability and its potential impact
   - Steps to reproduce the issue
   - Any proof-of-concept code or screenshots (if applicable)
   - Your suggested fix (if you have one)

### What to Expect

- **Acknowledgement**: We will acknowledge receipt of your report within **48 hours**.
- **Assessment**: We will investigate and provide an initial assessment within **7 days**.
- **Fix timeline**: We aim to release a fix within **30 days** for critical issues. We will keep you informed of progress.
- **Credit**: We will credit you in the release notes (unless you prefer to remain anonymous).

## Security Best Practices for Contributors

- Never commit API keys, private keys, tokens, or passwords to this repository.
- Always use environment variables (`.env` file, never committed) for secrets.
- Ensure `.env` is listed in `.gitignore` before adding any credentials.
- Use placeholder values in `.env.template` files (e.g., `ODYSSEY_API_KEY=ody_your_api_key_here`).
- Restrict CORS origins to specific domains in production — never use `allow_origins=["*"]` in production deployments.
- If you accidentally commit a secret, rotate it immediately and use `git filter-repo` to purge it from history.

## Known Security Considerations

- **CORS**: The backend restricts allowed origins via the `CORS_ALLOWED_ORIGINS` environment variable. Set this to your exact frontend domain(s) in production.
- **API Keys**: The Odyssey API key is loaded exclusively from the environment (`ODYSSEY_API_KEY`). Never hardcode it in source files.
- **Logging**: The application does not log API key values or prefixes.
