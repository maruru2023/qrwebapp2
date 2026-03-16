# QRコード生成ツール（Render公開対応）

Flaskで作ったシンプルなQRコード生成Webアプリです。  
入力テキストからQRコードPNGを生成して表示・ダウンロードできます。

外部ライブラリは以下のみ使用しています。

- Flask
- qrcode
- Pillow

画像はファイル保存せず **インメモリ生成（BytesIO）** しています。

---

# ローカル実行

## 仮想環境作成

Mac / Linux

```bash
python -m venv env
source env/bin/activate
