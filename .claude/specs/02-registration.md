# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account.
This step wires up the existing `register.html` form (which already POSTs to `/register`)
to a real `POST /register` handler that validates input, checks for duplicate emails,
hashes the password, and inserts the new user into the `users` table. It also
introduces `app.secret_key`, which is required for Flask sessions used in later steps.
On success the user gets a success message and then redirected to `/login`; on failure the form is re-rendered
with a descriptive error message.

## Depends on
- Step 01 — Database setup (`users` table must exist, `get_db()` must work)

## Routes
- `POST /register` — process registration form — public

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at)
is already created by `init_db()` in Step 01.

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}`; no template
  changes needed unless the spec review reveals gaps
- **Modify:** `templates/base.html` — no changes needed

## Files to change
- `app.py` — add `app.secret_key`, import `request` and `redirect`, add `POST /register` handler,
  update the existing `GET /register` route to accept both GET and POST (or keep them separate)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already available
(used in `seed_db()`).

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Set `app.secret_key` to a hard-coded dev string (e.g. `"spendly-dev-secret"`) — a later
  step will move this to an env var
- Validate in this order; stop and re-render with the first error found:
  1. Name is not blank
  2. Email is not blank and contains `@`
  3. Password is at least 8 characters
  4. "Confirm password" matches "Password" exactly — show error
   "Passwords do not match" if they differ
  5. Email is not already registered (`SELECT` before `INSERT`, re-render with
     "An account with that email already exists")
- On success: `redirect(url_for('login'))`
- Do NOT auto-login after registration — session management comes in Step 3

## Definition of done
- [ ] Visiting `GET /register` still renders the form (no regression)
- [ ] Submitting the form with all valid fields inserts a new row into `users`
- [ ] Submitting with mismatched password and confirm-password fields
      shows "Passwords do not match" and does not insert a row
- [ ] The stored `password_hash` is a werkzeug hash, not plain text
- [ ] Submitting with a blank name shows an error on the form
- [ ] Submitting with an invalid email (no `@`) shows an error on the form
- [ ] Submitting with a password shorter than 8 characters shows an error on the form
- [ ] Submitting with an already-registered email shows "An account with that email already exists"
- [ ] Successful registration redirects to `/login`
- [ ] The demo user (`demo@spendly.com`) cannot be re-registered (duplicate email blocked)
- [ ] App starts without errors and all existing routes still work
