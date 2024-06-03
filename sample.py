import json
import numpy as np
import scipy.stats as stats

# JSON data (as a string for example)
json_data = '''
{
    "numOfAgents": 30000,
    "ageDistribution": {
        "description": "distribution of age in pedestrians",
        "distribution": {
            "normal": {
                "description": "normal distribution",
                "samples": "numOfAgents",
                "numberOfValues": 100,
                "minValue": 5,
                "maxValue": 104
            }
        }
    }
}
'''

# Parse JSON data
data = json.loads(json_data)
num_of_agents = data['numOfAgents']
age_dist = data['ageDistribution']['distribution']['normal']

# Get parameters from the JSON data
k = age_dist['numberOfValues']
min_value = age_dist['minValue']
max_value = age_dist['maxValue']

# Sinh ra ngẫu nhiên các giá trị của mẫu tuân theo phân bố chuẩn
mean = (min_value + max_value) / 2  # Trung bình của phân bố chuẩn
std = (max_value - min_value) / 6  # Độ lệch chuẩn của phân bố chuẩn
sample = np.random.normal(mean, std, num_of_agents)  # Mẫu dữ liệu tuân theo phân bố chuẩn
sample = np.clip(sample, min_value, max_value)  # Cắt bớt các giá trị ngoài khoảng [min_value, max_value]
sample = np.round(sample, 1)

# Tính toán giá trị p_value để kiểm tra xem mẫu dữ liệu có phải là phân bố chuẩn hay không
stat, p_value = stats.kstest(sample, 'norm', args=(mean, std))  # Tính toán giá trị thống kê và giá trị p_value

# In ra giá trị p_value
print("Giá trị p_value là: ", p_value)

# Đặt mức ý nghĩa thống kê (significance level) là 0.05
alpha = 0.05  # Mức ý nghĩa thống kê
if p_value < alpha:
    print("Mẫu dữ liệu không tuân theo phân bố chuẩn")
else:
    print("Mẫu dữ liệu tuân theo phân bố chuẩn")
    # In ra mẫu dữ liệu
    print("Mẫu dữ liệu tuân theo phân bố chuẩn là: ")
    print(sample)

    print("Giá trị cực tiểu là: ", np.min(sample))
    print("Giá trị cực đại là: ", np.max(sample))
