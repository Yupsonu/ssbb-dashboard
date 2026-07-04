# SSBB Project Dashboard (Streamlit)

A Streamlit rebuild of the Power BI **SSBB PROJECT DASHBOARD**, reading directly
from `SSBB.xlsx`. It re-reads the file automatically whenever it changes on disk,
so you can keep editing the Excel tracker and watch the dashboard update.

## 1. Install

```bash
pip install -r requirements.txt
```

(`streamlit-autorefresh` is optional but recommended — it lets the page
poll for changes on a timer instead of needing a manual reload.)

## 2. Place your data

Put `SSBB.xlsx` in the same folder as `app.py` (or point to it via the
"Path to Excel file" field in the sidebar once the app is running).

The app expects the sheet named `SSBB Batch 1&2 Tracking ` with the same
column layout as the original tracker (Batch, Participant's Name, Department,
ARS, and the D / M / A / I / C phase-status columns).

## 3. Run

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

## 4. How the auto-refresh works

- The sidebar has an **Auto-refresh dashboard** toggle (on by default) and an
  interval slider. When `streamlit-autorefresh` is installed, the page
  silently reruns on that interval and picks up any change to `SSBB.xlsx`
  (checked via the file's modified time + size, so nothing reloads unless the
  file actually changed).
- There's also a manual **🔄 Refresh now** button if you'd rather not auto-poll.
- If you edit the Excel file in Excel/LibreOffice, just save it — the next
  refresh tick (or a page reload) will show the new numbers.

## What's on the dashboard

- **KPI row:** Total Projects, Participants, Departments, Total ARS
- **DMAIC row:** count of projects that completed each of Define / Measure /
  Analyze / Improve / Control
- **Participant Completion Status (%):** average of the 5 phase-completion
  flags per participant, across all their projects
- **Total ARS by Department:** summed ARS (INR Lakh) per department
- **Overall Project Completion (%):** gauge showing the average completion
  percentage across all filtered projects
- **Filters:** Batch, Participant's Name, Department (sidebar)

## Note on one figure

The original Power BI dashboard shows **Participants = 65**, identical to
**Total Projects = 65** — that card was actually counting rows, not distinct
people (there are only 60 unique participant names; several people own more
than one project). This Streamlit version shows the *true* distinct headcount
(60) instead, since that's what "Participants" should mean. If you want exact
1:1 parity with the original PDF instead, change `total_participants` in
`app.py` from `fdf["Participant"].nunique()` to `len(fdf)`.
