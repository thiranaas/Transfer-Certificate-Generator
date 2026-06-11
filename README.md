# 🎓 Transfer Certificate Generator

A desktop application for managing student Transfer Certificate (TC) requests in a school setting — from submission to approval to PDF generation.

---

## Overview

This system streamlines the TC workflow between school admins and the principal. Admins submit TC requests for students; the principal reviews and approves or rejects them. Approved certificates are automatically generated as formatted PDFs.

---

## Features

- 🔐 Role-based login — separate flows for **Admin** and **Principal**
- 📋 TC request submission with student detail validation
- ✅ Principal approval / rejection workflow
- 📄 Auto-generated PDF Transfer Certificates (with school header, logo, and signature fields)
- 🔑 Password reset functionality
- 💾 CSV-based data storage — no database required

---

## Tech Stack

| Purpose | Library |
|---|---|
| GUI | `CustomTkinter` |
| PDF Generation | `ReportLab` |
| Image Handling | `Pillow (PIL)` |
| Data Storage | `csv` (built-in) |

---

## How It Works

### Step 1 — Login
When the application starts, both the Admin and the Principal land on the same login screen. They enter their username and password, which are verified against `Data.csv`. Based on the role, the system routes them to their respective dashboard. If a user forgets their password, they can reset it directly from the login screen.

---

### Step 2 — Admin Submits a TC Request
Once logged in, the Admin opens the **TC Generator** form and fills in the student's details:

- Admission Number *(validated against `Data.csv` — an error is shown if it doesn't exist)*
- Class the student is promoted to
- Fees concession details
- Date of application and date of issue
- Reason for leaving the school

On submission, the request is saved to `Pending_TCs.csv` with a **"Pending"** status and waits for the Principal's review.

---

### Step 3 — Principal Reviews the Request
The Principal logs in and opens the **TC Approval** panel, which loads all pending requests from `Pending_TCs.csv`. Requests are shown one at a time. The Principal can:

- **Approve** — triggers PDF generation, removes the record from `Pending_TCs.csv`, and deletes the student's entry from `Data.csv`
- **Reject** — marks the request accordingly in `Pending_TCs.csv`

---

### Step 4 — PDF is Generated
On approval, the system automatically creates a formatted Transfer Certificate as a PDF file, saved in the project folder. The certificate includes all student details, school header, logo, a formal border, and signature fields for the Principal.

---

## UI Overview

| Screen | Description |
|---|---|
| **Login** | Username/password entry with a password reset option |
| **Admin Dashboard** | Access to TC Generator and logout |
| **TC Generator Form** | Fields: Admission No, Promoted To, Fees Concession, Date of Application, Date of Issue, Reason for Leaving |
| **Principal Dashboard** | Access to TC Approval panel and logout |
| **TC Approval Panel** | Displays pending requests one at a time with Approve / Reject buttons |

---

## Generated PDF Contains

- School name, logo, and formal border
- Student name, father/guardian's name, mother's name
- Nationality, admission number
- Last class studied and subjects
- Class promoted to
- Fees concession details
- Date of application and date of issue
- Reason for leaving
- Signature fields for the principal

PDFs are saved to the project root directory.

---

## Function Reference

| Function | Role |
|---|---|
| `userlogin()` | Renders the login window; validates credentials from `Data.csv` |
| `reset_password()` | Opens the password reset window |
| `update_password()` | Validates and updates the new password in `Data.csv` |
| `collect_input()` | Handles input from login and TC forms; validates admission numbers |
| `mainpage1()` | Admin dashboard — TC Generator and logout |
| `mainpage2()` | Principal dashboard — TC Approval and logout |
| `open_tc_generator()` | Calls `tc()` |
| `open_tc_approval()` | Calls `principal_approve()` |
| `tc()` | TC request form window |
| `principal_approve()` | Loads and displays pending TC requests for review |
| `load_pending_requests()` | Reads all records from `Pending_TCs.csv` |
| `approve_tc()` | Triggers PDF generation, removes record from both CSV files |
| `reject_tc()` | Marks the request status in `Pending_TCs.csv` |
| `save_requests_to_file()` | Writes updated records back to `Pending_TCs.csv` |
| `create_pdf()` | Generates the formatted Transfer Certificate PDF |
| `logout()` | Clears session and returns to the login screen |

---

## Data Files

| File | Purpose |
|---|---|
| `Data.csv` | Stores user credentials and student records |
| `Pending_TCs.csv` | Tracks TC requests and their approval status |

---

⭐ If you found this project helpful, consider leaving a star — it means a lot!
