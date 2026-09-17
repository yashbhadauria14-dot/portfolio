# Product Requirement Document
## Yash Pratap Singh — Data Analyst Portfolio Website

---

## 1. Overview

**Purpose:** A single-page portfolio website presenting Yash Pratap Singh as a
Data Analyst / Business Analyst, showcasing real project work, technical
skills, and background to recruiters and hiring managers.

**Reference theme:** Dark navy/black background with purple-indigo accent
color, drawn from the provided "CodeCraft" template — same visual language
(dark hero, stat cards, progress-bar skills, project cards, footer with
social links), rebuilt around analytics content instead of web-dev content.

**Primary goal:** Give a recruiter, in under 60 seconds of scrolling, a clear
picture of: who Yash is, what tools he uses, and 3 concrete, quantified
projects proving it.

---

## 2. Target Audience

- Recruiters and hiring managers screening for Data Analyst / Business
  Analyst roles
- Referral contacts (e.g., a friend forwarding the portfolio link alongside
  a resume)

---

## 3. Design Direction (from reference theme)

| Element | Reference site | Adapted for this site |
|---|---|---|
| Background | Dark navy/black | Same — dark navy/near-black |
| Accent color | Purple/indigo (`#7C3AED`-family) | Same purple-indigo accent |
| Typography | Bold sans-serif headings, muted gray body text | Same |
| Hero layout | Left: intro + CTAs. Right: photo + floating code-snippet card | Left: intro + CTAs. Right: **provided photo** + floating "insight card" (styled like a small KPI/metric callout instead of a code snippet) |
| Stats row | 4 stat cards (years experience, projects, clients, satisfaction) | 4 stat cards using **real, truthful numbers** (see Section 5) |
| Skills section | Named skill + progress bar + percentage | Same pattern, applied to SQL/Python/Power BI/Excel/Tableau/Business Analysis |
| Projects section | 3 cards, image + title + description + "View Project" link | 3 cards for the 3 real resume projects, dashboard-style visual instead of a website screenshot |
| Testimonial | Fake client quote | **Excluded** — see Section 7 |
| Footer | Social links + contact | GitHub, LinkedIn, email — using existing resume contact info |

---

## 4. Site Structure (single page, scrollable, anchor nav)

1. **Nav bar** — Logo/name, links to Home / About / Skills / Projects / Contact, "Download Resume" button (top right)
2. **Hero** — Name, title, one-line pitch, 2 CTAs ("View Projects", "Download Resume"), photo
3. **About** — Short bio (from resume Summary) + stats row
4. **Skills** — Grouped skill bars (SQL, Python, Power BI, Excel, Tableau, Business Analysis)
5. **Projects** — 3 project cards (Hospital Healthcare Analytics, Retail Sales Analytics, Sales Performance & BI ETL Project)
6. **Certifications** — KPMG Lean Six Sigma Green Belt, PW/NSDC/PwC AI Bootcamp
7. **Contact/Footer** — Email, phone (optional to display publicly), GitHub, LinkedIn, location

---

## 5. Content Specification (pulled directly from resume — no invented facts)

### 5.1 Hero
- **Name:** Yash Pratap Singh
- **Title tag:** "Data Analyst" (matches resume title)
- **One-line pitch:** "I turn raw data into clear, actionable business insights using SQL, Python, and Power BI."
- **Photo:** provided headshot (circular crop, as in reference)
- **CTAs:** "View My Projects" (scrolls to Projects), "Download Resume" (links to resume PDF)

### 5.2 About + Stats Row
Bio drawn from resume Summary (condensed to 2-3 sentences for web readability).

**Stats — real numbers only, no inflation:**
| Stat | Value | Source |
|---|---|---|
| Certifications | 2 | KPMG Lean Six Sigma Green Belt + AI Analytics Bootcamp |
| Projects | 3 | Hospital, Retail, ETL |
| Core Tools | 5+ | SQL, Python, Power BI, Excel, Tableau |
| Education | MBA | Business Analytics & Marketing |

*(Deliberately not using "years of experience," "clients," or "satisfaction %" — none of these are honestly available yet; using them would repeat the fabrication pattern flagged earlier in this project.)*

### 5.3 Skills (progress bars)
Percentages are **self-assessed proficiency indicators**, labeled as such in a
small caption ("Self-assessed proficiency") so they don't imply a third-party
benchmark:
- SQL — 85%
- Power BI — 85%
- Excel — 90%
- Python — 75%
- Business Analysis — 75%
- Tableau — 65%

*(These are placeholders for Yash to adjust to his own honest self-rating before launch.)*

### 5.4 Projects (3 cards)
Each card: title, tool tags, 2-3 line summary, key metric highlight, "View Details" (expands or links to a case-study page/PDF).

**Card 1 — Hospital Healthcare Analytics**
Tags: MySQL, Power BI
Summary: Patient registration, demographic, and appointment analysis across 100 patients and 358 appointments — identifying a sharp acquisition slowdown, Orthopaedics as highest-demand specialty, and ~24% of billing records pending.
Key metric callout: ₹10.17 lakh paid revenue analyzed

**Card 2 — Retail Sales Analytics**
Tags: Excel
Summary: Interactive dashboard tracking ₹83.48 lakh revenue and 15.9 lakh units sold, identifying category/brand performance and seasonal trends.
Key metric callout: 1.05% YoY trend identified

**Card 3 — Sales Performance & BI End-to-End ETL Project**
Tags: Python, SQL, Power BI
Summary: Full pipeline — Python cleaning, SQL profitability analysis, Power BI dashboard — identifying ₹2.06 Cr sales and 25.29% margin.
Key metric callout: 482 clean records from raw dataset

### 5.5 Certifications
- KPMG Lean Six Sigma Green Belt (Jan 2024)
- PW | NSDC | PwC – Data Analytics with AI Course, 6-Month Bootcamp (Jul 2026)

### 5.6 Contact/Footer
- Email: bhadauriayash14@gmail.com
- Location: Lucknow, India
- GitHub, LinkedIn (icons linking out)
- Copyright line

---

## 6. Technical Requirements

- **Format:** Single-page responsive site (HTML/CSS/JS or React — recommend a single self-contained HTML file for easy hosting/sharing, per typical portfolio needs)
- **Responsive:** Must work on mobile (stats/skills/project cards stack vertically below ~768px)
- **No backend required** — static site, no forms that require server processing (a "Contact" mailto: link is sufficient)
- **Performance:** Single photo asset optimized (compressed), no heavy libraries needed
- **Accessibility:** Sufficient contrast between purple accent and dark background for text; alt text on photo

---

## 7. Explicit Exclusions (things intentionally left out)

- **No fabricated testimonials.** The reference theme includes a fake client quote — this is excluded entirely. If Yash later gets genuine feedback (a manager quote, a LinkedIn recommendation), it can be added truthfully then.
- **No inflated stats** ("years of experience," "happy clients," "100% satisfaction") — replaced with real, verifiable numbers.
- **No unearned skills** (e.g., no cloud/Snowflake/Airflow claims) — matches the resume exactly, consistent with the honesty standard maintained throughout the resume-building work.

---

## 8. Decisions Made (previously open, now resolved)

1. **Phone number:** Included publicly in Contact/Footer section.
2. **Project detail format:** Expandable inline cards (click to open/close) rather than separate case-study pages — keeps everything on one page, no extra routing needed.
3. **Skill percentages:** Set as self-assessed values (Excel 90%, SQL 85%, Power BI 85%, Python 75%, Business Analysis 75%, Tableau 65%), explicitly labeled "Self-assessed proficiency, not a third-party benchmark" so it's not misread as a certified score.
4. **Resume download:** Both versions offered via a dropdown button — Data Analyst version and Business Analyst version, each with a one-line description of its focus.

---

## 9. Delivered Build

Built as a single-page static site:
- `index.html` — full site (nav, hero, about, skills, projects, certifications, contact/footer)
- `photo.jpg` — provided headshot, used in hero
- `Yash_Pratap_Singh_Resume_DataAnalyst.pdf` / `Yash_Pratap_Singh_Resume_BusinessAnalyst.pdf` — linked from the resume dropdown

All 4 files must stay in the same folder for the relative links to resolve. No build step or backend required — deployable as-is to any static host (Netlify, Vercel, GitHub Pages).

**Design notes on the build:**
- Palette pulls a warm amber secondary accent directly from the provided photo's lighting, paired with the requested violet/purple primary accent — ties the two together rather than using purple in isolation
- Metric callouts in the hero (₹2.06 Cr, 25.29%) replace the reference site's code-snippet card, grounding the hero visual in data-analyst subject matter
- Mobile: working hamburger menu (reference template's mobile nav was non-functional at this breakpoint; this build fixes that)

