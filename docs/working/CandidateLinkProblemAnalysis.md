# Candidate Link Problem Analysis

## Current Flow

### 1. Registration Initiation (`InitiateRegistrationCommand`)
```
Email submitted → Create UserRegistration (with random token) → Save to DB → Send email with link
```

- Token generated: `secrets.token_urlsafe(32)` (43 chars, URL-safe base64)
- Token stored in `user_registrations.verification_token` (unique, indexed)
- Token expires in 24 hours (`token_expires_at`)
- Link format: `{FRONTEND_URL}/candidate/registration/verify/{token}`

### 2. Verification (`VerifyRegistrationCommand`)
```
Token received → Lookup by token → Validate → Create user/candidate → Return access_token
```

Key validation points:
1. `get_by_verification_token(token)` → If not found: **"Invalid verification token"**
2. `is_verified()` → If true: Returns existing data (idempotent)
3. `is_expired()` → If true: **"Verification token has expired"**

## Identified Failure Points

### Critical Issue: Token-Only Lookup
The current system relies **entirely** on finding the token in the database. If the token doesn't exist:
- **No fallback** - System fails immediately
- **No recovery** - User must restart the entire registration process

### Potential Causes of Token Not Found:

| Cause | Likelihood | Impact |
|-------|------------|--------|
| DB save failed (transaction rollback) | Medium | Token never persisted |
| Token cleanup job ran | Low | Token deleted prematurely |
| Database migration/restore issue | Low | Token lost |
| URL encoding/decoding issue | Medium | Token corrupted in transit |
| Copy-paste error by user | Medium | Partial token |
| Email client modified URL | Medium | Token truncated or encoded |

### URL Encoding Concern
Token `V4QfoZHTztg66-DDZ8f3VoStsEXsTl4Gx9wPClFWJoI` contains `-` which is URL-safe, but some email clients may:
- Double-encode the URL
- Truncate long URLs
- Add tracking parameters

## Current Idempotency (Partial)

**Already idempotent:**
- Re-clicking a verified link → Returns success with existing user data
- Multiple registration attempts with same email+job_position → Resends email for existing registration

**NOT idempotent:**
- Token not found → Fails permanently
- Token expired → Fails permanently (no way to recover)

## Proposed Solution: Self-Contained Tokens with Fallback

### Option A: JWT-based Token (Recommended)

Replace random token with signed JWT containing:
```python
{
    "email": "user@example.com",
    "company_id": "optional",
    "job_position_id": "optional",
    "registration_id": "ulid",  # For lookup optimization
    "iat": timestamp,
    "exp": timestamp + 24h
}
```

**Benefits:**
- Token is self-contained - works even if DB record missing
- Expiration built into token - no DB lookup needed for expiry check
- Can verify signature - prevents tampering
- Includes all context needed to create user/candidate

**Flow:**
1. Decode JWT → Extract email and metadata
2. Try to find registration by `registration_id` (optimization)
3. If not found → Find/create user by email
4. Create candidate if not exists
5. Create job application if `job_position_id` present
6. Return access token

### Option B: Hybrid Approach (Simpler)

Keep current random token but add email-based fallback:
1. Try `get_by_verification_token(token)`
2. If not found → Try `get_by_email(email_from_url_param)`
3. If found by email → Verify and proceed

**Requires:** Adding email as URL parameter (less clean)

## Recommended Implementation: Option A

### Changes Required:

1. **Token Generation** (`user_registration.py:108`)
   - Replace `secrets.token_urlsafe(32)` with JWT creation
   - Include email, company_id, job_position_id, registration_id

2. **Token Verification** (`verify_registration_command.py`)
   - Add JWT decoding logic
   - Implement fallback: DB lookup → JWT-based creation
   - Handle expired JWT gracefully (offer to resend)

3. **URL Structure**
   - Keep same: `/candidate/registration/verify/{jwt_token}`
   - JWT is URL-safe when encoded properly

### Idempotency Matrix (After Fix)

| Scenario | Current | After Fix |
|----------|---------|-----------|
| Token found, not verified | ✅ Works | ✅ Works |
| Token found, already verified | ✅ Returns existing | ✅ Returns existing |
| Token found, expired | ❌ Fails | ✅ Offers resend |
| Token NOT found (DB issue) | ❌ Fails | ✅ Creates from JWT |
| Token corrupted | ❌ Fails | ❌ Fails (unavoidable) |
| Expired JWT | ❌ Fails | ✅ Offers resend by email |

## Security Considerations

1. **JWT Signing**: Use HS256 with SECRET_KEY
2. **Short expiration**: 24-48 hours max
3. **No sensitive data**: Only email and IDs in token
4. **Rate limiting**: Prevent brute-force on email-based creation

## Files to Modify

1. `src/auth_bc/user_registration/domain/entities/user_registration.py` - Token generation
2. `src/auth_bc/user_registration/application/commands/verify_registration_command.py` - Main logic
3. `src/auth_bc/user_registration/application/commands/send_verification_email_command.py` - URL generation
4. Add new service: `src/auth_bc/user_registration/domain/services/verification_token_service.py`

## Implementation Priority

1. **High**: JWT token generation and verification
2. **Medium**: Expired token handling with resend option
3. **Low**: Email-based fallback for legacy tokens
