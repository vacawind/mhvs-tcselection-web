from flask import Flask
from flask import render_template
from flask import request

# 建立app物件,設定靜態檔案的路徑
app = Flask(__name__,
            static_folder='public',
            static_url_path='/public'
            )


# 讀取檔案
def read_file():
    teachers = {}
    with open('teachers_info.csv', 'r', encoding='utf-8') as f:
        for line in f:
            data = line.strip().split(',')
            sub_teachers = {}
            if '科別' in line:
                continue
            sub_teachers['name'] = data[3]
            sub_teachers['identity'] = data[2]
            sub_teachers['score'] = data[7]
            teachers[data[1]] = sub_teachers
    return teachers


teachers = read_file()
print(teachers)


# 使用GET方法, 處理路徑 '/'
@app.route('/')
def home():
    return render_template('home.html')


# 使用POST方法, 處理路徑 '/confirm'
@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form['name'].strip().upper()
    registration = request.form['registration'].strip().upper()
    identity = request.form['identity'].strip().upper()

    try:
        if identity == teachers[registration]['identity'] and name == teachers[registration]['name']:
            score = teachers[registration]['score']
            result = {'准考證號碼': registration,
                      '姓名': name,
                      '總分數': score,
                      }
            return render_template('teacher_info.html', result=result)
        else:
            return render_template('error_info.html')
    except KeyError:
        print('KeyError happened!!')
        return render_template('error_info.html')


if __name__ == "__main__":  # 當user載入SDK時, 有需要才執行, 而不是一載入就執行程式
    app.run()  # 立刻啟動伺服器
