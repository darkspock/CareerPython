# Security Policy

## Supported Versions

We actively support the following versions of CareerPython with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of CareerPython seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 Private Disclosure

**Do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security vulnerabilities privately by:

1. **Email**: Send details to [extjmv@gmail.com](mailto:extjmv@gmail.com)
2. **Subject**: Use the subject line "SECURITY: [Brief description]"
3. **Encryption**: For sensitive information, you may request our PGP key

### 📝 What to Include

Please include as much of the following information as possible:

- **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass)
- **Location of the vulnerability** (file path, URL, function name)
- **Steps to reproduce** the vulnerability
- **Potential impact** of the vulnerability
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up questions

### 🚀 Response Timeline

We will acknowledge receipt of your vulnerability report within **48 hours** and provide:

- Initial assessment within **7 days**
- Regular progress updates during investigation
- Target resolution timeline based on severity
- Credit in our security advisory (if desired)

### 🏆 Security Researcher Recognition

We appreciate security researchers who help keep CareerPython secure:

- Public recognition in our Hall of Fame (with your permission)
- Mention in release notes for security fixes
- LinkedIn recommendation for significant findings
- Potential collaboration opportunities

## 🛡️ Security Measures

CareerPython implements multiple security layers:

### Authentication & Authorization
- JWT token-based authentication
- Argon2 password hashing
- Role-based access control (RBAC)
- Session management with secure tokens

### Data Protection
- Input validation with Pydantic models
- SQL injection prevention via SQLAlchemy ORM
- XSS protection through output encoding
- CSRF protection for state-changing operations

### Infrastructure Security
- Environment variable isolation
- Secret management best practices
- Docker container security
- HTTPS encryption in production

### Monitoring & Logging
- Security event logging
- Failed authentication tracking
- Suspicious activity detection
- Error reporting without sensitive data exposure

## 🔧 Security Configuration

### Environment Variables
Never commit sensitive information to the repository:

```env
# ❌ DON'T DO THIS
SECRET_KEY=actual-secret-key-here

# ✅ DO THIS INSTEAD
SECRET_KEY=your-secret-key-here-change-in-production
```

### Database Security
- Use strong database passwords
- Enable database connection encryption
- Regularly update database software
- Implement proper backup encryption

### API Security
- Rate limiting on all endpoints
- Input validation on all requests
- Proper error handling without information leakage
- CORS configuration for allowed origins

## 🚨 Security Best Practices for Contributors

### Code Review Security Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user inputs
- [ ] Proper error handling without sensitive data exposure
- [ ] Authentication/authorization checks where needed
- [ ] SQL queries use parameterized statements
- [ ] File uploads are properly validated and sandboxed

### Dependencies
- Regularly update dependencies to patch known vulnerabilities
- Use `uv audit` to check for known security issues
- Pin dependency versions for reproducible builds
- Review third-party packages before adding them

### Testing Security
- Include security test cases
- Test authentication and authorization scenarios
- Validate input sanitization
- Test error handling scenarios

## 📊 Vulnerability Severity Levels

We use the following severity levels for vulnerabilities:

### 🚨 Critical (CVSS 9.0-10.0)
- Remote code execution
- SQL injection with data access
- Authentication bypass
- **Response time**: 24-48 hours

### 🔴 High (CVSS 7.0-8.9)
- Privilege escalation
- Sensitive data exposure
- Cross-site scripting (stored)
- **Response time**: 3-7 days

### 🟡 Medium (CVSS 4.0-6.9)
- Cross-site scripting (reflected)
- Information disclosure
- Denial of service
- **Response time**: 7-14 days

### 🔵 Low (CVSS 0.1-3.9)
- Minor information disclosure
- Security configuration issues
- **Response time**: 14-30 days

## 🔄 Security Update Process

1. **Vulnerability confirmed** and severity assessed
2. **Fix developed** and tested in private branch
3. **Security advisory** prepared
4. **Coordinated disclosure** with timeline
5. **Patch released** with security notes
6. **Public disclosure** after patch is available

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Python Security Best Practices](https://python.org/dev/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

## 🙏 Security Hall of Fame

We thank the following security researchers for their responsible disclosure:

<!-- Security researchers who have reported vulnerabilities will be listed here -->

*No security vulnerabilities have been reported yet.*

## 📞 Contact

For security-related questions or concerns:

- **Email**: [extjmv@gmail.com](mailto:extjmv@gmail.com)
- **LinkedIn**: [Juan Macías](https://linkedin.com/in/juanmaciasvela)

---

Thank you for helping keep CareerPython and our users safe!