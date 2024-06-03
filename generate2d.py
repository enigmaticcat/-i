import json
import numpy as np
from scipy import stats

# Đọc dữ liệu từ file JSON
with open('/Users/nguyenthithutam/Documents/GitHub/hoangnv-sfm/data/input.json', 'r') as file:
    data = json.load(file)

# Lấy thông tin từ file JSON
walkability = data['walkability']
distribution = walkability['distribution']
num_samples = int(distribution['normal']['samples'])
total_value = 30000  # Đây là giá trị tổng giả định, bạn có thể thay đổi theo nhu cầu
lower_bound = float(distribution['normal']['lowerBound'])
upper_bound = float(distribution['normal']['upperBound'])

# Tính giá trị trung bình và độ lệch chuẩn
mean = total_value / num_samples
std_dev = (mean - lower_bound) / 3  # Giả sử rằng 99.7% dữ liệu nằm trong khoảng 3 độ lệch chuẩn từ giá trị trung bình

# Tạo ra các mẫu ngẫu nhiên tuân theo phân phối chuẩn
samples = np.random.normal(mean, std_dev, num_samples)

# Chuẩn hóa các mẫu sao cho tổng của chúng bằng với total_value
samples = samples * total_value / np.sum(samples)

# Đảm bảo rằng tất cả các mẫu đều nằm trong khoảng từ lower_bound đến upper_bound
samples = np.clip(samples, lower_bound, upper_bound)
samples = np.round(samples, 0)

# Kiểm tra xem liệu các mẫu này có tuân theo phân phối chuẩn không bằng cách sử dụng kiểm định Shapiro-Wilk
stat, p = stats.shapiro(samples)
alpha = 0.05
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("Theo kiểm định Shapiro-Wilk, các mẫu không tuân theo phân phối chuẩn")
else:
    print("Theo kiểm định Shapiro-Wilk, các mẫu có thể tuân theo phân phối chuẩn")

# Kiểm tra xem liệu các mẫu này có tuân theo phân phối chuẩn không bằng cách sử dụng kiểm định Kolmogorov-Smirnov
stat, p = stats.kstest(samples, 'norm')
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("Theo kiểm định Kolmogorov-Smirnov, các mẫu không tuân theo phân phối chuẩn")
else:
    print("Theo kiểm định Kolmogorov-Smirnov, các mẫu có thể tuân theo phân phối chuẩn")

distribution['normal']['samples'] = int(num_samples)
distribution['normal']['sumOfValues'] = int(np.sum(samples))
distribution['normal']['lowerBound'] = int(lower_bound)
distribution['normal']['upperBound'] = int(upper_bound)
distribution['values'] = samples.astype(int).tolist()

# Ghi dữ liệu trở lại file JSON
with open('/Users/nguyenthithutam/Documents/GitHub/hoangnv-sfm/data/input.json', 'w') as file:
    json.dump(data, file, indent=4)

# In ra giá trị của các mẫu và tổng các giá trị
print("Các giá trị của mẫu: ", samples.astype(int))
print("Tổng các giá trị của mẫu: ", np.sum(samples))
