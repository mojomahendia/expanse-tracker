# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate with
Spendly and maintain a persistent logged-in state across requests. This step wires up
the existing `POST /login` form, stores the authenticated user's id and name in the
Flask session, updates the navbar to reflect login state, and implements the `/logout`
route that clears the session. This is the gateway step — without it, no future feature
can know who the current user is.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`password_hash` column is populated)

## Routes
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, flash message, redirect to landing — logged-in

## Database changes
No database changes. The `users` table already has `id`, `name`, `email`, and
`password_hash`. No new columns or tables are needed.

## Templates
- **Modify:** `templates/login.html` — already renders `{{ error }}` and flashed messages; no structural changes needed
- **Modify:** `templates/base.html` — update navbar to show "Sign out" link when
  `session.user_id` is set, and "Sign in" / "Get started" when it is not

## Files to change
- `app.py` — update `GET /login` to handle GET + POST, implement POST handler;
  implement `GET /logout`; import `session` and `check_password_hash`

- `templates/base.html` — conditional nav links based on `session.get('user_id')`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys to set on login:
  - `session['user_id']` — integer (the user's `id` from the `users` table)
  - `session['user_name']` — string (the user's `name`, for display in the navbar)
- Validate login in this order; re-render `login.html` with `error=` on first failure:
  1. Email field is not blank
  2. Password field is not blank
  3. A user with that email exists in the database
  4. `check_password_hash(row['password_hash'], password)` returns `True`
  - Use a single generic error for steps 3 and 4: `"Invalid email or password"` — do not
    reveal whether the email exists
- On successful login: `redirect(url_for('profile'))`
- On logout: `session.clear()`, then `flash("You've been signed out.")`,
  then `redirect(url_for('landing'))`
- `base.html` navbar logic:
  - When `session.get('user_id')` is set: show user's name (or a greeting) and a
    "Sign out" link pointing to `url_for('logout')`
  - When not logged in: show "Sign in" and "Get started" links (current behaviour)

## Definition of done
- [ ] `GET /login` still renders the login form (no regression)
- [ ] Submitting the login form with a valid email and correct password sets
      `session['user_id']` and `session['user_name']` and redirects to `/profile`
- [ ] Submitting with an unrecognised email shows "Invalid email or password" and does
      not set any session keys
- [ ] Submitting with a correct email but wrong password shows "Invalid email or password"
- [ ] Submitting with a blank email or blank password shows an appropriate error
- [ ] Demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] After login, the navbar shows a "Sign out" link (not "Sign in" / "Get started")
- [ ] Visiting `/logout` while logged in clears the session and redirects to landing
- [ ] After logout, the navbar reverts to showing "Sign in" / "Get started"
- [ ] Visiting `/logout` while already logged out redirects to landing without error
- [ ] App starts without errors and all existing routes still work
