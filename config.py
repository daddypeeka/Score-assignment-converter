# 配置常量
import os

# Flask基础配置
<<<<<<< HEAD
SECRET_KEY = ''  # 用于flash提示
=======
SECRET_KEY = 'score_assignment_123456'  # 用于flash提示
>>>>>>> e5c004d79f6aee8c916f1daf73fc1f4106d64648
MAX_CONTENT_LENGTH = 10 * 1024 * 1024    # 上传文件大小限制：10MB
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}     # 允许的文件格式

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# 文件名前缀（仅用于下载）
DEFAULT_FILENAME_PREFIX = 'Result'
