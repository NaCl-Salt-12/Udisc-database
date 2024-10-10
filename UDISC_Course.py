from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

# List of URLs to scrape
links = [
    "https://udisc.com/courses/byu-idaho-bgX9",
    "https://udisc.com/courses/nature-park-I7t3",
    "https://udisc.com/courses/aspen-acres-dg-lzRM"
]

# Initialize the WebDriver
driver = webdriver.Chrome()

# Store course data in a list
course_data = []

# Loop through each URL
for url in links:
    driver.get(url)

    try:
        # Wait for the course name element to be present and extract its text
        course_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './html/body/div[1]/div/div[2]/div/div/div/div[1]/a/h1'))
        ).text
        
        # Extract city and state
        city_state = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/span').text
        city, state = city_state.split(',')
        
        # Extract additional information about the course
        about = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/main/div[1]/section[3]/div[1]').text
        
        # Append the extracted data to the list
        course_data.append({
            'course_name': course_name,
            'city': city.strip(),
            'state': state.strip(),
            'about': about
        })

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

# Close the WebDriver
driver.quit()

# Convert the collected data into a DataFrame
df = pd.DataFrame(course_data)

# Export the DataFrame to a CSV file with a comma delimiter and double quotes around strings
df.to_csv('course_data.csv', sep=',', index=False, quoting=1, encoding='utf-8')

print("Data exported to course_data.csv with proper format for MySQL import.")
