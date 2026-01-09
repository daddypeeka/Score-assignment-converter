from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import io
import config
from score_processor import load_tables, process_assignment, save_to_bytes
from utils import generate_unique_filename

# 初始化Flask应用
app = Flask(__name__, 
            template_folder=config.TEMPLATE_DIR,
            static_folder=config.STATIC_DIR)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """首页：上传文件 + 选择配置 + 生成下载文件"""

    if request.method == 'POST':
        # 1. 检查文件是否上传
        if 'original_file' not in request.files or 'score_file' not in request.files:
            flash('请上传原始分数表和赋分表！', 'error')
            return redirect(request.url)
        
        original_file = request.files['original_file']
        score_file = request.files['score_file']
        
        # 2. 检查文件是否为空
        if original_file.filename == '' or score_file.filename == '':
            flash('文件不能为空！', 'error')
            return redirect(request.url)
        
        # 3. 检查文件格式
        if not (allowed_file(original_file.filename) and allowed_file(score_file.filename)):
            flash(f'仅支持{",".join(config.ALLOWED_EXTENSIONS)}格式文件！', 'error')
            return redirect(request.url)
        
        # 4. 处理表格并生成下载文件
        try:
            df_original, df_score = load_tables(original_file, score_file)
            
            insert_position = request.form.get('insert_position', 'after_subject')
            
            df_result = process_assignment(df_original, df_score, insert_position)
            
            _, filename = generate_unique_filename()
            
            file_bytes = save_to_bytes(df_result)
            
            return send_file(
                io.BytesIO(file_bytes),
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
                
        except Exception as e:
            flash(f'处理失败：{str(e)}', 'error')
            return redirect(request.url)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)