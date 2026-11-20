# SecureVyapar Prototype - Testing Guide

## 📋 Overview
This guide helps you test the SecureVyapar prototype against the PRD success criteria.

## 📁 Files Involved
- `index.html` — Full prototype (landing → wizard → results → scanner)
- `css/styles.css` — Design system with responsive tokens
- `user-testing-form.md` — Printable feedback form for user interviews

## 🔧 Quick Start

### 1. Open the Prototype
**Location:** `C:\Users\HP\Documents\Default Project\securevyapar\index.html`

**Methods:**
- Double-click the file
- Right-click → "Open with" → Chrome/Firefox/Edge
- Or drag the file into your browser window

**URL:** `file:///C:/Users/HP/Documents/Default%20Project/securevyapar/index.html`

---

## 🧪 Test Scenario 1: Complete Assessment Flow

### Step 1: Start the Assessment
1. Landing page loads with headline: "Is your shop safe online?"
2. Click the **green button**: "Check My Security Free"
3. Assessment wizard appears: "1 / 25" progress indicator

### Step 2: Answer 25 Questions
- Each question has 3 options (a, b, c)
- Select an answer and click "Next >"
- Progress bar fills from 0% to 100%
- Can click "Previous" to go back

**Sample Questions:**
- Q1: UPI payment request from unknown sender → Ignore / Reply / Click link
- Q2: Same password for email and banking? → Different / Same / Don't use
- Q3: Backup frequency → Daily / Weekly / Never
- Q4: WhatsApp "free recharge" links → Never / Once / Frequently
- Q5: Two-factor authentication → Always / Sometimes / No
- ... (20 more questions)

**Verify:** Score updates with each answer (0–100 scale)

### Step 3: View Results
After question 25, you see:
- **Shop Safety Score** (large number, color-coded pill)
- **Status**: Green (80–100) / Amber (50–79) / Red (0–49)
- **Category bars**: 5 categories with progress (0–25)
- **Top risks**: Dynamic list based on your score
- **Action plan**: 3 prioritized "Fix first" steps
- **CTAs**: "Get Detailed Report (₹299)" and "Scan a suspicious link"

**Verify:** You can identify your score range and what it means.

---

## 🔗 Test Scenario 2: Link Scanner

### Step 1: Access Link Scanner
- Click "Scan a suspicious link" in the results CTA band
- OR click "Scan Link" in the top navbar
- OR go to the "Link Scanner" section from the navbar

### Step 2: Test URLs
Test each URL and verify the verdict:

| Test URL | Expected Result | What to Check |
|----------|----------------|---------------|
| `upi://pay?pa=scammer@upi&am=500` | **Dangerous** / High risk | Shows "Fake UPI Payment Request" with explanation |
| `http://secure-gpay-login.com` | **Dangerous** / High risk | Shows "Fake Payment App Login" with explanation |
| `free-recharge.xyz` | **Dangerous** / High risk | Shows "Free Recharge Scam" with explanation |
| `www.google.com` | **Safe** / Low risk | Shows "Link appears safe" with checkmark |
| `bit.ly/xyz123` | **Suspicious** / Medium risk | Shows "URL Shortener" with explanation |

**Verify:** 
- Verdict icon color (red/amber/green)
- Plain-language explanation
- "Recommended action" button
- Signal details below the verdict

---

## 📄 Test Scenario 3: PDF Report Generation

### Step 1: Complete Assessment
Finish the 25-question assessment to see your results page.

### Step 2: Generate PDF
1. In the results CTA band, click the **green button**: "Generate PDF Report"
2. jsPDF library initializes (first time may take 1–2 seconds)
3. PDF report opens in a new tab/downloads automatically
4. Filename: `SecureVyapar_Shop_Safety_Report_[score].pdf`

### Step 2: Verify PDF Contents
- [ ] Shop Safety Score at top (large, color-coded)
- [ ] Category breakdown bars with percentages
- [ ] Top risks identified (2–3 bullet points)
- [ ] 3-step action plan (priority fixes)
- [ ] Footer: "SecureVyapar · Simplifying security for Indian small businesses"
- [ ] Download button to save the PDF

**Verify:** The PDF is professional-looking and contains all key information.

---

## 🌐 Test Scenario 4: Language Toggle

### Step 1: Locate Language Button
- Click the **language button** (English ▼) in the top navbar
- Dropdown shows: English / मराठी / हिन्दी

### Step 2: Switch Languages
- Click "मराठी" → All UI text changes to Marathi
- Click "हिंदी" → All UI text changes to Hindi
- Click "English" → Returns to English

**UI Elements That Change:**
- Hero headline ("Is your shop safe online?")
- Assessment questions and help text
- Score status pills (Mostly safe / Needs attention / High risk)
- Category labels (Identity & 2FA, Backups, etc.)
- Action plan steps
- Footer text
- Navigation links

**Verify:** All major text elements translate when switching languages.

---

## 📊 Test Scenario 5: Mobile Responsiveness

### Step 1: Resize Browser
- Drag the browser window to narrow it (simulate a phone)
- Or open on an actual Android phone (6-inch viewport)

### Step 2: Check Mobile Features
- [ ] No horizontal scroll bar
- [ ] Hamburger menu appears for navigation
- [ ] All buttons are ≥44×44px tap target
- [ ] Category bars stack vertically
- [ ] Progress indicator is visible
- [ ] Text is readable without zooming
- [ ] "Give Feedback" button is accessible

### Step 3: Test Touch Features
- [ ] Can select radio answers with finger/tap
- [ ] "Next" button is tappable
- [ ] Link scanner input field accepts pasting text
- [ ] PDF button is accessible

---

## 📊 Success Metrics (from PRD.md)

### Pass/Fail Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Users completing assessment | 50+ in testing | Count finished assessments |
| Users who "like/love" prototype | ≥ 40% | Post-test survey question |
| Time to complete free check | ≤ 3 minutes | Stopwatch / self-reported |
| Clarity of risk score | High (user feedback) | "Did you understand your score?" (Yes/No) |
| Conversion intent (would pay ₹299) | ≥ 20% | "Would you pay ₹299 for detailed report?" |

### Post-Test Survey Questions

1. "What is your Shop Safety Score and what does it mean?"
2. "Do you know what to do next after seeing the score?"
3. "Would you consider paying ₹299 for a detailed PDF report? Why/why not?"
4. "Was the interface easy to understand? What was confusing?"
5. "Do you trust the tool? Why/why not?"
6. "Would you use this regularly? Why/why not?"
7. **Key Quote**: "My favorite/least favorite part was..."

---

## 📝 Documentation Template

### Per Participant

```
Participant ID: ______
Age: ______  Tech Comfort: Low/Med/High
UPI Usage: Yes/No/Sometimes

--- Assessment Results ---
Final Score: ______/100
Status: Green/Amber/Red
Understood score: Yes/Partly/No
Knows next steps: Yes/Partly/No

--- Link Scanner Results ---
Safe URL test: ______ → Result: ______
Unsafe URL test: ______ → Result: ______

--- Feedback ---
Would pay ₹299: Yes/No/Maybe
Favorite part: ____________________
Least favorite part: ____________________
Key quote: _________________________________

--- Overall ---
Likelihood to recommend: 1–10 scale
Likelihood to use again: 1–10 scale
Additional comments: ____________________
```

### Aggregated Results (After 15 Users)

| Metric | Target | Actual |
|--------|--------|--------|
| Users completing assessment | 50+ | ______ / 15 |
| Users who "like/love" it | ≥ 40% | ______ / 15 (__%) |
| Avg. time to complete | ≤ 3 min | ______ min |
| Would pay ₹299 | ≥ 20% | ______ / 15 (__%) |
| Users finding score clear | -- | ______ / 15 (__%) |

**Key learnings:**  
> ________________________________________________________  

**Recommended improvements:**  
> ________________________________________________________  

---

## ❓ Need Help?

**Having trouble with a specific test?**  
- Link scanner not matching a URL? → Check the 7 SCAM_PATTERNS in the code
- Language not switching? → Verify `data-lang` attribute is being set
- PDF not generating? → Ensure jsScript CDN is loaded and jsPDF is available
- Mobile layout issues? → Check @media breakpoints at 860px and 680px

**Contact:** SecureVyapar Team  
**Version:** v1.0 (Phase 1.5)  
**Date:** _______________