def get_email_template(name, discord_link):
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Template</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #202124;
                background-color: #fafafa;
                margin: 0;
                padding: 0;
            }}
            .container {{
                margin: 0 auto;
                text-align: left;
                width: 624px;
            }}
            .header img {{
                width: 100%;
                height: auto;
            }}
            .content {{
                padding: 24px;
                background-color: #fafafa;
            }}
            .highlight {{
                font-family: 'Poppins', sans-serif;
                font-size: 16pt;
                font-weight: 700;
                color: #000;
            }}
            .paragraph {{
                font-size: 12pt;
                line-height: 1.6;
                color: #000;
                margin-bottom: 12px;
            }}
            .footer {{
                background-color: #eead3c;
                padding: 18px;
                text-align: center;
            }}
            .footer img {{
                width: 94px;
                height: 48px;
            }}        
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXdcARY7QnXRi9VfotWl2D0xAHfzXoEUbcuYeJN1J0IqFJ4JaUWFML4PJbHj8pXkmJhqmucGkq3oM9KneooRSds3gXphBwb2Bv8wM2jQ_77a7QrpDYCR9LBiF4kwifF5-jz9mNAZEcKJIZbWu3kNpO7ef1G1XGOGsY0dR1VwtTcgdJ4_NljKnEc?key=Q9oHoM_FdfbYYvumuI-xUQ" alt="Header" />
            </div>
    
            <div class="content">
                <p class="highlight">
                    🎉 {name}님께,
                </p>
                <p class="paragraph">
                    GDG on Campus Kangnam University에 합류하게 된 것을 진심으로 환영드립니다!
                </p>
                <p class="paragraph">
                    저희 커뮤니티에서는 다양한 사람들이 함께 모여 지식을 공유하고, 다양한 기술과 프로젝트를 탐구하며 성장할 수 있는 공간을 만들고 있습니다.
                </p>
                <p class="paragraph">
                    주요 활동은 디스코드에서 진행되며, 여기에서 다양한 이벤트와 소통을 경험할 수 있습니다
                    <a href="{discord_link}" target="_blank" rel="noopener noreferrer">
                        디스코드 링크
                    </a>
                </p>
                <p class="paragraph">
                    다시 한 번, {name}님의 합류를 축하드립니다. 앞으로 GDG에서의 활동을 기대하겠습니다!
                </p>
            </div>
    
            <div class="footer">
                <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXeiWsfPsbtHP4Vi81BhiUIBpUcpcw3RfLqN0mavgdquogHJ9P9ZNfHa8ErFxBea6c6CZqrS7BPq6cKbR8uw_ZjEDp19SoZel7otuPJ7xONu95vOm130K9HSIIVHDWbdTfQAhoaYCPFoer2rTW7rG4Qj3S-Y5z8o5sUwee0heMgXTkuDsO9g9Kw?key=Q9oHoM_FdfbYYvumuI-xUQ" alt="Footer" />
            </div>
        </div>
    </body>
    </html>
    """
