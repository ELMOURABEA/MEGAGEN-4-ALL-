name: MeGaOcToOoN Agent
description: A lightweight companion service for the MeGaOcToOoN GitHub App that handles post-install onboarding, installation token exchange, webhook processing, and optional automation tasks. Designed to be run as a small Express server or serverless function and to be deployed with secrets stored in your host's secret manager.

---

# My Agent

This document describes what the MeGaOcToOoN Agent does, how it should be configured, and what to include when committing it to the repository.

## Purpose
The MeGaOcToOoN Agent performs the server-side actions required after a user installs the MeGaOcToOoN GitHub App. Its primary responsibilities are:
- Accept the GitHub App setup redirect and exchange the installation_id for a short-lived installation access token.
- Run onboarding automation (create repo config files, register webhooks, seed data).
- Provide a webhook endpoint to receive and process GitHub events (installation, push, pull_request, etc.).
- Provide a healthcheck and basic status page for monitoring.

## Responsibilities / capabilities
- GET /setup
  - Receives `installation_id` from GitHub after the user installs the app.
  - Uses the App JWT (created with APP_ID + PRIVATE_KEY) to request an installation token from GitHub.
  - Performs onboarding tasks using the installation token and shows a success page.
- POST /webhook
  - Receives events from GitHub.
  - Validates signature using a webhook secret.
  - Routes events to handlers for processing (e.g., create issue, label PR).
- Optional admin endpoints (protected by auth) to list active installations and revoke tokens.

## Run & configure
Environment variables (never commit real values):
- APP_ID — numeric GitHub App ID
- PRIVATE_KEY — PEM for the GitHub App (store in secrets, not repo)
- WEBHOOK_SECRET — secret to validate webhook payloads
- SETUP_ORIGIN — public origin for redirects (e.g. https://elmorab3.com)
- ADMIN_EMAIL — optional admin contact

Example local start:
1. Copy `server/.env.example` → `server/.env` and fill values (do NOT commit).
2. npm install
3. npm start

CI / deployment:
- Store secrets in GitHub Actions secrets or your host provider (Render, Fly, Vercel).
- Use the `.github/workflows/ci.yml` and `release.yml` to run tests and publish releases.
- Ensure PRIVATE_KEY is only available to runtime and CI via secrets.

## Commit & PR guidance (what to add to the repo)
When adding or updating the agent code, use a clear commit message and request a reviewer. Example:
- Commit message: chore(agent): add setup server and agent metadata
- PR title: feat(agent): add setup server and onboarding flow
- Request reviewer: @ELMOURABEA

If you want to indicate collaborative authorship for automation, you may add a co-author trailer in commits:
- Co-authored-by: GitHub Copilot <copilot@github.com>  (optional)

## Security considerations
- NEVER commit PRIVATE_KEY or other secrets to the repo.
- Validate webhooks using X-Hub-Signature-256 and the webhook secret.
- Restrict app permissions to the minimum required (principle of least privilege).
- Rotate private key periodically and publish a revocation/rotation plan.
- Enable branch protection and require PR reviews for main.

## Release & distribution
- Tag releases with semantic tags (we're preparing v10.0).
- Publish release notes (RELEASE_NOTES.md) and attach build artifacts if applicable.
- For Marketplace: provide clear permission rationale, privacy policy URL, support contact, screenshots, and an install flow.

## Review checklist for PRs touching the agent
- [ ] No private keys or secrets are included
- [ ] .env.example present and complete
- [ ] README / INSTALL.md updated with setup URL and domain
- [ ] Tests added or smoke checks for endpoints
- [ ] CI workflow references secrets via `${{ secrets.* }}` and does not print them
- [ ] Webhook signature validation implemented
- [ ] Code scanning (CodeQL) passes or is configured

---

If you'd like, I can:
- Convert this agent to TypeScript and add types & tsconfig.
- Add unit tests for the token exchange and webhook validation.
- Create the initial PR and request you (ELMOURABEA) as the reviewer.

Suggested commit to include this file:
- git add AGENT.md
- git commit -m "docs(agent): add agent metadata and responsibilities"
- git push origin main

Describe any changes you want in this file and I will update it for you.
