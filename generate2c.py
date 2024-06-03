import numpy as np
import scipy.stats as stats
import json

def generate_normal_distribution(samples, minValue, maxValue):
    mean = (minValue + maxValue) / 2
    std = (maxValue - minValue) / 6
    sample = np.random.normal(mean, std, samples)
    sample = np.clip(sample, minValue, maxValue)
    sample = np.round(sample, 1)
    
    stat, p_value = stats.kstest(sample, 'norm', args=(mean, std))
    alpha = 0.05
    if p_value < alpha:
        print(f"Mẫu dữ liệu không tuân theo phân bố chuẩn")
    else:
        print(f"Mẫu dữ liệu tuân theo phân bố chuẩn")
        print("Mẫu dữ liệu tuân theo phân bố chuẩn là: ")
    print(sample)

    print("Gia tri cuc tieu la: ")
    print(np.min(sample))

    print("Gia tri cuc dai la: ")
    print(np.max(sample))

    
    return sample

def main():
    numOfAgents = 30000
    minValue_time = 100
    maxValue_time = 3600
    minValue_age = 5
    maxValue_age = 104

    time_samples = generate_normal_distribution(20, minValue_time, maxValue_time)
    age_samples = generate_normal_distribution(numOfAgents, minValue_age, maxValue_age)

    data = {
        "ageDistribution": {
            "description": "distribution of age in pedestrians",
            "distribution": {
                "normal": {
                    "description": "normal distribution",
                    "samples": numOfAgents,
                    "numberOfValues": 100,
                    "minValue": minValue_age,
                    "maxValue": maxValue_age,
                    "sampleData": age_samples.tolist()
                }
            }
        }
    }

    with open('output2c.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON data has been written to output.json")

if __name__ == "__main__":
    main()
