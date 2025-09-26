# 🎯 Goal

Let students reach tailored, explainable **global university
recommendations** fast---by **uploading a CV (PDF)** or **filling a
short form**. CV parsing is **client-side only**. We use **Auth0** for
login/signup and session management.

------------------------------------------------------------------------

# 👤 Primary persona

-   **Student applicant** for bachelor's/master's programs worldwide.

------------------------------------------------------------------------

# 🗺️ High-level journey (happy path)

1)  **Landing → Value proposition**\
2)  **Entry choice:** Upload CV **(client-side parse)** or Start with
    Form\
3)  **CV Upload (frontend-only parse)** → **Prefilled Form**\
4)  **Smart Profile Form** (only asks for missing bits)\
5)  **Auth (Auth0)**: continue as guest or log in to save progress\
6)  **Recommendations (first run)**\
7)  **Details & shortlist**\
8)  **Feedback & refine**

------------------------------------------------------------------------

# 🧩 Screen-by-screen detail (+ what the BE does)

### 1) Landing

-   **FE:** Hero, value prop, CTAs: "Get recommendations".
-   **BE:** None.

------------------------------------------------------------------------

### 2) Entry choice

-   **FE:** Two cards: **Upload CV (PDF)** or **Start with Form**.
-   **BE:** None.

------------------------------------------------------------------------

### 3) CV Upload (frontend-only) → Prefill

-   **FE:**
    -   Dropzone for **PDF**.
    -   Parse **entirely in browser** (e.g., `pdfjs-dist` for text
        extraction; optional OCR like `tesseract.js` only if needed;
        simple parsers/regex/NLP to pick GPA, degree, dates, tests,
        disciplines, languages, locations, email, etc.).
    -   Build a **structured JSON** (no confidence scores---per your
        note).\
    -   Show a **readable preview** of extracted fields with **Edit**
        toggles.
    -   When user confirms, pass the structured JSON to the next step
        (not the PDF file).
-   **BE:** None for parsing. (We **do not** upload the PDF.)

**Data produced on FE:**

``` json
{
  "identity": {"name": "…", "email": "…"},
  "education": [{"degree": "BSc CS", "institution": "…", "country": "…", "gpa": 3.6, "gpa_scale": 4.0, "start": "2019", "end": "2023"}],
  "tests": {"TOEFL": 110, "GRE_Q": 165, "GRE_V": 158, "GRE_AWA": 4.0},
  "disciplines": ["Computer Science", "AI"],
  "languages": ["English", "German"],
  "locations": ["DE", "NL"],
  "budget": {"min": 0, "max": 15000}
}
```

------------------------------------------------------------------------

### 4) Smart Profile Form (asks only what's missing)

-   **FE:**
    -   Pre-fills from CV JSON.
    -   Shows **only missing** fields (e.g., GPA scale if just GPA value
        was found).
    -   Sections: Academics, Discipline interests, Career goals,
        Location prefs, Budget, Constraints (language/visa/online).
    -   Always allow edits to prefilled fields.
-   **BE (hybrid stack):**
    -   If user is **logged in** → upsert `StudentProfile` +
        `Preference` in MySQL.
    -   If **guest** → keep in memory/localStorage (no server write
        yet).

------------------------------------------------------------------------

### 5) Auth (Auth0)

-   **FE:**
    -   "Save & continue" prompts login: **Auth0 Universal Login**
        (PKCE, SPA).
    -   Options: Google/Email/Passwordless (your choice in Auth0).
    -   On success, FE gets **ID token** (profile) + **access token**
        (API audience/scope).
    -   Silent re-auth (renew session) on refresh via Auth0 SDK.
-   **BE:**
    -   **No local password auth.** DRF uses **JWT verification** of
        Auth0 access tokens:
        -   Validate **issuer (Auth0 domain)** and **audience (your
            API)**.
        -   Map `sub` as the external user id; create a local `User` row
            on first API call (just a shell; all auth remains Auth0).
    -   Roles/claims from Auth0 can be used for admin gates if needed.

**Auth flows supported:** - Logged-in users can **save** profiles,
preferences, shortlists, recommendation history. - Guests can still
**generate recommendations** (no DB persistence until they log in).

------------------------------------------------------------------------

### 6) Recommendations (first run)

-   **FE:**
    -   Press "Get recommendations".
    -   Show loading + what's happening ("filtering global dataset based
        on your inputs...").
    -   Show ranked results with **rationales** and facet filters
        (country, tuition, degree level, discipline).
-   **BE (hybrid):**
    -   **DatasetService** reads curated global Parquet via
        DuckDB/Polars (OpenAlex + optional ranking signal).\
    -   Computes rankings (weights from `Preference` or FE defaults).\
    -   **If logged in:** `RecommendationService` **persists** top-N
        rows in MySQL with the OpenAlex IDs + filters/weights snapshot.\
    -   **If guest:** compute-on-the-fly, return results; no DB write.

Endpoints used: - `POST /api/recommendations/run` → returns list (and DB
ids if logged in) - `GET /api/universities` (for additional browsing) -
`GET /api/universities/{openalex_id}` (detail)

------------------------------------------------------------------------

### 7) University detail & shortlist

-   **FE:** Detail page, **Add to shortlist**, **Export** (CSV/PDF),
    **Share**.
-   **BE:**
    -   Detail = dataset read only.\
    -   Shortlist actions (if logged in) persist to MySQL (could be a
        simple `Shortlist` table or reuse `Recommendation` + a flag).

------------------------------------------------------------------------

### 8) Feedback & refine

-   **FE:** 1--5 rating or thumbs; "Refine results" toggles (budget
    up/down, expand region).
-   **BE:** `POST /api/recommendations/{id}/feedback` → save feedback;
    optionally nudge weights and re-run on next request.

------------------------------------------------------------------------

# 🔐 Privacy & trust (CV now stays client-side)

-   CV **never leaves the browser**; only structured fields may be sent
    to BE on save/recommend.\
-   Clear copy: "We parse your CV locally in your browser. You can edit
    everything before anything is sent."\
-   Data deletion: profile page action (MySQL rows); dataset is
    non-personal and stays file-based.

------------------------------------------------------------------------

# ⚙️ System interactions (updated)

-   **Auth:** Auth0 (OIDC with PKCE). FE holds tokens; BE validates
    Auth0 JWTs.\
-   **MySQL:** `User` (linked to Auth0 `sub`), `StudentProfile`,
    `Preference`, `Recommendation`, `Feedback`, (optional) `Shortlist`,
    `IngestionRun`.\
-   **Files (global dataset):** `/data/current/institutions.parquet`,
    `/data/current/search_index.parquet`.\
-   **APIs:**
    -   `GET /api/universities`, `GET /api/universities/{openalex_id}`\
    -   `POST /api/recommendations/run`, `GET /api/recommendations`,
        `POST /api/recommendations/{id}/feedback`\
    -   `GET/PATCH /api/students/me`, `PUT /api/students/preferences`\
    -   `GET /api/healthz`

------------------------------------------------------------------------

# 🧪 Edge cases

-   **Scanned CV (no selectable text):** FE optionally tries OCR
    (`tesseract.js`) with a warning; if poor, nudge to the form.\
-   **Weird GPA formats:** ask for GPA and scale explicitly (required).\
-   **No tests yet:** allow "I'll provide later"; algorithm downweights
    test-dependent features.\
-   **Guest closes tab:** warn on navigate-away if unsaved; offer
    **Auth0 login** to save.

------------------------------------------------------------------------

# 📏 Acceptance criteria (MVP)

-   CV parsing completes **entirely in FE**; **no PDF** uploaded to BE.\
-   After CV upload, prefilled form shows up with editable fields; only
    **missing fields** are required.\
-   Auth0 login/signup works; FE stores/refreshes tokens; BE validates
    Auth0 JWTs.\
-   First recommendations render in **\< 3s** for common queries.\
-   Logged-in users see their **history**, **shortlist**, and
    **feedback** on revisit.\
-   All personal data deletable; dataset responses include
    `dataset_version`.

------------------------------------------------------------------------

# 📊 Analytics to track

-   CV upload → prefill completion rate\
-   Time to first recommendation\
-   Guest → Auth0 conversion\
-   Edits per prefilled field (to improve FE parsers)\
-   Feedback submission rate and its effect on refinements

------------------------------------------------------------------------

# 🔧 Dev notes (how to wire quickly)

**Frontend** - CV parse: `pdfjs-dist` to extract text; simple
regex/entity rules; optional `tesseract.js` fallback. - Auth0:
`@auth0/auth0-react` or Auth0 SPA SDK with **PKCE**; set **audience**
for your DRF API; store tokens in memory (rotate via silent auth). -
Call BE with `Authorization: Bearer <access_token>` when logged in.

**Backend** - DRF auth: validate Auth0 **issuer**, **audience**,
**JWKS** for signature verification. - On first authenticated call,
ensure a local `User` row (linked by Auth0 `sub`). - Keep all university
data **file-backed**; transactional state in **MySQL** only.
