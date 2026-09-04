# Continuous Camera Proctoring & Exam Integrity Specification

## Overview
ExamHub includes an enterprise-grade Continuous Camera Proctoring and Academic Honesty Monitoring engine designed for high-stakes institutional assessments.

## Key Capabilities
1. **Teacher Authorization Toggle**: Instructors can mandate or waive video proctoring per examination directly from the Exam Creation Studio.
2. **Real-Time Client Telemetry**:
   - Continuous browser webcam streaming via `MediaStream` API.
   - Live face detection guidelines and framing crosshairs.
   - Audio volume threshold analysis for ambient noise spikes.
   - Tab switch, window blur, and developer tools inspection detection.
3. **Instructor Command Console**:
   - Real-time candidate telemetry cards.
   - Integrity risk scoring algorithm (0 to 100).
   - Instant warning broadcast to active student sessions.
   - Proctor-initiated early termination with automated submission.
