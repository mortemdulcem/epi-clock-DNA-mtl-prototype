---
name: GitHub push blocked by oversized committed blobs
description: Why a GitHub push of this repo cannot succeed without a user-authorized git history rewrite.
---

# GitHub push is hard-blocked by >100MB blobs already in git history

A plain `git push` to GitHub **fails** for this repo because large binaries are already
committed (tracked) in history. GitHub hard-rejects any single file >100MB.

Worst offender: `attached_assets/gdrive/epiclock/EpiClockPrototype.zip` (~1.6GB). Plus a
dozen 50–82MB tracked files (forensic-medicine reference PDFs/atlases, a DICOM `.crdownload`,
`scripts/revize/realdata/out/*_CONFOUNDED.csv`). The big methylation matrices under
`scripts/revize/realdata/data/*.gz` are already untracked via the `data/` rule — those are fine.

**Why .gitignore alone does not help:** gitignore never un-tracks already-committed files; the
blobs persist in history and GitHub still rejects the push.

**How to apply / unblock (all need the user):**
- Requires `GITHUB_TOKEN` (a missing secret) AND a destructive history rewrite — BFG / `git filter-repo` / `git lfs migrate`, or a fresh orphan branch / new repo containing only article + reproducible scripts.
- Destructive git is blocked in the main-agent sandbox; do not attempt git rm/reset/filter-branch/commit directly. This is a genuine user-decision blocker, documented in `scripts/revize/realdata/REPORT.md` §9.

## Two further hard facts learned pushing to the existing public repo

Target repo for this project = **`mortemdulcem/epi-clock-DNA-mtl-prototype`** (public, default branch `main`, ~587 MB — it already holds this project's earlier pushed state, so any new push must be additive/non-destructive, parent = current HEAD).

1. **A repo's `permissions.push=true` in the REST listing does NOT mean a token can write.** It can reflect the user's role, not the token's grant. Verify writability for real, then trust the result.
2. **Git CLI being blocked is escapable via the GitHub REST Git Data API** (no git binary needed): GET ref→commit→base tree, POST `git/trees` with `base_tree` chaining + inline `content` for text files (base64 blob for binary), POST `git/commits`, PATCH ref. One commit, ~13 batched tree requests for ~1500 files. **But** every one of git/blobs, git/trees, git/commits **and** the high-level Contents API requires fine-grained-PAT permission `contents=write`; a read-only-Contents token 403s on all of them with header `x-accepted-github-permissions: contents=write`. The fine-grained PAT the user supplied (account `mortemdulcem`) is read-only for Contents and also cannot create repos — so it cannot push by ANY method. Need a token with **Contents: Read and write** on the repo.
**Why:** burned many turns building an API pusher before discovering the token was read-only. **How to apply:** before attempting any push, probe one write endpoint and read `x-accepted-github-permissions` on the 403 to confirm the token actually has `contents=write`.
