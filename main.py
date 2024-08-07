from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

# setting up the driver
driver_path = ":/home/user/chrome-linux64/chrome"
# Set the path to the ChromeDriver executable in the PATH environment variable
os.environ["PATH"] += driver_path
driver = webdriver.Chrome()
driver.set_page_load_timeout(18)
try:
    driver.get(url="https://www.genius.com/artists/tyler-the-creator/songs")
except TimeoutException:
    driver.execute_script("window.stop();")
# Wait for the dropdown button to be clickable and then click it
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.Dropdown__Toggle-ugfjuc-2'))
)
dropdown_button.click()

# Wait for the "A-Z" option to be visible and then click it
a_to_z_option = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//li[text()='A-Z']"))
)
a_to_z_option.click()
time.sleep(3)

# find the number of songs
no_of_songs = driver.find_element(by=By.XPATH, value="//div/h2[contains(@class,'ListSectiondesktop')]")
no_of_songs = no_of_songs.find_element(by=By.XPATH, value="following-sibling::*[1]")
# print(no_of_songs.text)
# split the string to obtain the number
number_of_songs = no_of_songs.text.split(sep="includes ")[1].split(sep=" songs")[0]
print(f"number is {int(number_of_songs)}")
number_of_songs = int(number_of_songs)

# find song element
song_elements = driver.find_elements(by=By.XPATH, value="//div/ul/li/a")


# implement scroll
def has_increased(driver):
    loaded_songs = driver.find_elements(by=By.XPATH, value="//div/ul/li/a")
    return len(loaded_songs) > len(song_elements)


# loop guard checks if loaded songs < number_of_songs
loaded_flag = 0
while len(song_elements) < number_of_songs:
    song_elements = driver.find_elements(by=By.XPATH, value="//div/ul/li/a")

    # todo implement scroll here
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # todo implement a wait for elements to load up

    try:
        WebDriverWait(driver, timeout=6).until(method=has_increased, message="exited")
    except TimeoutException:
        song_element = driver.find_elements(by=By.XPATH, value="//div/ul/li/a")
        if number_of_songs - len(song_element) < 10:
            break
        else:

            print(f"current no is {len(song_element)}")
            # todo detect if the page is no longer loading
            if loaded_flag > 2 :
                print(f"loaded_flag = {loaded_flag}")
                break
            else:
                loaded_flag += 1
                continue
total_songs_found = len(song_elements)
print(f"scroll has discovered {total_songs_found} songs")
song_link = song_elements[1].get_attribute('href')
all_song_links = [x.get_attribute('href') for x in song_elements]
driver.set_page_load_timeout(10)
for song_link in all_song_links:
    try:
        driver.get(url=song_link)
    except TimeoutException:
        driver.execute_script("window.stop();")

    # todo find song name
    try:
        song_name = driver.find_element(by=By.XPATH, value="//h1/span[contains(@class,'SongHeaderdesktop')]")
        song_name = song_name.text
    except TimeoutException:
        continue

    lyrics_text = ""
    # todo fetch the lyrics to the song
    div_lyrics_container = driver.find_elements(by=By.XPATH, value="//div[contains(@class,'Lyrics__Container')]")
    for x in div_lyrics_container:
        try:
            lyrics_text += x.text
        except TimeoutException:
            continue

    # todo write to a txt file
    # Replace '/' with '_'
    song_name = song_name.replace('/', '_')

    with open(file=f"{song_name}.txt", mode="w") as file:
        file.write(lyrics_text)

time.sleep(200)

# except TimeoutException:
#    driver.execute_script("window.stop();")  # Stop loading the page
#
# find the search bar
# sent = 0
# driver.set_page_load_timeout(time_to_wait=300)
# search_bar = driver.find_element(by=By.XPATH, value="//form/input")
# search_bar.click()
# search_bar.send_keys("Drake")
# driver.set_page_load_timeout(12)
# try:
#    search_bar.send_keys(Keys.RETURN)
# except TimeoutException:
#    driver.execute_script("window.stop();")
# time_now=time.time()
# elapsed_time=0
## while elapsed_time < 12:
##     print("b")
##     elapsed_time=time.time() - time_now
## try:
##     driver.execute_script("window.stop();")
##     print("stopped")
## except:
##     pass
## find the top result
# top_result_div = driver.find_element(by=By.XPATH, value="//search-result-section/div/div")
# artist_link=driver.find_element(by=By.XPATH,value="//mini-artist-card/a")
# all_songs_link=driver.find_element(by=By.XPATH,value="//a/div[contains(@text(),'Show all songs')]")
# all_songs_link=all_songs_link.parent
# all_songs_link.click()
# driver.set_page_load_timeout(100)
# artist_link.click()
# time.sleep(50)
