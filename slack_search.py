import sqlite3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver_with_existing_profile(profile_path):
    options = Options()
    options.profile = profile_path
    service = FirefoxService(executable_path=r'./geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def check_login_success(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.title_contains("Slack - Search - Red Hat Inc.")
        )
        print("Login appears to be successful based on the page title.")
    except TimeoutException:
        print("Login might not have been successful. Check if redirected to login page.")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        body_text = driver.find_element(By.TAG_NAME, 'body').text[:500]
        print(f"Page body snippet: {body_text}")


def perform_slack_search(driver, search_url, search_query):
    driver.get(search_url)
    # Wait for the search input to become clickable, ensuring it starts with 'Search'
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder^='Search']"))
    )
    # Find the search input using the same condition
    search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder^='Search']")
    search_input.click()  # Click the search bar to activate it
    search_input.clear()  # Clear any pre-filled text
    search_input.send_keys(search_query)  # Enter the search query
    search_input.send_keys(Keys.RETURN)  # Press Enter to initiate the search


def main():
    # Replace with your actual profile path:
    # find in Firefox with about:profiles it's the "Local Directory" value
    profile_path = "/Users/btofel/Library/Application Support/Firefox/Profiles/ok6k84nz.default-release"
    driver = setup_driver_with_existing_profile(profile_path)
    try:
        slack_search_url = "https://app.slack.com/client/E030G10V24F/search"
        search_query = "foosball"  # Replace with your actual search term
        perform_slack_search(driver, slack_search_url, search_query)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
