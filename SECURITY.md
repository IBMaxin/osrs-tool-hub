# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of OSRS Tool Hub seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send details to the repository maintainers (check repository for contact information)
2. **GitHub Security Advisory**: Use GitHub's private vulnerability reporting feature if available

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Updates**: We will provide regular updates on the status of the vulnerability
- **Resolution**: We will work to resolve the issue as quickly as possible

### Disclosure Policy

- We will work with you to understand and resolve the issue quickly
- We will credit you for the discovery (if desired)
- We will not take legal action against security researchers who:
  - Act in good faith
  - Avoid privacy violations, destruction of data, and interruption or degradation of our service
  - Do not exploit a security issue beyond what is necessary to demonstrate the vulnerability

## Security Best Practices

### For Users

1. **Environment Variables**: Never commit `.env` files or expose environment variables
2. **Database Security**: Use strong passwords for database connections
3. **CORS Configuration**: Restrict CORS origins to your production domains only
4. **Rate Limiting**: Keep rate limiting enabled in production
5. **HTTPS**: Always use HTTPS in production (never HTTP)
6. **Updates**: Keep dependencies up to date
7. **Secrets**: Never hardcode API keys, passwords, or tokens

### For Developers

1. **Input Validation**: Always validate and sanitize user input
2. **SQL Injection**: Use parameterized queries (SQLModel handles this)
3. **XSS Prevention**: Sanitize output and use Content Security Policy
4. **Authentication**: Implement proper authentication (currently uses client-side user IDs)
5. **Authorization**: Verify user permissions before allowing actions
6. **Error Handling**: Don't expose sensitive information in error messages
7. **Dependencies**: Regularly update dependencies and audit for vulnerabilities
8. **Logging**: Never log secrets, tokens, or user identifiers

### Configuration Security

#### Environment Variables

- Store sensitive configuration in environment variables, not in code
- Use `.env` files for local development (never commit them)
- Use secure secret management in production (e.g., AWS Secrets Manager, HashiCorp Vault)

#### Database Security

- Use strong, unique passwords for database users
- Restrict database network access (firewall rules)
- Use SSL/TLS for database connections in production
- Regularly backup databases
- Limit database user permissions (principle of least privilege)

#### API Security

- **Rate Limiting**: Enabled by default (100 req/min, 10 req/min strict)
- **CORS**: Configure allowed origins explicitly
- **User-Agent**: Required for OSRS Wiki API (prevents 403 errors)
- **Input Validation**: All inputs validated via Pydantic models
- **Error Messages**: Generic error messages to avoid information leakage

### Deployment Security

1. **HTTPS Only**: Use HTTPS/TLS for all production traffic
2. **Security Headers**: Configure security headers (X-Frame-Options, X-Content-Type-Options, etc.)
3. **Firewall**: Restrict access to backend ports
4. **Updates**: Keep system and dependencies updated
5. **Monitoring**: Set up monitoring and alerting for security events
6. **Backups**: Regular automated backups of database
7. **Access Control**: Limit SSH and server access

### Known Security Considerations

#### Current Limitations

1. **No Authentication**: Currently uses client-side user IDs (UUIDs in localStorage)
   - Users can access any user_id's data if they know the ID
   - Future versions will include proper authentication

2. **Rate Limiting**: IP-based rate limiting
   - Can be bypassed with multiple IPs
   - Consider user-based rate limiting in future

3. **CORS**: Configured via environment variables
   - Ensure production CORS origins are correctly set
   - Wildcard origins (`*`) are not recommended

#### Recommendations for Production

1. **Implement Authentication**: Add JWT or session-based authentication
2. **User-Based Rate Limiting**: Complement IP-based with user-based limits
3. **API Keys**: Consider API key authentication for programmatic access
4. **WAF**: Use a Web Application Firewall (WAF) for additional protection
5. **DDoS Protection**: Use CDN/DDoS protection services
6. **Security Scanning**: Regular security scans and penetration testing

## Security Updates

Security updates will be released as patch versions (e.g., 0.1.1, 0.1.2) and documented in:
- [CHANGELOG.md](CHANGELOG.md) (security fixes marked)
- GitHub Security Advisories (if applicable)
- Release notes

## Dependencies

We use the following security practices for dependencies:

- **Regular Updates**: Dependencies are regularly updated
- **Vulnerability Scanning**: We monitor for known vulnerabilities
- **Minimal Dependencies**: We keep the dependency list minimal
- **Trusted Sources**: We only use dependencies from trusted sources (PyPI, npm)

### Dependency Security Tools

- **Python**: `pip-audit`, `safety`
- **Node.js**: `npm audit`, `snyk`

## Compliance

This project follows security best practices but does not claim compliance with specific standards (e.g., SOC 2, ISO 27001). For compliance requirements, please conduct your own security assessment.

## Contact

For security-related questions or concerns, please contact the repository maintainers.

---

*Last Updated: 2026-01-28*
