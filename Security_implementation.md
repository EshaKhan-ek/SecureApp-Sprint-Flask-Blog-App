# SECURITY_IMPLEMENTATION.md

## Secure Implementation of OWASP Top 10 Vulnerabilities

**Project:** SecureApp-Sprint-Flask-Blog-App
**Course:** CYC386 — Secure Software Design and Development
**Sprint:** 48-Hour DevSecOps Security Sprint

---

# 4. Secure Implementation

This section documents the identification and mitigation of three critical OWASP Top 10 vulnerabilities:

* Insecure Direct Object Reference (IDOR)
* Cross-Site Request Forgery (CSRF)
* Clickjacking

Each vulnerability includes:

* Description
* Vulnerable code
* Fixed code
* Testing & verification

---

# 4.1 Fix 1 — IDOR (Member 1)

## Vulnerability Description

Insecure Direct Object Reference (IDOR) occurs when an application allows users to access or modify objects (such as posts) by manipulating identifiers (IDs) without proper authorization checks.

In this Flask Blog application, any authenticated user could edit another user's post by changing the `post_id` in the URL.

---

## Exploitation Steps

1. User A creates a blog post
2. User B logs in
3. User B manually accesses:
   `/post/1/update`
4. User B successfully edits User A’s post

---

## Vulnerable Code

```python
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

    return render_template('create_post.html', form=form)
```

❌ No ownership check → unauthorized access allowed

---

## Fixed Code

```python
from flask import abort

@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # IDOR FIX
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

    return render_template('create_post.html', form=form)
```

---

## Verification

* **Before:** User B edits User A’s post
* **After:** HTTP 403 Forbidden

---

# 4.2 Fix 2 — CSRF (Member 2)

## Vulnerability Description

Cross-Site Request Forgery (CSRF) allows attackers to trick authenticated users into performing unwanted actions (e.g., deleting posts) without their consent.

---

## Vulnerable State

* No CSRF protection enabled
* Forms missing CSRF tokens
* No SameSite cookie

```python
# __init__.py
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
```

❌ No CSRF protection configured

---

## Fixed Code

```python
from flask_wtf.csrf import CSRFProtect

app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

csrf = CSRFProtect(app)
```

---

## Template Fix

```html
<form method="POST">
    {{ form.hidden_tag() }}
</form>
```

---

## Fix Summary

* Enabled Flask-WTF
* Added CSRF middleware
* Added CSRF token in forms
* Configured SameSite cookies

---

## Verification

* **Before:** No CSRF token in forms
* **After:** CSRF token visible in HTML

---

# 4.3 Fix 3 — Clickjacking (Member 2)

## Vulnerability Description

Clickjacking occurs when an attacker embeds the application inside an iframe to trick users into performing unintended actions.

---

## Vulnerable State

* No security headers present
* Application loads inside iframe

---

## Vulnerable Code

```python
# No clickjacking protection implemented
```

---

## Fixed Code

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    return response
```

---

## Fix Summary

* Added X-Frame-Options header
* Added Content-Security-Policy
* Prevented iframe embedding

---

## Verification

* **Before:** App loads inside iframe
* **After:** Browser blocks iframe

---

# 4.4 Summary of Fixes

| Vulnerability | Issue                        | Fix Applied                    |
| ------------- | ---------------------------- | ------------------------------ |
| IDOR          | Unauthorized access to posts | Ownership check + 403          |
| CSRF          | Forged requests              | CSRF tokens + SameSite cookies |
| Clickjacking  | UI redress attack            | Security headers               |

---

# 4.5 Conclusion

All three critical OWASP vulnerabilities were successfully identified, exploited, and mitigated. The application now enforces proper access control, request validation, and browser-level protections, making it significantly more secure and aligned with modern DevSecOps practices.

---

