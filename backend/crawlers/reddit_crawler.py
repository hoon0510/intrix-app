from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from typing import List, Dict, Optional

class RedditCrawler:
    def __init__(self, headless: bool = True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def scroll_and_collect(self, max_scroll: int = 10) -> List[Dict[str, str]]:
        """스크롤을 내리면서 게시물을 수집합니다."""
        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        retries = 0

        for _ in range(max_scroll):
            # 스크롤 다운
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 콘텐츠 로딩을 위한 대기

            try:
                # 새로운 콘텐츠가 로드되었는지 확인
                self.wait.until(
                    lambda d: d.execute_script("return document.body.scrollHeight") != last_height
                )
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                retries = 0

                # 현재 보이는 게시물 수집
                current_posts = self._collect_visible_posts()
                posts.extend(current_posts)

            except TimeoutException:
                retries += 1
                if retries >= 3:
                    print("최대 재시도 횟수 도달. 크롤링을 종료합니다.")
                    break

        return posts

    def _collect_visible_posts(self) -> List[Dict[str, str]]:
        """현재 보이는 게시물들을 수집합니다."""
        posts = []
        post_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='post-container']")
        
        for post in post_elements:
            try:
                title = post.find_element(By.CSS_SELECTOR, "h3").text
                content = post.find_element(By.CSS_SELECTOR, "div[data-testid='post-content']").text
                posts.append({
                    "title": title,
                    "content": content
                })
            except Exception as e:
                print(f"게시물 수집 중 오류 발생: {e}")
                continue

        return posts

    def search(self, keyword: str, max_posts: int = 50) -> List[Dict[str, str]]:
        """키워드로 Reddit을 검색하고 결과를 수집합니다."""
        try:
            search_url = f"https://www.reddit.com/search/?q={keyword}"
            self.driver.get(search_url)
            
            # 초기 로딩 대기
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='post-container']"))
            )
            
            return self.scroll_and_collect(max_scroll=max_posts//5)
            
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return []
        finally:
            self.driver.quit()

    def __del__(self):
        """크롤러 종료 시 드라이버 정리"""
        if hasattr(self, 'driver'):
            self.driver.quit() 