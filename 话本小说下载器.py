from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# 中文数字转换
def to_chinese_numeral(num):
    numerals = "零一二三四五六七八九"
    units = ["", "十", "百", "千", "万"]
    if num < 10:
        return numerals[num]
    digits = list(map(int, str(num)))
    chinese = ""
    length = len(digits)
    for i, digit in enumerate(digits):
        if digit != 0:
            chinese += numerals[digit] + units[length - i - 1]
        elif chinese and not chinese.endswith("零"):
            chinese += "零"
    return chinese.rstrip("零").replace("一十", "十")

# 生成章节标题
def generate_chapter_title(chapter_title, current_counter, extra_counter):
    """根据章节内容生成正确的标题"""
    if re.match(r"^第[一二三四五六七八九十百千万零]+章", chapter_title):
        extra_counter = 1
        return chapter_title, current_counter, extra_counter  # 已包含编号
    elif re.match(r"^第[1234567890]+章", chapter_title):
        extra_counter = 1
        return chapter_title, current_counter, extra_counter  # 已包含编号
    elif "番外" in chapter_title:
        new_title = f"第{to_chinese_numeral(current_counter)}点{to_chinese_numeral(extra_counter)}章 {chapter_title}"
        extra_counter += 1
        return new_title, current_counter, extra_counter
    else:
        new_title = f"第{to_chinese_numeral(current_counter)}章 {chapter_title}"
        extra_counter = 1
        current_counter += 1
        return new_title, current_counter, extra_counter

# 输入小说的第一章链接
url_link_ch1 = input("输入小说的第一章链接： ")

# 初始化浏览器
driver = webdriver.Firefox()

# 打开目标页面
driver.get(url_link_ch1)

# 创建一个以书名和作者命名的txt文件，准备写入章节内容
try:
    # 提取书名和作者
    book_title = driver.find_element(By.CSS_SELECTOR, "li a.text-lightgrey").text.strip()  # 书名
    author = driver.find_elements(By.CSS_SELECTOR, "li a.text-lightgrey")[1].text.strip()  # 作者

    # 生成文件名
    file_name = f"{book_title}({author}).txt"

    # 初始化章节和番外计数器
    chapter_counter = 1
    extra_counter = 1

    with open(file_name, "w", encoding="utf-8") as file:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.dp"))
            )

            while True:
                # 获取章节标题
                try:
                    chapter_title = driver.find_element(By.CSS_SELECTOR, "div#chaptertitle h1").text.strip()
                    chapter_title, chapter_counter, extra_counter = generate_chapter_title(chapter_title, chapter_counter, extra_counter)
                    file.write(f"{chapter_title}\n\n")
                    print(f"章节标题: {chapter_title}")
                except Exception as e:
                    print("获取章节标题时出现异常:", e)

                # 检测到“看视频恢复阅读体力”按钮
                try:
                    exhaustion_message = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '您的阅读体力值已经用完')]"))
                    )
                    current_url = driver.current_url
                    print(f"当前页面的链接是: {current_url}")

                    driver.quit()
                    time.sleep(2)
                    driver = webdriver.Firefox()
                    driver.get(current_url)
                    print("页面已重新加载")
                    time.sleep(5)

                except Exception as e:
                    print("\n\n")

                # 获取章节内容
                quotes = driver.find_elements(By.CSS_SELECTOR, "p.dp")
                for q in quotes:
                    text = q.text.strip()
                    file.write(text + "\n\n")

                # 获取评论内容
                try:
                    comments = driver.find_elements(By.CSS_SELECTOR, "div.talkcontent")
                    for comment in comments:
                        author_name = comment.find_element(By.CSS_SELECTOR, "div.name span").text.strip()
                        message = comment.find_element(By.CSS_SELECTOR, "p").text.strip()
                        if author_name and message:
                            comment_text = f"{author_name}：{message}"
                            file.write(comment_text + "\n\n")
                except Exception as e:
                    print("获取评论内容时出现异常:", e)

                # 尝试查找“下一章”按钮
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[span[text()=' 下一章']]"))
                    )
                    next_button.click()
                    time.sleep(2)
                except Exception as e:
                    print("没有下一章了，或出现异常:", e)
                    break
        finally:
            print("End")
            driver.quit()

except Exception as e:
    print("提取书名或作者时出现异常:", e)
    driver.quit()
