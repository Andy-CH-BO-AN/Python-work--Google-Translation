from selenium import webdriver
import time


def translation():
    language_dict = \
        {"1": "zh-TW",
         "2": "en-GB",
         "3": "fr-FR",
         "4": "de-DE",
         "5": "es-ES",
         "6": "ru-RU",
         "7": "it-IT",
         "8": "ko-KR",
         "9": "ja-JP", }
    select_language = input("select your language to translate!!\n"
                            "press 1: Chinese\n"
                            "press 2: English\n"
                            "press 3: French\n"
                            "press 4: German\n"
                            "press 5: Spanish\n"
                            "press 6: Russian\n"
                            "press 7: Italian\n"
                            "press 8: Korean\n"
                            "press 9: Japanese\n")
    language = language_dict[f'{select_language}']
    driver = webdriver.Chrome()
    driver.get(f"https://translate.google.com.tw/?hl={language}")

    # 找到輸入框
    element = driver.find_element_by_id("source")

    # 輸入內容
    translated_text = input("Key in the text(make sure your input is correct):")
    element.send_keys(f'{translated_text}')
    time.sleep(0.5)
    result = driver.find_element_by_class_name("tlid-translation,translation").text
    print(result)


if __name__ == '__main__':
    translation()
