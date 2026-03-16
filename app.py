import os
import io
import base64
from flask import Flask, request, render_template
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

app = Flask(__name__)

MAX_TEXT_LENGTH = 500
MAX_SIZE = 1024

ERROR_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def create_qr(text, size, border, error_level):
    qr = qrcode.QRCode(
        error_correction=ERROR_LEVELS.get(error_level, ERROR_CORRECT_M),
        border=border,
        box_size=10,
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    size = 300
    border = 4
    error_level = "M"
    image_data_url = ""
    error_message = ""

    if request.method == "POST":
        try:
            text = request.form.get("text", "").strip()
            size = int(request.form.get("size", 300))
            border = int(request.form.get("border", 4))
            error_level = request.form.get("error_level", "M")

            if not text:
                raise ValueError("テキストを入力してください")

            if len(text) > MAX_TEXT_LENGTH:
                raise ValueError("文字数は500以内にしてください")

            if size < 100 or size > MAX_SIZE:
                raise ValueError("サイズは100〜1024pxで指定してください")

            if border < 0 or border > 20:
                raise ValueError("余白は0〜20で指定してください")

            if error_level not in ERROR_LEVELS:
                raise ValueError("誤り訂正レベルは L / M / Q / H のいずれかを指定してください")

            img_bytes = create_qr(text, size, border, error_level)
            b64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
            image_data_url = f"data:image/png;base64,{b64}"

        except ValueError as e:
            error_message = str(e)
        except Exception:
            error_message = "QRコード生成中にエラーが発生しました"

    return render_template(
        "index.html",
        text=text,
        size=size,
        border=border,
        error_level=error_level,
        image_data_url=image_data_url,
        error_message=error_message,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)