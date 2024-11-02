import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# 讀取 Excel 文件
df = pd.read_excel('九周年資料.xlsx', sheet_name='九宮格核實表')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']  # 獲取用戶輸入的電子信箱

    # 根據電子信箱篩選數據
    email_data = df[df['會員電子信箱'] == email]

    if not email_data.empty:  # 檢查是否找到符合條件的數據
        # 獲取會員名稱和已完成線數
        member_name = email_data.iloc[0]['會員名稱']
        completed_lines = email_data.iloc[0]['完成數量']

        # 九宮格圖片路徑設置，按 A1 B1 C1 排列
        grid_positions = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        images = []

        for pos in grid_positions:
            # 原始圖片路徑和有 "f" 的圖片路徑
            original_image = f"{pos}.svg"
            altered_image = f"{pos}f.svg"

            # 判斷是否為 'O' 或 'X'，選擇相應圖片
            if email_data.iloc[0][pos] == 'O':
                images.append(altered_image)  # 用 f 的圖片
            else:
                images.append(original_image)  # 用原始圖片

        # 將 images 分成三行（每行包含三個圖片）
        images_grid = [images[i:i + 3] for i in range(0, len(images), 3)]

        return render_template('success.html', member_name=member_name, completed_lines=completed_lines, images=images_grid)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
