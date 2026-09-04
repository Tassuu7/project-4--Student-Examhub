# Institutional Certificate Authority & Verification Specification

## Overview
The ExamHub Certificate Authority empowers educators and institutional leaders to issue, manage, verify, and revoke tamper-evident digital completion certificates.

## Key Capabilities
1. **Cryptographic Signatures**: Certificates are cryptographically signed using HMAC-SHA256 digests encoding candidate ID, exam ID, issue timestamp, and percentage score.
2. **Public Verification Portal**: Public verification portal resolves certificate IDs and hashes against the institutional ledger.
3. **Teacher Credential Authority**:
   - Issue custom credentials directly from the Instructor Console.
   - 1-click issuance from passing exam candidate scorecards.
   - Real-time certificate status tracking (Active vs. Revoked).
   - Audit trail tracking revocation reasons and timestamps.
