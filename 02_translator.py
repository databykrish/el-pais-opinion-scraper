"""
Translation & Analysis Module

✔ Translates Spanish titles → English
✔ Uses RapidAPI translation (optional)
✔ Performs word frequency analysis
✔ Detects repeated words (>2 occurrences)
✔ Saves results to JSON
"""

import requests
import json
from collections import Counter
import time
import re


# ============================================================================
# TRANSLATION FUNCTION
# ============================================================================

def translate_with_rapid_api(spanish_text, api_key):

    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

    payload = {
        "from": "es",
        "to": "en",
        "type": "text",
        "q": spanish_text
    }

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                return result[0]

            if isinstance(result, dict) and 't' in result:
                return result['t']

            return f"Error: Unknown response → {result}"

        return f"Error {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# ============================================================================
# WORD FREQUENCY ANALYSIS (UPDATED ⭐)
# ============================================================================

def analyze_word_frequency(translated_titles):
    """Find words repeated more than twice"""

    all_words = []

    for title in translated_titles:
        # ✅ Clean word extraction using regex
        words = re.findall(r"\b[a-zA-Z]+\b", title.lower())
        all_words.extend(words)

    word_counts = Counter(all_words)

    repeated_words = {
        word: count
        for word, count in word_counts.items()
        if count > 2
    }

    return repeated_words, word_counts


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print("TRANSLATION & WORD FREQUENCY ANALYSIS")
    print("=" * 70)

    # ──────────────────────────────────────────────────────────────
    # STEP 1 — API Key Input
    # ──────────────────────────────────────────────────────────────

    api_key = input("\nPaste RapidAPI Key (or press Enter to skip): ").strip()

    if not api_key:
        print("\n⚠️ No API key provided → Using fallback demo translations")
        api_key = None

    # ──────────────────────────────────────────────────────────────
    # STEP 2 — Load Scraped Articles
    # ──────────────────────────────────────────────────────────────

    print("\n[STEP 1] Loading scraped_articles.json...")
    print("─" * 70)

    try:
        with open("scraped_articles.json", "r", encoding="utf-8") as f:
            articles_data = json.load(f)

        spanish_titles = [
            article["title"]
            for article in articles_data
            if article.get("title")
        ]

        print(f"✓ Loaded {len(spanish_titles)} Spanish titles")

    except FileNotFoundError:
        print("✗ scraped_articles.json not found")
        print("→ Run scraper.py first")
        return

    print("\n📋 Spanish Titles:")
    for i, title in enumerate(spanish_titles, 1):
        print(f"{i}. {title}")

    # ──────────────────────────────────────────────────────────────
    # STEP 3 — Translation
    # ──────────────────────────────────────────────────────────────

    print("\n[STEP 2] Translating titles...")
    print("─" * 70)

    translated_titles = []

    if api_key:
        for i, title in enumerate(spanish_titles, 1):
            print(f"\n{i}. Spanish: {title}")

            translated = translate_with_rapid_api(title, api_key)
            translated_titles.append(translated)

            print(f"   English: {translated}")

            if i < len(spanish_titles):
                time.sleep(1)

    else:
        # ✅ Simple fallback translations (for demo only)
        translated_titles = [f"[Demo Translation] {t}" for t in spanish_titles]

        for sp, en in zip(spanish_titles, translated_titles):
            print(f"\n✓ Spanish: {sp}")
            print(f"  English: {en}")

    # ──────────────────────────────────────────────────────────────
    # STEP 4 — Word Frequency Analysis
    # ──────────────────────────────────────────────────────────────

    print("\n[STEP 3] Analyzing repeated words...")
    print("─" * 70)

    repeated_words, all_word_counts = analyze_word_frequency(translated_titles)

    if repeated_words:
        print("\n✓ Repeated Words (>2 occurrences):\n")

        sorted_words = sorted(
            repeated_words.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for word, count in sorted_words:
            print(f"'{word}' → {count} times")

    else:
        print("\n✓ No words repeated more than twice")

    # ──────────────────────────────────────────────────────────────
    # STEP 5 — Save Results
    # ──────────────────────────────────────────────────────────────

    print("\n[STEP 4] Saving results...")
    print("─" * 70)

    results = {
        "spanish_titles": spanish_titles,
        "translated_titles": translated_titles,
        "repeated_words": repeated_words,
        "all_word_counts": dict(all_word_counts)
    }

    with open("translation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("✓ Saved → translation_results.json")

    print("\n" + "=" * 70)
    print("PROCESS COMPLETE ✅")
    print("=" * 70)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
