from selenium import webdriver
import time
import os

language_dict = {"1": "zh-TW",
                 "2": "en-GB",
                 "3": "fr-FR",
                 "4": "de-DE",
                 "5": "es-ES",
                 "6": "ru-RU",
                 "7": "it-IT",
                 "8": "ko-KR",
                 "9": "ja-JP", }

language_dict2 = {"zh-TW": "Chinese",
                  "en-GB": "English",
                  "fr-FR": "French",
                  "de-DE": "German",
                  "es-ES": "Spanish",
                  "ru-RU": "Russian",
                  "it-IT": "Italian",
                  "ko-KR": "Korean",
                  "ja-JP": "Japanese", }


def select_languages():
    select_language = "0"

    select_language = input("Select a language to translate into ↓\n"
                            "press 1: Chinese\n"
                            "press 2: English\n"
                            "press 3: French\n"
                            "press 4: German\n"
                            "press 5: Spanish\n"
                            "press 6: Russian\n"
                            "press 7: Italian\n"
                            "press 8: Korean\n"
                            "press 9: Japanese\n")
    try:
        language = language_dict[f'{select_language}']
    except Exception as e:
        print("We don't have this language!!\n"
              "Please choose again!!")
        time.sleep(3)
        select_languages()
    translation(language)


def translation(language):
    # 找到輸入框
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(f"https://translate.google.com.tw/?hl={language}")
    element = driver.find_element_by_id("source")

    # 輸入內容
    str_language = language_dict2[f'{language}']
    translated_text = input(f"The language is {str_language}.\n"
                            "Key in the text(make sure your input is correct):")
    element.send_keys(f'{translated_text}')
    time.sleep(1)
    result = driver.find_element_by_class_name("tlid-translation,translation").text
    print(result)
    menu(driver)


def menu(driver):
    option = input("0 close translation\n"
                   "1 continue:")
    if option == "1":
        driver.close()
        select_languages()
    elif option == "0":
        driver.close()
        os.close(0)
    else:
        print("We don't have this selection!!\n"
              "Please choose again!!")
        time.sleep(3)
        menu(driver)


if __name__ == '__main__':
    select_languages()
