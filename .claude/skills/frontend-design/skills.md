---
name: spendly-ui
description: >
  Generates modern, production-ready UI components and pages for Spendly — a Flask-based personal expense tracker app.
  Use this skill whenever the user asks to design, create, build, redesign, improve, or add any page or component
  for the Spendly project. Trigger on phrases like "design the page", "create UI for", "build component for",
  "redesign", "improve the layout", "add a screen for", or any request involving Spendly's frontend.
  Also trigger when the user shares screenshots or asks for visual feedback on Spendly's existing UI.
  This skill should be used even for small component requests (buttons, modals, cards) — not just full pages.
---

# Spendly UI Skill

Generates clean, consistent, production-ready UI for the **Spendly** expense tracker — a Flask app using
Jinja2 templates, hand-written CSS, and minimal vanilla JavaScript.

---

## Project Context

| Property | Value |
|---|---|
| App name | **Spendly** |
| Backend | Python + Flask |
| Templating | Jinja2 (`.html` files in `/templates`) |
| Styling | Custom CSS (`/static/css/`) — no Bootstrap, no Tailwind |
| JavaScript | Minimal vanilla JS (`/static/js/`) |
| Database | SQLite (`spendly.db`) |
| Icons | Lucide Icons (preferred) or Heroicons |

---

## Step 0 — Always Read Before Writing

Before generating any UI, do the following:

1. **Read the existing CSS** — `cat static/css/style.css` (or equivalent path). Extract:
   - CSS custom properties (`--color-*`, `--spacing-*`, `--radius-*`, etc.)
   - Existing component class names (cards, buttons, nav, badges)
   - Font family and base sizing

2. **Scan existing templates** — `ls templates/` then read 1–2 relevant pages for layout patterns.

3. **If you can't access the files** (e.g. running in chat only), ask the user:
   > "Can you paste your `style.css` or share a screenshot of an existing page? I'll match it exactly."

Do NOT invent a new design system from scratch if the existing one is accessible.

---

## Design System

Use these rules consistently across all output. If the actual CSS differs, defer to the actual CSS.

### Colors (defaults — override with actual values from style.css)
```css
:root {
  --color-bg:          #F8F9FC;   /* page background */
  --color-surface:     #FFFFFF;   /* cards, panels */
  --color-border:      #E8ECF4;   /* dividers, card borders */
  --color-primary:     #6366F1;   /* indigo — primary actions */
  --color-primary-soft:#EEF2FF;   /* primary tints, badges */
  --color-success:     #10B981;   /* income, positive */
  --color-danger:      #EF4444;   /* expense, negative */
  --color-warning:     #F59E0B;   /* alerts, pending */
  --color-text:        #111827;   /* headings */
  --color-muted:       #6B7280;   /* labels, secondary text */
  --color-muted-bg:    #F3F4F6;   /* subtle backgrounds */

  --radius-sm:  6px;
  --radius-md: 12px;
  --radius-lg: 16px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.04);
}
```

### Spacing Grid
8px base unit. Use multiples: `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`.

### Typography
```css
/* Headings */
h1 { font-size: 1.75rem; font-weight: 700; color: var(--color-text); }
h2 { font-size: 1.25rem; font-weight: 600; }
h3 { font-size: 1rem;    font-weight: 600; }

/* Body */
body { font-size: 0.9375rem; line-height: 1.6; color: var(--color-text); }
.text-muted { font-size: 0.8125rem; color: var(--color-muted); }
```

---

## Component Patterns

### Card
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Title</h3>
    <span class="card-action">...</span>
  </div>
  <div class="card-body">...</div>
</div>
```
```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: 20px 24px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
```

### Stat Card (KPI)
```html
<div class="stat-card">
  <div class="stat-icon stat-icon--primary">
    <!-- Lucide SVG icon -->
  </div>
  <div class="stat-body">
    <p class="stat-label">Total Spent</p>
    <p class="stat-value">₹12,450</p>
    <p class="stat-delta stat-delta--down">↓ 8% vs last month</p>
  </div>
</div>
```

### Button
```html
<button class="btn btn-primary">Save</button>
<button class="btn btn-ghost">Cancel</button>
```
```css
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: var(--radius-sm);
  font-size: 0.875rem; font-weight: 500; cursor: pointer;
  border: none; transition: all .15s ease;
}
.btn-primary { background: var(--color-primary); color: #fff; }
.btn-primary:hover { filter: brightness(1.08); }
.btn-ghost { background: transparent; color: var(--color-muted); border: 1px solid var(--color-border); }
```

### Badge / Tag
```html
<span class="badge badge--food">Food</span>
<span class="badge badge--success">Paid</span>
```
```css
.badge {
  display: inline-block; padding: 2px 10px;
  border-radius: 999px; font-size: 0.75rem; font-weight: 500;
}
.badge--success  { background: #D1FAE5; color: #065F46; }
.badge--danger   { background: #FEE2E2; color: #991B1B; }
.badge--warning  { background: #FEF3C7; color: #92400E; }
.badge--neutral  { background: var(--color-muted-bg); color: var(--color-muted); }
```

### Table Row (Transactions)
```html
<tr class="tx-row">
  <td class="tx-icon"><!-- category icon --></td>
  <td class="tx-meta">
    <p class="tx-title">Zomato</p>
    <p class="tx-date text-muted">Apr 30, 2026</p>
  </td>
  <td class="tx-category"><span class="badge badge--neutral">Food</span></td>
  <td class="tx-amount tx-amount--expense">−₹340</td>
</tr>
```

### Form Input
```html
<div class="form-group">
  <label class="form-label" for="amount">Amount</label>
  <div class="input-wrapper">
    <span class="input-prefix">₹</span>
    <input type="number" id="amount" class="form-input" placeholder="0.00">
  </div>
  <p class="form-hint">Enter amount in INR</p>
</div>
```

### Empty State
```html
<div class="empty-state">
  <!-- Lucide icon, larger -->
  <p class="empty-title">No transactions yet</p>
  <p class="empty-desc text-muted">Add your first expense to get started.</p>
  <button class="btn btn-primary">+ Add Expense</button>
</div>
```

---

## Icons

Use **Lucide Icons** (preferred). Include via CDN or as inline SVG:

```html
<!-- CDN (add to base template head) -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<!-- Usage -->
<i data-lucide="wallet" class="icon"></i>
<script>lucide.createIcons();</script>
```

Common icon map for Spendly:
| Concept | Lucide icon name |
|---|---|
| Dashboard | `layout-dashboard` |
| Transactions | `receipt` |
| Add expense | `plus-circle` |
| Budget | `wallet` |
| Categories | `tag` |
| Analytics | `bar-chart-2` |
| Settings | `settings` |
| Income | `trending-up` |
| Expense | `trending-down` |
| Delete | `trash-2` |
| Edit | `pencil` |
| Filter | `sliders-horizontal` |
| Search | `search` |
| Calendar | `calendar` |
| Export | `download` |

---

## Layout Patterns

### Sidebar + Main
```html
<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-logo">Spendly</div>
    <nav class="sidebar-nav">
      <a href="/" class="nav-item nav-item--active">
        <i data-lucide="layout-dashboard"></i> Dashboard
      </a>
      <!-- more nav items -->
    </nav>
  </aside>
  <main class="main-content">
    <header class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <!-- actions -->
    </header>
    <div class="page-body">
      <!-- content -->
    </div>
  </main>
</div>
```

### Stats Row
```html
<div class="stats-grid">
  <!-- 3 or 4 stat-cards -->
</div>
```
```css
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
```

---

## Output Format

For every UI request, produce output in this order:

### 1. UI Structure (brief)
- 3–6 bullet points: what sections are on the page, key UX decisions made, and why.
- Keep it short — this is context, not documentation.

### 2. Jinja2 Template (`templates/<name>.html`)
- Extends `base.html` (or equivalent) if one exists.
- Uses real Jinja2 blocks: `{% extends %}`, `{% block %}`, `{{ url_for() }}`, `{{ expense.amount }}` etc.
- Passes real data from Flask routes (see data model below).
- Includes Lucide icon calls where relevant.

### 3. CSS (`static/css/<name>.css` or additions to `style.css`)
- Uses CSS custom properties from the design system.
- No inline styles except where unavoidable.
- Mobile-responsive (use `@media (max-width: 768px)`).
- Append to existing CSS rather than replacing it.

### 4. JavaScript (only if needed)
- Vanilla JS only.
- Keep it minimal — no jQuery, no frameworks.
- Annotate what it does.

---

## Spendly Data Model (inferred from project)

```python
# Expense
{
  id, title, amount, category, date, type  # 'income' | 'expense'
}

# Category
{ id, name, color, icon }

# Budget
{ id, category_id, limit_amount, month }
```

Use these field names in templates. If the actual schema differs, check `app.py` or `database/` first.

---

## Rules

### DO
- Always read existing CSS/templates before writing new ones (Step 0)
- Match the exact variable names and class conventions found in the codebase
- Use card-based layouts with soft shadows
- Prefer subtle colors — avoid saturated fills except on primary actions
- Keep currency in ₹ (INR) for all UI copy
- Use Lucide icons consistently (see icon map above)
- Respect 8px spacing grid
- Make forms feel guided — labels above fields, hints below

### DON'T
- Don't import Bootstrap, Tailwind, or any CSS framework (not in the project)
- Don't generate flat, boxy, or dated UI
- Don't produce unstructured code dumps — always structure output as shown above
- Don't hardcode colors — always use CSS variables
- Don't add animations or transitions that feel heavy
- Don't use generic placeholder copy like "Lorem ipsum"

### Consistency Rule
If the user hasn't shared their existing CSS or templates, ask before generating:
> "I want to match your existing design exactly. Can you share a screenshot of an existing page or paste your `style.css`?"

Only skip this if the user explicitly says "start fresh" or "new design."

---

## Reference Files

- `references/pages.md` — patterns for common Spendly pages (Dashboard, Transactions, Add Expense, Budget)

Read `references/pages.md` for page-level layout guidance when building a full page (not just a component).