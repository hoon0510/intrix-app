def render_report_html(data: dict) -> str:
    """
    분석 결과 데이터를 HTML 형식으로 렌더링합니다.
    
    Args:
        data: 분석 결과 데이터
        
    Returns:
        str: 렌더링된 HTML 문자열
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Intrix 분석 리포트</title>
        <style>
            body {
                font-family: 'Noto Sans KR', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .section {
                margin-bottom: 30px;
            }
            .section-title {
                font-size: 24px;
                font-weight: bold;
                color: #1a73e8;
                margin-bottom: 15px;
            }
            .content {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
            }
            .slogan {
                font-size: 18px;
                font-weight: bold;
                margin: 10px 0;
            }
            .positioning {
                font-style: italic;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Intrix 분석 리포트</h1>
        </div>
        
        <div class="section">
            <h2 class="section-title">전략 요약</h2>
            <div class="content">
                {strategy_summary}
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">슬로건</h2>
            <div class="content">
                {slogans}
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">브랜딩 포지셔닝</h2>
            <div class="content">
                {branding_positioning}
            </div>
        </div>
    </body>
    </html>
    """
    
    # 데이터 포맷팅
    strategy_summary = data.get('strategy', {}).get('summary', '')
    slogans = ''.join([f'<div class="slogan">{slogan}</div>' for slogan in data.get('branding', {}).get('slogans', [])])
    branding_positioning = data.get('branding', {}).get('positioning', '')
    
    # HTML 템플릿에 데이터 삽입
    html = html_template.format(
        strategy_summary=strategy_summary,
        slogans=slogans,
        branding_positioning=branding_positioning
    )
    
    return html 