---
**Shift Left:** Catch problems as early in the pipeline as possible. A bug caught in linting costs minutes; the same bug caught in production costs hours. Move checks upstream — static analysis before tests, tests before staging, staging before production.
**Faster is Safer:** Smaller batches and more frequent releases reduce risk, not increase it. A deployment with 3 changes is easier to debug than one with 30. Frequent releases build confidence in the release process itself.
Every change goes through these gates before merge:
name: CI
on:
pull_request:
branches: [main]
push:
branches: [main]
jobs:
quality:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with:
node-version: '22'
cache: 'npm'
- name: Install dependencies
run: npm ci
- name: Lint
run: npm run lint
- name: Type check
run: npx tsc --noEmit
- name: Test
run: npm test -- --coverage
- name: Build
run: npm run build
- name: Security audit
run: npm audit --audit-level=high
integration:
runs-on: ubuntu-latest
services:
postgres:
image: postgres:16
env:
POSTGRES_DB: testdb
POSTGRES_USER: ci_user
POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
ports:
- 5432:5432
options: >-
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with:
node-version: '22'
cache: 'npm'
- run: npm ci
- name: Run migrations
run: npx prisma migrate deploy
env:
DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
- name: Integration tests
run: npm run test:integration
env:
DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
> **Note:** Even for CI-only test databases, use GitHub Secrets for credentials rather than hardcoding values. This builds good habits and prevents accidental reuse of test credentials in other contexts.
e2e:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with:
node-version: '22'
cache: 'npm'
- run: npm ci
- name: Install Playwright
run: npx playwright install --with-deps chromium
- name: Build
run: npm run build
- name: Run E2E tests
run: npx playwright test
- uses: actions/upload-artifact@v4
if: failure()
with:
name: playwright-report
path: playwright-report/
The power of CI with AI agents is the feedback loop. When CI fails:
Feed it to the agent:
"The CI pipeline failed with this error:
**Key patterns:**
Every PR gets a preview deployment for manual testing:
deploy-preview:
runs-on: ubuntu-latest
if: github.event_name == 'pull_request'
steps:
- uses: actions/checkout@v4
- name: Deploy preview
run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
Feature flags decouple deployment from release. Deploy incomplete or risky features behind flags so you can:
**Flag lifecycle:** Create → Enable for testing → Canary → Full rollout → Remove the flag and dead code. Flags that live forever become technical debt — set a cleanup date when you create them.
Every deployment should be reversible:
name: Rollback
on:
workflow_dispatch:
inputs:
version:
description: 'Version to rollback to'
required: true
jobs:
rollback:
runs-on: ubuntu-latest
steps:
- name: Rollback deployment
run: |
version: 2
updates:
- package-ecosystem: npm
directory: /
schedule:
interval: weekly
open-pull-requests-limit: 5
- **Required reviews:** At least 1 approval before merge
- **Required status checks:** CI must pass before merge
- **Branch protection:** No force-pushes to main
- **Auto-merge:** If all checks pass and approved, merge automatically
When the pipeline exceeds 10 minutes, apply these strategies in order of impact:
**Example: caching and parallelism**
jobs:
lint:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with: { node-version: '22', cache: 'npm' }
- run: npm ci
- run: npm run lint
typecheck:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with: { node-version: '22', cache: 'npm' }
- run: npm ci
- run: npx tsc --noEmit
test:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
with: { node-version: '22', cache: 'npm' }
- run: npm ci
- run: npm test -- --coverage
skill-author: External/Merged
license: MIT
original-source: addyosmani/agent-skills
---|---|
| "CI is too slow" | Optimize the pipeline (see CI Optimization below), don't skip it. A 5-minute pipeline prevents hours of debugging. |
| "This change is trivial, skip CI" | Trivial changes break builds. CI is fast for trivial changes anyway. |
| "The test is flaky, just re-run" | Flaky tests mask real bugs and waste everyone's time. Fix the flakiness. |
| "We'll add CI later" | Projects without CI accumulate broken states. Set it up on day one. |
| "Manual testing is enough" | Manual testing doesn't scale and isn't repeatable. Automate what you can. |

## Red Flags

- No CI pipeline in the project
- CI failures ignored or silenced
- Tests disabled in CI to make the pipeline pass
- Production deploys without staging verification
- No rollback mechanism
- Secrets stored in code or CI config files (not secrets manager)
- Long CI times with no optimization effort

## Verification

After setting up or modifying CI:

- [ ] All quality gates are present (lint, types, tests, build, audit)
- [ ] Pipeline runs on every PR and push to main
- [ ] Failures block merge (branch protection configured)
- [ ] CI results feed back into the development loop
- [ ] Secrets are stored in the secrets manager, not in code
- [ ] Deployment has a rollback mechanism
- [ ] Pipeline runs in under 10 minutes for the test suite
