from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import requests
import os
import json
import re
import time

# folder for images
if not os.path.exists("article_images"):
    os.makedirs("article_images")


# Cookie Handler
def accept_cookies(driver):
    wait = WebDriverWait(driver, 5)

    try:
        accept_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Accept') or contains(., 'Aceptar')]")
            )
        )
        accept_btn.click()
        print("Cookies accepted")

    except TimeoutException:
        print("Cookie banner not shown")

    try:
        agree_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Agree') or contains(., 'Aceptar')]")
            )
        )
        agree_btn.click()
        print("Secondary cookies handled")

    except TimeoutException:
        pass


# Scroll func
def scroll_page(driver, scrolls=5):
    print("\n✓ Triggering lazy loading via scroll...")

    for i in range(scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")
        print(f"Scroll {i+1}")
        time.sleep(1.5)


# image 
def download_image(img_url, filename):
    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
    except:
        pass
    return False


# Title extraction
def extract_title(driver):
    selectors = [
        "h1[data-dtm-region='articulo_titulo']",
        "article h1",
        "header h1",
        "h1"
    ]

    for selector in selectors:
        try:
            title = driver.find_element(By.CSS_SELECTOR, selector).text.strip()
            if title and title.lower() not in ["opinión", "opinion"]:
                return title
        except:
            continue

    try:
        page_title = driver.title.strip()
        return page_title.split("|")[0].strip()
    except:
        return None


# article content extraction
def extract_full_content(driver):
    selectors = [
        "div[data-dtm-region='articulo_cuerpo'] p",
        "article p"
    ]

    for selector in selectors:
        try:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, selector)

            texts = [
                p.text.strip()
                for p in paragraphs
                if p.text.strip() and len(p.text.strip()) > 20
            ]

            if texts:
                return " ".join(texts)

        except:
            continue

    return None


# after everything extract and save
def extract_and_save_image(driver, idx):
    selectors = ["figure img", "article img", "img"]

    for selector in selectors:
        try:
            img = driver.find_element(By.CSS_SELECTOR, selector)
            src = img.get_attribute("src")

            if src and not src.startswith("http"):
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = "https://elpais.com" + src

            if src and src.startswith("http"):
                filename = f"article_images/article_{idx}.jpg"
                if download_image(src, filename):
                    return filename

        except:
            continue

    return None


# main scrapping logic
def scrape_el_pais():
    print("\n" + "=" * 70)
    print("EL PAÍS OPINION SCRAPER")
    print("=" * 70)

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    articles_data = []

    try:
        print("\n[1/6] Opening Opinion section...")
        driver.get("https://elpais.com/opinion/")

        accept_cookies(driver)

        # wait for anchors (more reliable than waiting for articles)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))

        # spanish language confirmation
        lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
        print(f"Language detected: {lang}")

        scroll_page(driver)

        print("\n[2/6] Collecting REAL article links...")

        all_links = driver.find_elements(By.CSS_SELECTOR, "a")
        print(f"Total links found on page: {len(all_links)}")

        article_links = []

        for link_el in all_links:
            try:
                href = link_el.get_attribute("href")

                # ARTICLE FILTER
                if (
                    href
                    and "/opinion/" in href
                    and href.endswith(".html")
                    and not any(x in href for x in ["editoriales", "tribunas", "autores"])
                ):
                    if href not in article_links:
                        article_links.append(href)
                        print("  ✓ Article link captured")

                if len(article_links) == 5:
                    break

            except:
                continue

        print(f"Collected {len(article_links)} article links")

        print("\n[3/6] Scraping articles...")

        for idx, url in enumerate(article_links, 1):
            print("\n" + "─" * 60)
            print(f"ARTICLE {idx}")
            print("─" * 60)

            driver.get(url)
            accept_cookies(driver)

            # to avoid sticky header overlap
            driver.execute_script("window.scrollTo(0, 500);")

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article")))

            title = extract_title(driver)
            content = extract_full_content(driver)
            image = extract_and_save_image(driver, idx)

            print(f"Title: {title}")
            print(f"Content: {content[:120]}..." if content else " Content not found")

            if image:
                print(f"Image saved → {image}")
            else:
                print("No image found")

            articles_data.append({
                "article_number": idx,
                "url": url,
                "title": title,
                "content": content,
                "image": image
            })

        print("\n[4/6] Saving results...")

        with open("scraped_articles.json", "w", encoding="utf-8") as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)

        print("Data saved → scraped_articles.json")

        print("\n[5/6] Spanish Titles:")
        print("=" * 70)
        for article in articles_data:
            print(article["title"])

        print("\n[6/6] Scraping Complete")

    except Exception as e:
        print("Error:", e)

    finally:
        print("\nClosing browser...")
        driver.quit()
        print("Done")


if __name__ == "__main__":
    scrape_el_pais()
