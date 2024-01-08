import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import os
from datetime import timedelta
import re

# Import the functions from block_sites.py and unblock_sites.py
from block_sites import modify_hosts_file
from unblock_sites import remove_entry_from_hosts

def save_history(data, filename='history.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_history(filename='history.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def parse_time(time_str):
    # Extract hours, minutes, and seconds from the time string
    match = re.match(r'(\d+):(\d+):(\d+) hrs', time_str)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return timedelta()

def is_time_difference_significant(old_time_str, new_time_str, threshold_minutes=30):
    old_time = parse_time(old_time_str)
    new_time = parse_time(new_time_str)
    time_diff = new_time - old_time
    return time_diff > timedelta(minutes=threshold_minutes)

def find_differences(old_data, new_data):
    differences = {}
    for key, new_value in new_data.items():
        old_value = old_data.get(key)
        if old_value != new_value:
            differences[key] = {'old': old_value, 'new': new_value}
    return differences

def get_lifetime_totals():
    driver = webdriver.Safari()  # use Safari instead of Chrome
    driver.get("https://connect.garmin.com/modern/profile/3276ce24-3f12-4709-ac61-72e148253700")

    # Wait for the page or a specific element on the page to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Lifetime Total')]")))

    # find the div with text 'Lifetime Total'
    stats_group = driver.find_element(By.XPATH, "//*[contains(@class, 'UserStats_statsGroup__') and contains(., 'Lifetime Total')]")

    # Now find all elements with class name containing 'LifetimeTotals_statsList__' within this stats_group
    stats_lists = stats_group.find_elements(By.CSS_SELECTOR, "[class*='LifetimeTotals_statsList__']")
    lifetime_totals = {}

    # iterate over the stats lists
    for stats_list in stats_lists:
        # find all li elements in the current stats list
        stats_items = stats_list.find_elements(By.TAG_NAME, 'li')

        # iterate over the stats items and store them in the dictionary
        for item in stats_items:
            label = item.find_element(By.CSS_SELECTOR, "[class*='statLabel']").text
            data = item.find_element(By.CSS_SELECTOR, "[class*='statData']").text
            lifetime_totals[label] = data

    driver.quit()  # close the browser when you're done

    return lifetime_totals

# After fetching the lifetime totals
lifetime_totals = get_lifetime_totals()

# Load the history
history = load_history()

# Find the differences
differences = find_differences(history, lifetime_totals)

print(differences)

# Update the history with the new data
history.update(lifetime_totals)

# Save the updated history
save_history(history)

# Print out the differences
print("Differences found:")
for key, value in differences.items():
    print(f"{key}: Old Value: {value['old']}, New Value: {value['new']}")

if "Time" in differences:
    print("Time has changed!")
    significant_change = is_time_difference_significant(differences["Time"]['old'], differences["Time"]['new'])
    if significant_change:
        print(f"Time difference is significant: {significant_change}")
        # Call the unblock function if the time difference is significant
        remove_entry_from_hosts('www.example.com')
    else:
        print(f"Time difference is not significant: {significant_change}")
else :
    print("Time has not changed.")
    # Call the block function if the time has not changed
    modify_hosts_file('www.example.com', '127.0.0.1')
