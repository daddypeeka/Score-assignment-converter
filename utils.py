import time
from config import DEFAULT_FILENAME_PREFIX

def generate_unique_filename():
    """
    生成唯一的输出文件名（避免重复）
    格式：赋分结果表_20260102_153045.xlsx
    :return: 空字符串（无路径）, 文件名
    """
    # 时间戳（年月日_时分秒）
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    filename = f'{DEFAULT_FILENAME_PREFIX}_{timestamp}.xlsx'
    return "", filename
