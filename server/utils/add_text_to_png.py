from PIL import Image, ImageDraw, ImageFont

def add_text_to_png(image_path, output_path, text):
    # 이미지 열기
    image = Image.open(image_path)

    # 이미지 위에 그리기 위한 ImageDraw 객체 생성
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("coupon_data/NotoSansKR-Bold.ttf", 22)

    # 텍스트 삽입
    draw.text((413, 348), text, font=font, fill=(0, 0, 0))

    # 결과 이미지 저장
    image.save(output_path)


