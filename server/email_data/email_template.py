def generate_gdg_cm_email(name, coupon1, coupon2):
    email_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Template</title>
        <style>
            body {{
                font-family: "Noto Sans Kr", sans-serif;
                color: #202124;
                margin: 0;
                padding: 0;
            }}
            
            .bold {{
                font-size: 20px;
                font-weight: 700;
            }}
            
            .container {{
                margin: 0 auto;
                margin-top: 20px;
                text-align: left;
                width: 624px;
                padding: 20px;
                background-color: #fafafa;
            }}
            
            .header img, .footer img {{
                width: 100%;
                height: auto;
            }}
            
            .content {{
                padding: 24px;
                line-height: 1.6;
            }}

            .content p {{
                margin-bottom: 16px;
            }}
            
            .footer {{
                background-color: #eead3c;
                padding: 18px;
                text-align: center;
            }}

            .footer img {{
                width: 94px;
                height: auto;
            }}     

            .signature {{
                margin: 20px;
                padding: 12px;
                width: 230px;
            }}

            .signature p {{
                font-size: 14px;
                margin: 4px 0;
            }}

            .signature .name {{
                font-size: 16px;
                font-weight: bold;
            }}

            .signature .affiliation {{
                color: rgb(95,99,104);
            }}

            .signature a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            .signature .email span {{
                font-weight: bold;
            }}

            .signature .email a {{
                font-size: 12px;
                font-weight: 700;
            }}

            .signature img {{
                margin-top: 16px;
                width: 232px;
                height: auto;
            }}

            a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://i.ibb.co/FsvyVSL/GDG-Email-Signature.png" alt="Header" />
            </div>

            <div class="content">
                <p class="bold">🎉 {name}님께,</p>
                <p>Core Member으로서, GDG on Campus Kangnam University에 누구보다 먼저 관심을 가져주시고 운영진으로서 함께 열심히 오픈 준비를 해주셔서 감사합니다.</p>
                <p>GDG Kangnam University는 이번이 첫 번째 기수로서 2024년 9월 19일부터 활동을 시작하게 되었습니다.</p>
                <p>그러다보니 첫 번째 기수로서 부족한 체계속에서 누구보다 더 많은 일을 해야했고 여러 난관이 많았지만, Core Member 모두가 밤낮 가리지 않고 활동을 열심히 해주셔서 처음 생각했던 것 보다 훨씬 대단한 커뮤니티가 만들어져가고 있는 것 같아요.</p>
                <p>그 과정속에서 언제나 {name}님이 열정적으로 작업하시던 모습은 잊지 못할 것 같습니다.</p>
                <p>GDG의 첫번째 팬에게 보내는 선물이자, 같이 일하는 동료에게 감사한 마음으로 7,000원 쿠폰과 함께 편지로나마 고마운 말을 전하고자 합니다.</p>
                <p>분명히 저 스스로도 그렇고 GDG 활동에서도 여러 체계가 부족한 부분이 많다고 느끼실 수도 있지만, 언제든지 열린 마음으로 함께 개선해 나갈 수 있도록 하겠습니다.</p>

                <p>앞으로도 많은 활동 부탁드리며, 함께 즐겁게 커뮤니티를 만들어 나갈 수 있기를 기대합니다.</p>

                <p>감사합니다.</p>
                
                <br />
                <a href="https://discord.gg/UFaJc7cxYg" target="_blank">아직 디스코드에 참여하지 않은 분들이 있어요! [ 클릭 ]</a>
                <br />
                <a href="https://gdg-kangnam.notion.site/" target="_blank">GDG 홈페이지 바로가기</a>
                <br />
                <p>쿠폰번호: {coupon1}</p>
                <p>쿠폰번호: {coupon2}</p>
            </div>

            <div class="footer">
                <img src="https://i.ibb.co/5r1k6Ft/gdg-footer.png" alt="Footer" />
            </div>
        </div>

        <div class="signature">
            <p class="name">Hongki Shin</p>
            <p class="affiliation">GDG on Campus Kangnam University</p>
            <p class="position">Co Lead</p>
            <p class="email">
                <span>E&nbsp;</span>
                <a href="mailto:hin6150@gmail.com">hin6150@gmail.com</a>
            </p>
            <p class="affiliation">gdg-kangnam.notion.site</p>

            <img src="https://i.ibb.co/d79TgZn/gdg.png" alt="Logo">
        </div>
    </body>
    </html>
    """
    return email_template


def get_notification_email_template(name, coupon):
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
                margin: 0;
                padding: 0;
            }}
            
            .bold {{
                font-size: 20px;
                font-weight: 700;
            }}
            
            .container {{
                margin: 0 auto;
                text-align: left;
                width: 624px;
                padding: 20px;
                background-color: #fafafa;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            
            .header img, .footer img {{
                width: 100%;
                height: auto;
            }}
            
            .content {{
                padding: 24px;
                line-height: 1.6;
            }}

            .content p {{
                margin-bottom: 16px;
            }}
            
            .footer {{
                background-color: #eead3c;
                padding: 18px;
                text-align: center;
            }}

            .footer img {{
                width: 94px;
                height: auto;
            }}     

            .signature {{
                margin: 20px;
                padding: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: #ffffff;
                width:230px;
            }}

            .signature p {{
                color: rgb(30,50,61);
                font-size: 14px;
                font-family: Arial, sans-serif;
                margin: 4px 0;
            }}

            .signature .name {{
                font-size: 16px;
                font-weight: bold;
            }}

            .signature .affiliation {{
                color: rgb(95,99,104);
            }}

            .signature a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            .signature .email span {{
                font-weight: bold;
            }}

            .signature .email a {{
                font-size: 12px;
                font-weight: 700;
            }}

            .signature img {{
                margin-top: 16px;
                width: 232px;
                height: auto;
            }}

            a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://i.ibb.co/FsvyVSL/GDG-Email-Signature.png" alt="Header" />
            </div>

            <div class="content">
                <p class="bold">🎉 {name}님께,</p>
                <p>GDG on Campus Kangnam University에 관심을 가져주시고 오랜 시간 기다려주셔서 감사합니다.</p>
                <p>GDG Kangnam University는 이번이 첫 번째 기수로서 2024년 9월 19일부터 활동을 시작하게 되었습니다.</p>
                <p>현재 Google에서 GDSC에서 GDG on Campus로의 변화를 준비하고 있어, 저희도 이에 맞춰 활동 시작이 지연된 점 사과드립니다.</p>

                <p>감사의 마음을 담아, GDG on Campus Kangnam University에서는 사전 알림 신청자에 한해 가입비 5,000원 쿠폰을 발급해 드리고자 합니다.</p>
                <p>앞으로도 많은 관심 부탁드리며, 커뮤니티에서 뵐 수 있기를 기대합니다.</p>

                <p>감사합니다.</p>
                
                <br />
                <a href="https://forms.gle/6K9djkTwkjVxbiXG8" target="_blank">가입신청 폼 바로가기</a>
                <br />
                <a href="https://gdg-kangnam.notion.site/" target="_blank">GDG 홈페이지 바로가기</a>
                <br />
                <p>쿠폰번호: {coupon}</p>
            </div>

            <div class="footer">
                <img src="https://i.ibb.co/5r1k6Ft/gdg-footer.png" alt="Footer" />
            </div>
        </div>

        <div class="signature">
            <p class="name">EunHyeok Jung</p>
            <p class="affiliation">GDG on Campus Kangnam University</p>
            <p class="position">Lead</p>
            <p class="email">
                <span>E&nbsp;</span>
                <a href="mailto:silverhyeok.dev@gmail.com">silverhyeok.dev@gmail.com</a>
            </p>
            <p class="affiliation">gdg-kangnam.notion.site</p>

            <img src="https://i.ibb.co/d79TgZn/gdg.png" alt="Logo">
        </div>
    </body>
    </html>
    """

def generate_gdg_welcome_email(name, coupon):
    email_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GDG 환영 이메일</title>
        <style>
            body {{
                font-family: "Noto Sans Kr", sans-serif;
                color: #202124;
                margin: 0;
                padding: 0;
            }}
            
            .bold {{
                font-size: 20px;
                font-weight: 700;
            }}
            
            .container {{
                margin: 0 auto;
                margin-top: 20px;
                text-align: left;
                width: 624px;
                padding: 20px;
                background-color: #fafafa;
            }}
            
            .header img, .footer img {{
                width: 100%;
                height: auto;
            }}
            
            .content {{
                padding: 24px;
                line-height: 1.6;
            }}

            .content p {{
                margin-bottom: 16px;
            }}
            
            .footer {{
                background-color: #eead3c;
                padding: 18px;
                text-align: center;
            }}

            .footer img {{
                width: 94px;
                height: auto;
            }}     

            .signature {{
                margin: 20px;
                padding: 12px;
                width: 230px;
            }}

            .signature p {{
                color: rgb(30,50,61);
                font-size: 14px;
                font-family: Arial, sans-serif;
                margin: 4px 0;
            }}

            .signature .name {{
                font-size: 16px;
                font-weight: bold;
            }}

            .signature .affiliation {{
                color: rgb(95,99,104);
            }}

            .signature a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            .signature .email span {{
                font-weight: bold;
            }}

            .signature .email a {{
                font-size: 12px;
                font-weight: 700;
            }}

            .signature img {{
                margin-top: 16px;
                width: 232px;
                height: auto;
            }}

            a {{
                color: #1155cc;
                font-weight: 700;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://i.ibb.co/FsvyVSL/GDG-Email-Signature.png" alt="Header" />
            </div>

            <div class="content">
                <p class="bold">🎉 {name}님께,</p>
                <p>GDG on Campus Kangnam University에 오신 것을 환영합니다!</p>
                <p>GDG Kangnam University는 이번이 첫 번째 기수로서 2024년 9월 19일부터 활동을 시작하게 되었습니다.</p>
                <p>저희는 GDG on Campus라는 커뮤니티를 통해 강남대학교를 넘어 더 많은 사람들과 소통할 수 있는 공간을 만들고자 합니다.</p>

                <p>학과, 나이, 실력에 상관없이 누구나 자유롭게 참여할 수 있으며, 다양한 프로그램과 이벤트를 통해 회원들이 IT와 관련된 여러 기회를 접하고 함께 성장할 수 있는 공간을 꿈꾸고 있습니다.</p>
                <p>몇몇 사람들은 이를 불가능하다고 생각했을 수도 있지만, 많은 분들의 관심과 참여 덕분에 이렇게 활동을 시작할 수 있었습니다.</p>

                <p>저희의 노력이 인연으로서 {name}님께 닿게 되어 매우 감사하게 생각합니다.</p>
                <p>{name}님께서 커뮤니티 활동을 하시면서 불편함 없이 즐겁게 활동하실 수 있도록 최선을 다하겠습니다.</p>

                <p>앞으로도 많은 관심 부탁드리며, 커뮤니티에서 열정적으로 활동하시는 {name}님을 뵙기를 기대합니다.</p>
                <p>감사합니다.</p>

                <a href="https://discord.gg/UFaJc7cxYg" target="_blank">GDG 디스코드 바로가기</a>
                <br />
                <a href="https://gdg-kangnam.notion.site/" target="_blank">GDG 홈페이지 바로가기</a>
                
                <br />
                <br />
                <br />

                <p>추신. 감사한 마음을 담아 5,000원 가입비 쿠폰을 보내드리고 있습니다. 주변에 GDG를 추천해주세요!</p>
                <p>추신2. 활동 중 어려움이 있으시다면 gdg.kangnam@gmail.com나 디스코드 등을 통해 운영진에게 연락해주세요!</p>            

                <br />
                <p>쿠폰번호: {coupon}</p>
            </div>

            <div class="footer">
                <img src="https://i.ibb.co/5r1k6Ft/gdg-footer.png" alt="Footer" />
            </div>
        </div>

        <div class="signature">
            <p class="name">EunHyeok Jung</p>
            <p class="affiliation">GDG on Campus Kangnam University</p>
            <p class="position">Lead</p>
            <p class="email">
                <span>E&nbsp;</span>
                <a href="mailto:silverhyeok.dev@gmail.com">silverhyeok.dev@gmail.com</a>
            </p>
            <p class="affiliation">gdg-kangnam.notion.site</p>

            <img src="https://i.ibb.co/d79TgZn/gdg.png" alt="Logo">
        </div>
    </body>
    </html>
    """
    return email_template
