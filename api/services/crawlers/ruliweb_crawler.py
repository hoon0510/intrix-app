from typing import List
from ....utils.text_cleaner import clean_text

async def crawl_ruliweb(input_text: str) -> List[str]:
    # TODO: 실제 크롤링 구현 예정
    # 현재는 테스트용 샘플 데이터 반환
    raw_text = f"[ruliweb] 크롤링 결과 샘플: '{input_text}' <section>HTML 태그 테스트</section> https://bbs.ruliweb.com 🎮"
    return [clean_text(raw_text)] 