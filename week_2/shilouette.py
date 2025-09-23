import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
from week_1 import dataset
import yaml
from week_1.k_means import k_means, Distance

import matplotlib.pyplot as plt

class Silhouette:
    @staticmethod
    def getSilhouette(data, dist_fn, labels):
        silhouette = []
        label = np.unique(labels)
        
        for idx in range(len(data)):
            _label = labels[idx]
            # a(i), 내 군집과 나의 평균 거리
            # 조건을 만족하는 인덱스 찾기
            A_cluster = np.where(labels == _label)[0]
            if len(A_cluster) <= 1:
                a_i = 0.0
            else:
                a_distance = dist_fn(
                    data[idx][np.newaxis, np.newaxis, :], # (1,1,2)( , , [x, y])
                    data[A_cluster][np.newaxis, :, :] # (1, 1500, 2)( , [[x, y] * 1500])
                )
                a_i = np.sum(a_distance) / (len(A_cluster)-1)
                
            # b(i), 가장 가까운 다른 군집과 나의 평균 거리
            b_i = np.inf
            C_labels = label[label != _label]
            for C_label in C_labels:
                C_Cluster = np.where(labels == C_label)[0]
                b_distance = dist_fn(
                    data[idx][np.newaxis, np.newaxis, :],
                    data[C_Cluster][np.newaxis, :, :]
                )
                avg_distance = np.mean(b_distance)
                if avg_distance < b_i:
                    b_i = avg_distance
                
            # s(i), silhouette score
            if max(a_i, b_i) == 0:
                s_i = 0.0
            else:
                s_i = (b_i - a_i) / max(a_i, b_i)
            
            silhouette.append(s_i)
            
        return np.array(silhouette)
            
def getWidth(data, Z=1.96):
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    margin = Z * (std/np.sqrt(n))
    lower = mean - margin
    upper = mean + margin
    
    return (lower, upper)
        
def main():
    np.random.seed(2025)
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    factory = dataset.MakeDataset(config["n_samples"], config["noise"])
    ds = factory.make("blobs")
    points, _ = ds.making()
    # Tuple[np.ndarray, np.ndarray] = ([n_samples, 2(x, y)], [1500, 0])

    dist = Distance.euclidean
    point, label, _ = k_means(points, dist, 10)
    silhouette = Silhouette.getSilhouette(point, dist, label)
    
    # 잼미나이야!!! 도와줘ㅓㅓㅓ
    cluster_means = []
    widths = []
    for k in np.unique(label):
        mean = np.mean(silhouette[label==k])
        low_margin, up_margin = getWidth(silhouette[label==k], 1.96)
        cluster_means.append(mean)
        widths.append([mean-low_margin, up_margin-mean])
        
    errors = np.array(widths).T
    plt.figure()
    plt.bar(np.unique(label), cluster_means, yerr=errors, capsize=5, color='skyblue', edgecolor='black')
    plt.axhline(np.mean(silhouette), color='red', linestyle='--', label='Whole mean of clueters')
    plt.xlabel('K')
    plt.ylabel('avg_silhouette')
    plt.title('width with each clusters')
    plt.xticks(np.unique(label))
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    
if __name__ == "__main__":
    main()