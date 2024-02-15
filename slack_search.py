import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import NoSuchElementException


def fetch_cookies_for_domain(db_path, domain):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, value FROM moz_cookies WHERE host LIKE ?", ('%' + domain + '%',))
    cookies = cur.fetchall()
    conn.close()
    return cookies


from selenium.webdriver.firefox.options import Options

def setup_driver_with_existing_profile(profile_path):
    # Set Firefox Options to use the existing profile
    options = Options()
    options.profile = profile_path
    service = FirefoxService(executable_path=r'./geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def check_login_success(driver):
    time.sleep(5)  # Allow time for any redirects and for the page to load
    try:
        # Using a generic element that should be visible after login, adjust as needed
        driver.find_element(By.CSS_SELECTOR, "[data-qa='top_nav']")
        print("Login appears to be successful.")
    except NoSuchElementException:
        print("Login might not have been successful. Check if redirected to login page.")
        # Additional debugging: Print current URL and page title
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")


def perform_slack_search(driver, search_url):
    driver.get(search_url)  # Make sure to navigate to the search URL
    check_login_success(driver)  # Debugging login

    time.sleep(5)  # Allow time for page load and dynamic content

    # Now, attempting to interact with the search or finding elements
    try:
        # Adjust as needed based on actual elements for search results on Slack
        search_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        print(f"Number of elements found: {len(search_elements)}")
        for element in search_elements[:3]:  # Just as an example, print out first few
            print(element.text[:100])  # Print a snippet of each result for verification
    except Exception as e:
        print(f"Error finding or printing elements: {e}")


def main():
    # Replace with your actual profile path:
    # find in Firefox with about:profiles it's the "Local Directory" value
    profile_path = "/Users/btofel/Library/Application Support/Firefox/Profiles/ok6k84nz.default-release"
    driver = setup_driver_with_existing_profile(profile_path)
    try:
        slack_search_url = "https://app.slack.com/client/E030G10V24F/search"
        perform_slack_search(driver, slack_search_url)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
