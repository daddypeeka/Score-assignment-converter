import pandas as pd
import random
import string
from faker import Faker
import time  # 新增：用于时间戳，强化文件名唯一性

# 初始化Faker（生成中文姓名）
fake = Faker('zh_CN')
# 移除固定种子，让每次生成的随机数不同
# Faker.seed(42)  # 如需复现数据，可取消注释
# random.seed(42)  # 如需复现数据，可取消注释

# 配置项
SUBJECTS = ['物理', '化学', '生物', '政治', '历史', '地理', '技术']  # 科目列表
STUDENT_COUNT = 50  # 生成学生数量
SCORE_RANGES = {
    '差': (0, 40),
    '中': (40, 80),
    '好': (80, 100)
}  # 成绩区间

def generate_random_string(length=8):
    """生成随机字符串（数字+时间戳后缀，确保唯一性）"""
    # 基础随机数字符串
    random_num = ''.join(str(random.randint(0, 9)) for _ in range(length))
    # 加入时间戳（毫秒级），彻底避免重复
    timestamp = str(int(time.time() * 1000))[-4:]  # 取时间戳最后4位
    return f"{random_num}{timestamp}"

def generate_student_scores():
    """生成单个学生的成绩数据"""
    # 随机选3门科目
    selected_subjects = random.sample(SUBJECTS, 3)
    
    # 初始化所有科目成绩为空
    score_data = {subject: '' for subject in SUBJECTS}
    score_data['姓名'] = fake.name()
    
    # 为选中的3门科目生成随机成绩（覆盖好/中/差）
    score_levels = random.choices(['差', '中', '好'], k=3)
    for subject, level in zip(selected_subjects, score_levels):
        min_score, max_score = SCORE_RANGES[level]
        score = round(random.uniform(min_score, max_score), 1)  # 保留1位小数
        score_data[subject] = score
    
    return score_data

def generate_test_original_table():
    """生成测试用原始分数表"""
    # 生成所有学生数据
    students_data = [generate_student_scores() for _ in range(STUDENT_COUNT)]
    
    # 转换为DataFrame
    df = pd.DataFrame(students_data)
    
    # 调整列顺序（姓名在前，科目在后）
    col_order = ['姓名'] + SUBJECTS
    df = df[col_order]
    
    # 生成随机文件名（每次不同）
    random_str = generate_random_string()
    filename = f'Original_{random_str}.xlsx'
    
    # 保存为Excel文件
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"测试原始分数表已生成：{filename}")
    return filename

if __name__ == '__main__':
    generate_test_original_table()
