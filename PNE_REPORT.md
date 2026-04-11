# **Protection Needs Elicitation (PNE)**

**Project:** SecureApp-Sprint-Flask-Blog-App\
**Repository:**
<https://github.com/EshaKhan-ek/SecureApp-Sprint-Flask-Blog-App>\
**Course:** CYC386 --- Secure Software Design and Development\
**Sprint:** Midterm Lab Exam --- 48-Hour DevSecOps Security Sprint\
**Institution:** COMSATS University Islamabad\
**Instructor:** Engr. Muhammad Ahmad Nawaz\
**Semester:** Spring 2026\
**CLO Alignment:** CLO-5 (Lab), CLO-6 (Lab)\
**CDF Reference:** Unit 2 --- Protection Needs Elicitation

## Table of Contents

1.  [Executive
    > Summary](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#1-executive-summary)

2.  [Application
    > Overview](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#2-application-overview)

3.  [Stakeholder
    > Analysis](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#3-stakeholder-analysis)

4.  [Asset
    > Identification](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#4-asset-identification)

5.  [Threat Actor
    > Profiling](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#5-threat-actor-profiling)

6.  [Elicited Protection
    > Needs](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#6-elicited-protection-needs)

7.  [Security Requirements
    > Specification](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#7-security-requirements-specification)

8.  [Vulnerability Scope: IDOR, CSRF,
    > Clickjacking](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#8-vulnerability-scope-idor-csrf-clickjacking)

9.  [Protection Needs Priority
    > Matrix](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#9-protection-needs-priority-matrix)

10. [Compliance & Regulatory
    > Considerations](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#10-compliance--regulatory-considerations)

11. [Summary & Sprint
    > Mapping](https://claude.ai/chat/8aaeccfb-ef04-4e3f-8410-fe9e020878c1#11-summary--sprint-mapping)

## 1. Executive Summary

This Protection Needs Elicitation (PNE) report is produced as the first
deliverable of the 48-Hour DevSecOps Security Sprint for CYC386 ---
Secure Software Design and Development. The application under analysis
is a **Flask-based Blog Web Application**, an open-source platform that
allows users to register, log in, create and manage blog posts, and
interact with content through a browser-based interface.

The purpose of this report is to systematically identify all digital and
informational assets associated with the application, enumerate
realistic threat actors and their motivations, and elicit concrete,
measurable protection needs grounded in real-world security
requirements. This document serves as the foundation for subsequent
sprint phases including Threat Modeling (STRIDE), Risk Assessment (CVSS
v3.1), and Secure Implementation.

Three critical vulnerabilities mandated for mitigation by the sprint
specification are scoped explicitly in this report: **Insecure Direct
Object Reference (IDOR)**, **Cross-Site Request Forgery (CSRF)**, and
**Clickjacking**. All protection needs are mapped to OWASP Top 10
(2021), relevant CWEs, and the course CDF units.

## 2. Application Overview

### 2.1 Technology Stack

  -----------------------------------------------------------------------
  Component          Technology
  ------------------ ----------------------------------------------------
  Backend            Python 3.x, Flask (micro-framework)

  Database           SQLite (development) / PostgreSQL (production)

  ORM                SQLAlchemy / Flask-SQLAlchemy

  Authentication     Flask-Login, Werkzeug password hashing

  Frontend           HTML5, CSS3, Bootstrap, Jinja2 templates

  Forms              Flask-WTF / WTForms

  Session Mgmt       Flask built-in sessions (server-side cookies)

  Deployment         Gunicorn / Nginx (production target)
  -----------------------------------------------------------------------

### 2.2 Core Functional Features

-   **User Registration & Authentication** --- Users can register with
    > username/email/password, log in, and maintain authenticated
    > sessions.

-   **Blog Post Management (CRUD)** --- Authenticated users can create,
    > read, update, and delete their own blog posts.

-   **User Profile Management** --- Users can view and update their
    > profile information including display name and profile picture.

-   **Public Post Listing** --- All published blog posts are publicly
    > accessible without authentication.

-   **Comment System** --- Registered users may leave comments on blog
    > posts.

-   **Admin Panel (if present)** --- Administrative users can manage all
    > users and posts.

### 2.3 Deployment Context

The application is being prepared for a **production release** following
a simulated client handover. It is assumed to be deployed on a
public-facing server accessible over the internet, making it subject to
a wide range of web application attack vectors.

### 2.4 Trust Boundary Overview

![](./image1.png){width="5.322916666666667in" height="5.09375in"}

## 3. Stakeholder Analysis

Identifying stakeholders is the first step in PNE --- protection needs
must reflect the concerns of all parties who have an interest in the
system\'s security.

### 3.1 Internal Stakeholders

  ------------------------------------------------------------------------
  Stakeholder     Role              Security Concern
  --------------- ----------------- --------------------------------------
  Registered      End users of the  Privacy of posts, account takeover,
  Users           platform          data integrity

  Blog Authors    Content creators  Unauthorized modification or deletion
                                    of their content

  System          Platform manager  Unauthorized admin access, system
  Administrator                     integrity, availability

  Development     Builders of the   Secure code delivery, no introduced
  Team            application       vulnerabilities

  DevSecOps Team  Security sprint   Threat identification, vulnerability
                  team              mitigation, compliance
  ------------------------------------------------------------------------

### 3.2 External Stakeholders

  -----------------------------------------------------------------------
  Stakeholder    Role              Security Concern
  -------------- ----------------- --------------------------------------
  Client /       Commissioning the Secure, deployable product; no
  Product Owner  sprint            reputational damage

  End Consumers  Readers of blog   Not served malicious content, no
                 content           tracking/injection

  Regulatory     Compliance        GDPR compliance for user data, data
  Bodies         oversight         breach obligations
  -----------------------------------------------------------------------

## 4. Asset Identification

Asset identification is the cornerstone of PNE. Each asset is classified
by type, sensitivity, and its relevance to the three mandatory
vulnerabilities.

### 4.1 Primary Data Assets

  ----------------------------------------------------------------------------------
  Asset   Asset Name        Type   Sensitivity   Description
  ID                                             
  ------- ----------------- ------ ------------- -----------------------------------
  DA-01   User Credentials  Data   Critical      Usernames, email addresses, hashed
                                                 passwords stored in DB

  DA-02   User Session      Data   Critical      Flask session cookies used to
          Tokens                                 authenticate requests

  DA-03   Blog Post Content Data   High          All user-authored posts including
                                                 drafts and published content

  DA-04   User Profile Data Data   High          Display names, bio, profile
                                                 pictures, email addresses

  DA-05   Comment Data      Data   Medium        User-submitted comments on posts

  DA-06   Application       Data   Critical      SECRET_KEY, DB URI, mail
          Configuration                          credentials stored in config files

  DA-07   Database File     Data   Critical      SQLite .db file containing all
                                                 persistent application data

  DA-08   Uploaded Media    Data   Medium        Profile images and any
          Files                                  user-uploaded file attachments

  DA-09   Admin Account     Data   Critical      Administrative user credentials
          Credentials                            with elevated privileges

  DA-10   Application Logs  Data   Medium        Server-side logs capturing user
                                                 activity and errors
  ----------------------------------------------------------------------------------

### 4.2 System & Infrastructure Assets

  ---------------------------------------------------------------------------------------
  Asset   Asset Name         Type             Sensitivity   Description
  ID                                                        
  ------- ------------------ ---------------- ------------- -----------------------------
  SA-01   Flask Application  System           High          The running web server
          Process                                           process handling all HTTP
                                                            requests

  SA-02   Web Server         Infrastructure   High          Reverse proxy and WSGI server
          (Nginx/Gunicorn)                                  in production

  SA-03   Source Code        System           High          GitHub repo containing all
          Repository                                        application logic

  SA-04   CI/CD Pipeline     Infrastructure   High          GitHub Actions workflows for
                                                            automated build/test/deploy

  SA-05   File System Paths  System           Medium        Upload directories, static
                                                            files, template directories

  SA-06   Database           System           Critical      SQLAlchemy connection to
          Connection                                        SQLite/PostgreSQL
  ---------------------------------------------------------------------------------------

### 4.3 Asset Criticality Summary

CRITICAL: DA-01, DA-02, DA-06, DA-07, DA-09, SA-06

HIGH: DA-03, DA-04, SA-01, SA-02, SA-03, SA-04

MEDIUM: DA-05, DA-08, DA-10, SA-05

## 5. Threat Actor Profiling

Understanding who might attack the system and why is essential to
formulating meaningful protection needs.

### 5.1 Threat Actor Profiles

  ---------------------------------------------------------------------------------
  Actor   Actor Type      Motivation          Capability    Likely Attack Vectors
  ID                                                        
  ------- --------------- ------------------- ------------- -----------------------
  TA-01   Opportunistic   Exploit publicly    Low--Medium   Automated scanners,
          Attacker        known                             OWASP Top 10 attacks
                          vulnerabilities                   

  TA-02   Malicious       Accessing or        Medium        IDOR on post/user IDs,
          Registered User modifying others\'                session manipulation
                          data                              

  TA-03   Cross-Site      Abuse authenticated Medium        CSRF via forged forms
          Attacker        user actions                      hosted on attacker site

  TA-04   Phishing / UI   Credential theft    Medium        Clickjacking via iframe
          Attacker        via fake UI                       embedding of login page

  TA-05   Credential      Account takeover    Medium        Brute force, password
          Attacker                                          spraying, credential
                                                            stuffing

  TA-06   Insider Threat  Data exfiltration   High          Unauthorized DB access,
                          or sabotage                       code injection

  TA-07   Automated Bot / Data harvesting,    Low           Mass registration,
          Scraper         spam                              content scraping,
                                                            comment spam

  TA-08   Advanced        Long-term system    High          SQLi, RCE, supply chain
          Persistent      compromise                        attacks
          Threat                                            
  ---------------------------------------------------------------------------------

### 5.2 Most Relevant Threat Actors for Sprint Scope

Given the three mandated vulnerabilities (IDOR, CSRF, Clickjacking), the
most directly relevant threat actors are:

-   **TA-02** (Malicious Registered User) → primary actor for IDOR
    > exploitation

-   **TA-03** (Cross-Site Attacker) → primary actor for CSRF
    > exploitation

-   **TA-04** (UI Attacker) → primary actor for Clickjacking
    > exploitation

## 6. Elicited Protection Needs

Protection needs are elicited from the intersection of assets and threat
actors. Each protection need is stated as a security requirement that
the system must satisfy.

### 6.1 Authentication & Session Management Protection Needs

  ------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                          Asset(s)   Threat
                                                                        Actor
  ------- -------------------------------------------------- ---------- --------
  PN-01   The system SHALL store all user passwords using a  DA-01      TA-05,
          strong adaptive hashing algorithm (e.g.,                      TA-08
          bcrypt/Argon2).                                               

  PN-02   The system SHALL enforce a minimum password        DA-01      TA-05
          complexity policy (length \>= 8, mixed                        
          characters).                                                  

  PN-03   The system SHALL invalidate session tokens upon    DA-02      TA-02,
          logout and SHALL NOT reuse tokens across sessions.            TA-03

  PN-04   The system SHALL set session cookies with          DA-02      TA-03,
          HttpOnly, Secure, and SameSite=Lax or Strict                  TA-04
          attributes.                                                   

  PN-05   The system SHALL implement rate limiting on login  DA-01,     TA-05
          endpoints to prevent brute force attacks.          DA-09      

  PN-06   The system SHALL use a cryptographically random,   DA-06      TA-08
          sufficiently long SECRET_KEY never hardcoded in               
          source.                                                       
  ------------------------------------------------------------------------------

### 6.2 Authorization & Access Control Protection Needs (IDOR-Focused)

  --------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                            Asset(s)   Threat
                                                                          Actor
  ------- ---------------------------------------------------- ---------- --------
  PN-07   The system SHALL verify that the currently           DA-03,     TA-02
          authenticated user is the **owner** of a resource    DA-04      
          before permitting any read/edit/delete operation on             
          it, regardless of the resource ID supplied in the               
          URL or request body.                                            

  PN-08   The system SHALL NOT expose predictable sequential   DA-03,     TA-02
          integer IDs in URLs for sensitive user-specific      DA-04      
          resources.                                                      

  PN-09   The system SHALL return HTTP 403 Forbidden when an   DA-03      TA-02
          authenticated user attempts to access a resource                
          they do not own, to avoid information leakage                   
          through response differences.                                   

  PN-10   Administrative routes SHALL be protected by a        DA-09,     TA-02,
          role-based access control check that cannot be       SA-01      TA-06
          bypassed by URL manipulation.                                   

  PN-11   The system SHALL log all unauthorized access         DA-10      TA-02,
          attempts to sensitive resources for audit purposes.             TA-06
  --------------------------------------------------------------------------------

### 6.3 Cross-Site Request Forgery (CSRF) Protection Needs

  --------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                            Asset(s)   Threat
                                                                          Actor
  ------- ---------------------------------------------------- ---------- --------
  PN-12   All HTML forms that perform state-changing           DA-03,     TA-03
          operations (POST/PUT/DELETE) SHALL include a unique, DA-04      
          per-session, cryptographically random anti-CSRF                 
          token validated server-side before processing.                  

  PN-13   The system SHALL reject any state-changing request   DA-03,     TA-03
          that does not include a valid CSRF token or that     DA-04      
          contains a mismatched token.                                    

  PN-14   Session cookies SHALL be issued with the             DA-02      TA-03
          SameSite=Lax attribute at minimum, and                          
          SameSite=Strict for high-privilege actions.                     

  PN-15   AJAX/API endpoints performing state-changing         SA-01      TA-03
          operations SHALL validate CSRF tokens from the                  
          X-CSRFToken request header.                                     
  --------------------------------------------------------------------------------

### 6.4 Clickjacking Protection Needs

  --------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                            Asset(s)   Threat
                                                                          Actor
  ------- ---------------------------------------------------- ---------- --------
  PN-16   All HTTP responses for application pages SHALL       DA-01,     TA-04
          include the X-Frame-Options: DENY or                 DA-02      
          X-Frame-Options: SAMEORIGIN header to prevent                   
          framing by external origins.                                    

  PN-17   The application SHALL emit a Content-Security-Policy DA-01,     TA-04
          header including the frame-ancestors \'none\'        DA-02      
          directive to prevent embedding in iframes on any                
          origin.                                                         

  PN-18   Authentication pages (login, registration, password  DA-01      TA-04
          reset) SHALL be specifically protected against                  
          Clickjacking with the most restrictive frame policy             
          (frame-ancestors \'none\').                                     
  --------------------------------------------------------------------------------

### 6.5 Input Validation & Injection Protection Needs

  ------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                          Asset(s)   Threat
                                                                        Actor
  ------- -------------------------------------------------- ---------- --------
  PN-19   All user-supplied input rendered in HTML templates DA-03,     TA-01,
          SHALL be escaped by the templating engine (Jinja2  DA-05      TA-03
          auto-escaping) to prevent Cross-Site Scripting                
          (XSS).                                                        

  PN-20   All database queries SHALL use parameterized       DA-07      TA-01,
          queries or ORM abstractions and SHALL NOT use                 TA-08
          string concatenation with user-controlled input.              

  PN-21   File upload functionality SHALL validate file type DA-08,     TA-01
          (MIME type + extension whitelist), enforce a       SA-05      
          maximum file size, and store uploads outside the              
          web root.                                                     
  ------------------------------------------------------------------------------

### 6.6 Security Headers & Transport Protection Needs

  ------------------------------------------------------------------------------
  PN-ID   Protection Need Statement                          Asset(s)   Threat
                                                                        Actor
  ------- -------------------------------------------------- ---------- --------
  PN-22   All production traffic SHALL be served over HTTPS  DA-01,     TA-01
          (TLS 1.2+) and HTTP requests SHALL be redirected   DA-02      
          to HTTPS.                                                     

  PN-23   The application SHALL emit the                     DA-02      TA-01
          Strict-Transport-Security (HSTS) header with a                
          minimum max-age of 31536000.                                  

  PN-24   The application SHALL emit the                     SA-01      TA-01
          X-Content-Type-Options: nosniff header on all                 
          responses.                                                    

  PN-25   The application SHALL NOT expose the Server or     SA-01      TA-01,
          X-Powered-By headers that disclose technology                 TA-08
          stack details.                                                
  ------------------------------------------------------------------------------

## 7. Security Requirements Specification

This section formalizes the protection needs into traceable, testable
security requirements categorized by OWASP Top 10 (2021) mapping.

### 7.1 Functional Security Requirements

  ----------------------------------------------------------------------------------------
  Req ID  Requirement                            OWASP 2021         CWE         Priority
  ------- -------------------------------------- ------------------ ----------- ----------
  SR-01   Implement object-level authorization   A01 Broken Access  CWE-284     Critical
          checks on all /post/\<id\>/edit,       Control                        
          /post/\<id\>/delete, and /user/\<id\>                                 
          routes.                                                               

  SR-02   Integrate Flask-WTF CSRF protection    A01 Broken Access  CWE-352     Critical
          globally; validate CSRF tokens on all  Control                        
          state-changing form submissions.                                      

  SR-03   Apply X-Frame-Options: DENY and        A05 Security       CWE-1021    Critical
          Content-Security-Policy:               Misconfiguration               
          frame-ancestors \'none\' via Flask                                    
          response headers.                                                     

  SR-04   Hash all passwords using bcrypt via    A07 ID & Auth      CWE-916     Critical
          werkzeug.security with a work factor   Failures                       
          \>= 12.                                                               

  SR-05   Configure Flask session cookies:       A07 ID & Auth      CWE-614     High
          SESSION_COOKIE_HTTPONLY=True,          Failures                       
          SESSION_COOKIE_SECURE=True,                                           
          SESSION_COOKIE_SAMESITE=\'Lax\'.                                      

  SR-06   Enable Jinja2 auto-escaping for all    safe\` filter on   A03         CWE-79
          HTML templates; avoid use of \`        untrusted data.    Injection   

  SR-07   Use SQLAlchemy ORM for all database    A03 Injection      CWE-89      High
          interactions; prohibit raw SQL with                                   
          string formatting.                                                    

  SR-08   Implement rate limiting on /login      A07 ID & Auth      CWE-307     Medium
          endpoint using Flask-Limiter (e.g., 10 Failures                       
          requests/minute per IP).                                              

  SR-09   Load SECRET_KEY and sensitive config   A02 Cryptographic  CWE-798     Critical
          from environment variables; never      Failures                       
          hardcode in source.                                                   

  SR-10   Validate file upload type and size;    A04 Insecure       CWE-434     Medium
          store uploads outside web-accessible   Design                         
          directories.                                                          
  ----------------------------------------------------------------------------------------

### 7.2 Non-Functional Security Requirements

  ------------------------------------------------------------------------------
  Req ID   Requirement                                           Category
  -------- ----------------------------------------------------- ---------------
  NFR-01   All security-critical changes SHALL be peer-reviewed  Process /
           via GitHub Pull Requests before merging to main.      DevSecOps

  NFR-02   The CI/CD pipeline SHALL run SAST (CodeQL or Bandit)  Automation
           on every push and block merges if critical findings   
           are detected.                                         

  NFR-03   DAST (OWASP ZAP) SHALL be executed against the        Testing
           staging deployment prior to production release.       

  NFR-04   All security fixes SHALL be documented with           Documentation
           before/after code evidence in                         
           SECURITY_IMPLEMENTATION.md.                           

  NFR-05   The application SHOULD achieve a score of B or above  Measurable
           on Mozilla Observatory security header scan           Target
           post-hardening.                                       
  ------------------------------------------------------------------------------

## 8. Vulnerability Scope: IDOR, CSRF, Clickjacking

This section provides a detailed pre-fix analysis of each mandated
vulnerability as it applies to the Flask Blog App, serving as the
baseline for the Secure Implementation phase.

### 8.1 Insecure Direct Object Reference (IDOR)

**CWE:** CWE-284 (Improper Access Control), CWE-639 (Authorization
Bypass Through User-Controlled Key)\
**OWASP 2021:** A01 --- Broken Access Control

#### Affected Surfaces in Flask Blog App {#affected-surfaces-in-flask-blog-app .unnumbered}

  ------------------------------------------------------------------------------------
  Endpoint                       Method   IDOR Risk Description
  ------------------------------ -------- --------------------------------------------
  /post/\<int:post_id\>/edit     GET,     Any authenticated user can edit any post by
                                 POST     substituting the post_id integer in the URL

  /post/\<int:post_id\>/delete   POST     Any authenticated user can delete any post
                                          by substituting the post_id

  /account (with user_id param)  GET,     User profile data accessible/modifiable by
                                 POST     manipulating user identifiers

  /user/\<int:user_id\>          GET      Direct enumeration of user profiles by
                                          incrementing user_id
  ------------------------------------------------------------------------------------

#### Root Cause {#root-cause .unnumbered}

Flask route handlers that accept resource IDs as URL parameters do not
verify that the authenticated user (current_user) is the owner of the
resource before granting access. The application trusts that
authenticated = authorized.

#### **Vulnerable Code Pattern (Example)** {#vulnerable-code-pattern-example .unnumbered}

\@app.route(\"/post/\<int:post_id\>/delete\", methods=\[\"POST\"\])

\@login_required

def delete_post(post_id):

post = Post.query.get_or_404(post_id)

\# MISSING: check that current_user.id == post.author_id

db.session.delete(post)

db.session.commit()

return redirect(url_for(\"home\"))

#### **Required Fix Pattern** {#required-fix-pattern .unnumbered}

\@app.route(\"/post/\<int:post_id\>/delete\", methods=\[\"POST\"\])

\@login_required

def delete_post(post_id):

post = Post.query.get_or_404(post_id)

if post.author != current_user:

abort(403) \# Object-level authorization check

db.session.delete(post)

db.session.commit()

return redirect(url_for(\"home\"))

#### **Relevant Protection Needs** {#relevant-protection-needs .unnumbered}

PN-07, PN-08, PN-09, PN-10, PN-11

### 8.2 Cross-Site Request Forgery (CSRF)

**CWE:** CWE-352 (Cross-Site Request Forgery)\
**OWASP 2021:** A01 --- Broken Access Control

#### **Affected Surfaces in Flask Blog App** {#affected-surfaces-in-flask-blog-app-1 .unnumbered}

  ------------------------------------------------------------------------------
  Endpoint              Method   CSRF Risk Description
  --------------------- -------- -----------------------------------------------
  /post/new (create     POST     Forged request can create posts as the
  post)                          authenticated victim

  /post/\<id\>/edit     POST     Forged request can silently modify a victim\'s
                                 post content

  /post/\<id\>/delete   POST     Forged request can delete any post owned by the
                                 victim

  /account (profile     POST     Forged request can change victim\'s display
  update)                        name, email, or profile picture

  /login, /register     POST     Forged login can lead to login CSRF --- victim
                                 is logged in as the attacker
  ------------------------------------------------------------------------------

#### **Root Cause** {#root-cause-1 .unnumbered}

Without CSRF tokens, any third-party website can host a form or
JavaScript snippet that triggers a POST request to the Flask app.
Because the browser automatically includes the victim\'s session cookie,
the server processes the request as if the victim submitted it
voluntarily.

#### **Attack Demonstration** {#attack-demonstration .unnumbered}

\<!\-- Attacker\'s malicious page \--\>

\<form action=\"https://target-blog.com/post/42/delete\"
method=\"POST\"\>

\<input type=\"submit\" value=\"Click me for a free gift!\"\>

\</form\>

\<script\>document.forms\[0\].submit();\</script\>

#### **Required Fix Pattern** {#required-fix-pattern-1 .unnumbered}

\# app.py --- enable Flask-WTF CSRF globally

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

\# In every form template, include:

\# {{ form.hidden_tag() }} or \<input type=\"hidden\"
name=\"csrf_token\" value=\"{{ csrf_token() }}\"\>

#### **Relevant Protection Needs** {#relevant-protection-needs-1 .unnumbered}

PN-12, PN-13, PN-14, PN-15

### 8.3 Clickjacking

**CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers or
Frames)\
**OWASP 2021:** A05 --- Security Misconfiguration

#### **Affected Surfaces in Flask Blog App** {#affected-surfaces-in-flask-blog-app-2 .unnumbered}

  -----------------------------------------------------------------------
  Page          Clickjacking Risk Description
  ------------- ---------------------------------------------------------
  /login        Attacker embeds login page in an invisible iframe; user
                unknowingly submits credentials

  /register     User registers an account while believing they are
                interacting with a different site

  /account      User unknowingly changes account settings (email,
  (settings)    password) by clicking overlaid elements

  All           Application can be embedded in malicious iframes to
  application   deceive users or harvest interactions
  pages         
  -----------------------------------------------------------------------

#### **Root Cause** {#root-cause-2 .unnumbered}

The Flask application does not set the X-Frame-Options HTTP response
header or the Content-Security-Policy header with frame-ancestors. This
allows any external website to embed the application within an
\<iframe\>, enabling UI redress / Clickjacking attacks.

#### **Attack Demonstration** {#attack-demonstration-1 .unnumbered}

\<!\-- Attacker\'s malicious page \--\>

\<style\>

iframe {

opacity: 0.0;

position: absolute;

top: 0; left: 0;

width: 100%; height: 100%;

}

\</style\>

\<div\>Click here to claim your prize!\</div\>

\<iframe src=\"https://target-blog.com/login\"\>\</iframe\>

#### **Required Fix Pattern** {#required-fix-pattern-2 .unnumbered}

\# app.py --- add security headers to all responses

\@app.after_request

def set_security_headers(response):

response.headers\[\"X-Frame-Options\"\] = \"DENY\"

response.headers\[\"Content-Security-Policy\"\] = \"frame-ancestors
\'none\'\"

return response

#### **Relevant Protection Needs** {#relevant-protection-needs-2 .unnumbered}

PN-16, PN-17, PN-18

## 9. Protection Needs Priority Matrix

This matrix maps all elicited protection needs to their priority for the
sprint, ensuring the team focuses on mandated critical fixes first.

  -----------------------------------------------------------------------
  Priority    Protection Need IDs  Vulnerability Category    Sprint Phase
  ----------- -------------------- ------------------------- ------------
  P1 ---      PN-07, PN-08, PN-09, IDOR / Broken Access      Phase 3
  Critical    PN-10                Control                   

  P1 ---      PN-12, PN-13, PN-14, CSRF                      Phase 3
  Critical    PN-15                                          

  P1 ---      PN-16, PN-17, PN-18  Clickjacking              Phase 3
  Critical                                                   

  P1 ---      PN-01, PN-06         Authentication / Key      Phase 3
  Critical                         Management                

  P2 --- High PN-03, PN-04, PN-05  Session Management        Phase 3

  P2 --- High PN-19, PN-20         Injection (XSS, SQLi)     Phase 3

  P2 --- High PN-22, PN-23, PN-24, Security Headers /        Phase 3
              PN-25                Transport                 

  P3 ---      PN-02, PN-11, PN-21  Input Validation /        Phase 3--4
  Medium                           Logging                   
  -----------------------------------------------------------------------

## 10. Compliance & Regulatory Considerations

## 10.1 OWASP Top 10 (2021) Coverage

  -----------------------------------------------------------------------
  OWASP Category                        Addressed By
  ------------------------------------- ---------------------------------
  A01 --- Broken Access Control         SR-01 (IDOR), SR-02 (CSRF), PN-07
                                        through PN-15

  A02 --- Cryptographic Failures        SR-09 (Secret Key), PN-06

  A03 --- Injection                     SR-06 (XSS), SR-07 (SQLi), PN-19,
                                        PN-20

  A04 --- Insecure Design               SR-10, PN-21

  A05 --- Security Misconfiguration     SR-03 (Clickjacking), PN-16
                                        through PN-25

  A07 --- Identification &              SR-04, SR-05, SR-08, PN-01
  Authentication Failures               through PN-06
  -----------------------------------------------------------------------

### 10.2 Relevant Standards

  -----------------------------------------------------------------------
  Standard /     Relevance to This Application
  Framework      
  -------------- --------------------------------------------------------
  OWASP Top 10   Direct mapping of all three mandated vulnerabilities
  (2021)         

  NIST SP 800-53 AC-3 (Access Enforcement), SC-8 (Transmission
                 Confidentiality), SI-10 (Input Validation)

  ISO/IEC 27001  A.9 Access Control, A.14 System Acquisition /
                 Development / Maintenance

  GDPR (if EU    Article 32 --- Security of processing; requires
  users)         appropriate technical measures for user data

  OWASP ASVS     V1 Architecture, V3 Session Management, V4 Access
  (Level 1)      Control, V5 Input Validation
  -----------------------------------------------------------------------

## 11. Summary & Sprint Mapping

### 11.1 Summary of Elicited Protection Needs

A total of **25 distinct protection needs (PN-01 through PN-25)** have
been elicited through structured analysis of:

-   **16 identified assets** --- 10 data assets, 6 system/infrastructure
    > assets

-   **8 threat actor profiles** --- ranging from opportunistic attackers
    > to advanced persistent threats

-   **3 mandated critical vulnerability classes** --- IDOR, CSRF, and
    > Clickjacking

-   **10 functional** and **5 non-functional security requirements**

### 11.2 Sprint Phase Mapping

  -----------------------------------------------------------------------
  Sprint Phase              PNE Output Used
  ------------------------- ---------------------------------------------
  Phase 2: Threat Modeling  Threat actors (TA-01 to TA-08), assets (DA-01
  (STRIDE)                  to SA-06), trust boundaries

  Phase 2: Risk Assessment  Vulnerability descriptions in Section 8 as
  (CVSS v3.1)               baseline

  Phase 3: Secure           SR-01 through SR-09 and PN-07 through PN-18
  Implementation            

  Phase 4: Security Testing NFR-02 (SAST), NFR-03 (DAST), all functional
  (SAST/DAST)               requirements

  Phase 5: Documentation    This PNE report forms Section 2 of the Final
                            Report
  -----------------------------------------------------------------------

*This document was produced as part of the CYC386 --- Secure Software
Design and Development Midterm Lab Exam (Spring 2026), COMSATS
University Islamabad. It is aligned with CDF Unit 2: Protection Needs
Elicitation and serves as the foundation for all subsequent sprint
deliverables.*

**Document Version:** 1.0\
**Sprint Phase:** Phase 1 (Hours 0--4)\
**Status:** Final --- Approved for Sprint Continuation
