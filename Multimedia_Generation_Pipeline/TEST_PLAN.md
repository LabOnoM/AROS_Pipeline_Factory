# Comprehensive Test Plan: AROS Cloud Federation User Center

This document outlines the testing strategy for verifying the recently developed Unified User Center and the Google OAuth authentication flow.

## 1. Authentication & Cloud Run Environment Tests

### 1.1 Google OAuth Flow
- **Action**: Navigate to the production URL (`https://aros.bs-gou.com`).
- **Action**: Click "Sign In" and select "Continue with Google".
- **Expected Result**: User is redirected to Google, authenticates, and is redirected back to the `/dashboard` route. A NextAuth session is established.
- **Verification**: The top right User Navigation dropdown displays the authenticated user's avatar and name.

### 1.2 Sandbox Developer Login (Fallback)
- **Action**: Click "Sign In" and select "Sandbox Developer Login".
- **Action**: Enter `test@aros.dev` and "Test User".
- **Expected Result**: User is instantly authenticated without a password and redirected to the `/dashboard`.

### 1.3 Missing Environment Variable Handling
- **Action**: Remove `NEXTAUTH_URL` or `GOOGLE_CLIENT_ID` from the environment.
- **Expected Result**: NextAuth should gracefully log the error, and the UI should clearly state that OAuth is disabled or fallback to the Developer Sandbox.

## 2. Unified User Center (GUI Workflows)

### 2.1 Overview Tab
- **Action**: Click the "Overview & Activity" tab.
- **Expected Result**: Displays active agent skills, benchmark evaluations, and total tokens consumed.
- **Action**: Click the "Refresh Data" button.
- **Expected Result**: The API (`/marketplace/stats`, etc.) is called and the UI gracefully updates or shows a loading pulse.

### 2.2 API Keys Management
- **Action**: Navigate to "API Keys" tab.
- **Action**: Enter a label (e.g., "Lab Node 1") and click "Generate Key".
- **Expected Result**: The backend creates an `ak_` prefixed key. The plaintext key is revealed *exactly once* in an amber warning box.
- **Action**: Click the "Copy" clipboard icon.
- **Expected Result**: The key is copied to the system clipboard, and a success toast appears.
- **Action**: Click the Trash icon to revoke a key.
- **Expected Result**: A browser confirmation dialog appears. If confirmed, the key is revoked via `DELETE /auth/keys/{id}` and removed from the list.

### 2.3 Billing & Subscriptions (Placeholder)
- **Action**: Navigate to "Billing & Credits" tab.
- **Expected Result**: Displays the active plan tier and the available refill balance (default: $5.00 for new users).
- **Action**: Click "Upgrade to Pro Workspace" under the Stripe Sandbox UI.
- **Expected Result**: The system simulates a Stripe checkout redirect, pauses for 1.5 seconds, upgrades the tier, injects credits, and displays a success toast.

### 2.4 Workspace Settings
- **Action**: Navigate to "Workspace Settings" tab.
- **Expected Result**: Displays user's Google email and allows editing the Organization Name.
- **Action**: Update organization name and save.
- **Expected Result**: Triggers `PUT /users/organization` and updates the sidebar globally.

## 3. Cross-Platform Compatibility
- **macOS (Safari/Chrome)**: Verify responsive flex layouts and glassmorphism backdrop filters render correctly.
- **Ubuntu/Linux (Firefox/Chrome)**: Verify typography and smooth micro-animations.
- **Windows (Edge/Chrome)**: Confirm scrollbars on the snapshot history table function without overflowing the parent glass panel.

## 5. VPEP Pipeline API & GUI Validation

### 5.1 GCS Signed Upload & Job Creation
- **Action**: In the Pipeline Studio, select a video file and an SOP docx file, then click "Upload".
- **Expected Result**: Frontend calls `POST /api/pipelines/vpep/upload-url`. The backend deducts 1 credit and returns signed URLs.
- **Verification**: Ensure direct PUT requests to GCS succeed with `200 OK`. The job should appear in the `VPEPJob` database table as `status: created`.

### 5.2 Background Processing & Polling
- **Action**: Click "Run Pipeline".
- **Expected Result**: The backend queues the background task via `POST /api/pipelines/vpep/run` and returns `202 Accepted`.
- **Verification**: Poll `GET /api/pipelines/vpep/status/{id}`. Confirm the `current_stage` field transitions through all stages (Downloading, Stage 1 to Stage 6) and completes without timeouts.

### 5.3 Result Downloads & Artifact Generation
- **Action**: Wait for pipeline completion.
- **Expected Result**: A "Download Interactive Report" button appears.
- **Verification**: Call `GET /api/pipelines/vpep/results/{id}`. Ensure the signed URLs generated are valid for 24 hours. Download the HTML, PDF, and DOCX files (created by Stage 5.5) and verify they open without corruption.

### 5.4 Sharing & Export Workflows
- **Action**: Click "Share Job".
- **Expected Result**: `POST /api/pipelines/vpep/share/{id}` generates a `share_token` and a unique shareable URL.
- **Verification**: Access the `/shared/{token}` endpoint from an incognito window (unauthenticated) and verify the download URLs are still served correctly.
- **Action**: Click "Export ZIP".
- **Expected Result**: `GET /api/pipelines/vpep/export/{id}` zips all artifacts from GCS.
- **Verification**: Extract the downloaded ZIP. Verify relative paths within `Interactive_Report.html` load local CSS, images, and videos properly.

## 6. Full Cross-Platform Backend Execution Validation
- **macOS / Apple Silicon**: Verify `sys.executable` targets the local venv and successfully executes FFmpeg subprocesses without segmentation faults.
- **Ubuntu Linux (Serverless)**: Ensure Cloud Run background tasks run to completion within the 3600-second timeout. Confirm `/tmp` mounts provide sufficient ephemeral storage for video processing.
- **Windows / WSL2**: Verify `os.path.join` standardizes paths correctly and subprocess arguments do not fail on spaces in directory names.
