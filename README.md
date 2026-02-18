#  El País Opinion Scraper  
### Selenium • API Integration • Text Intelligence • BrowserStack

---

## Project Context

Developed as part of a **Customer Engineer Interview Assignment**, this project simulates a real-world SaaS testing and automation scenario involving:

✔ Dynamic website automation  
✔ Intelligent data extraction  
✔ Third-party API integration  
✔ Text processing & analysis  
✔ Cross-browser & cross-device validation  

This solution reflects how a **Customer Engineer bridges product capabilities with practical technical execution**.

---

#  Problem Statement

Modern automation and testing workflows must handle:

❌ Dynamic, JavaScript-heavy websites  
❌ Cookie consent interruptions  
❌ Lazy-loaded content  
❌ Inconsistent DOM structures  
❌ Cross-browser compatibility  
❌ Real mobile device behaviour  

**Objective:**  
Build a resilient automation pipeline that scrapes Spanish news content, enriches it through translation APIs, performs text intelligence, and validates execution across browsers/devices using BrowserStack.

---

#  Key Challenges Encountered

###  1. Cookie Consent Blocking Automation
- Multi-layered consent dialogs
- Click interception issues

**Solution Implemented:**  
✔ Automated cookie banner detection  
✔ Fallback selectors  
✔ Explicit wait strategies  

---

###  2. Lazy-Loaded / Dynamic Content
- Articles not immediately available
- Scroll-triggered rendering

**Solution Implemented:**  
✔ Programmatic scrolling  
✔ Lazy-load triggering  
✔ Robust WebDriverWait logic  

---

###  3. Inconsistent Article Structures
- Titles located in varying HTML hierarchies

**Solution Implemented:**  
✔ Multi-selector fallback strategy  
✔ DOM-agnostic extraction  

---

###  4. Translation API Response Variability
- API returning list vs dictionary formats

**Solution Implemented:**  
✔ Response normalization layer  
✔ Defensive parsing logic  

---

###  5. Parallel Execution Complexity
- Running concurrent BrowserStack sessions

**Solution Implemented:**  
✔ Python threading  
✔ Parallel Selenium execution  

---

###  6. Cross-Browser / Cross-Device Behaviour
- Desktop vs Mobile rendering differences

**Solution Implemented:**  
✔ BrowserStack Automate integration  
✔ Real mobile device testing  

---
#  Solution Architecture

```
Selenium Scraper
      ↓
Spanish Article Data
      ↓
Translation API
      ↓
English Headers
      ↓
Word Frequency Analysis
      ↓
BrowserStack Parallel Tests
      ↓
Cross-Browser Screenshots
```
---

#  Features Implemented

##  Web Scraping Automation (Selenium)

- Navigates to **El País – Opinion Section**
- Ensures **Spanish language content**
- Extracts:
  - Spanish Article Titles  
  - Spanish Article Content  
  - Cover Images (if available)

 Output:
- `04_scraped_articles.json`
- `article_images/`

---

##  Translation & Enrichment (RapidAPI)

- Spanish → English translation
- Rapid Translate Multi Traduction API integration
- API response normalization

 Output:
- `05_translation_results.json`

---

##  Text Intelligence & Analysis

- Tokenization of translated headers
- Word frequency computation
- Detection of repeated words (>2 occurrences)

---

##  Cloud Cross-Browser Testing (BrowserStack)

Executed using **BrowserStack Automate**

 Desktop Browsers:
- Chrome – Windows 10  
- Firefox – Windows 10  
- Safari – macOS Monterey  

 Real Mobile Devices:
- Samsung Galaxy S22  
- iPhone 14  

✔ Parallel execution  
✔ Cloud Selenium Grid  
✔ Session status reporting  
✔ Automated screenshot capture  

 Output:
- `screenshots/`

---

#  Visual Validation

Automated screenshots captured across:

✔ Desktop browsers  
✔ Real mobile devices  

Ensuring:

✅ Spanish content consistency  
✅ Correct UI rendering  
✅ Cross-browser reliability  

---

#  Tech Stack

- **Python**
- **Selenium WebDriver**
- **BrowserStack Automate**
- **RapidAPI (Translation API)**
- **Requests**
- **BeautifulSoup**
- **Threading**

---
#  How To Run

## 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 2️⃣ Run Scraper
```bash
python 01_scraper.py
```

## 3️⃣ Run Translator
```bash
python 02_translator.py
```
(Provide RapidAPI key when prompted)

## 4️⃣ Run BrowserStack Tests
```bash
python 03_browserstack_test.py
```
---
# ⭐ Technologies & Tools

![Python](https://img.shields.io/badge/Python-3.x-blue)    
![Selenium](https://img.shields.io/badge/Selenium-Automation-green)    
![BrowserStack](https://img.shields.io/badge/Tested%20on-BrowserStack-orange)    
![API](https://img.shields.io/badge/API-Integrated-purple)  

