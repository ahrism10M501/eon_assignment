import dataset
import yaml
from typing import Tuple
import numpy as np

class Distance:
    @staticmethod
    def euclidean(p1, p2):
        # (p1 - p2).shape (1500, 3, 2)
        # print(np.sqrt(np.sum((p1 - p2)**2, axis=2)).shape) # 1500, 3
        # print(np.sqrt(np.sum((p1 - p2)**2, axis=2))[:5]) # dim=1에 각 k에 대한 거리 결과 들어감
        return np.sqrt(np.sum((p1 - p2)**2, axis=2))
    
    @staticmethod
    def manhattan(p1, p2):
        return np.sum(np.abs(p1-p2), axis=2)
    
    @staticmethod    
    def cosine(p1, p2):
        return np.dot(p1, p2) / np.linalg.norm(p1)*np.linalg.norm(p2)
    
def _calc_distances(ds, cent, dist_fn, k, threshold):
    while True:
        # 중앙값(cent)와 포인트 간의 거리 구하기
        # 브로드 캐스팅 이용! -> 제대로 이해하기
        distance = dist_fn(ds[:, np. newaxis, :], cent[np.newaxis, :, :])
        # (1500, 1, 2) <> (1, 3, 2) => (1500, 3) 왜냐하면 한번 3차원에 대해 덧셈 수행 혹은 dot product
        # 그러고 보니, 이 함수를 지나고서도 왜 1500, 2 쉐잎이지?
        
        # 제일 작은 값들의 인덱스 찾아주고, 새로운 k를 위한 공간 만들기
        k_label = np.argmin(distance, axis=1)
        # print(k_label.shape)
        # print(k_label[:10])
        new_cent = np.zeros_like(cent)
        
        # 각 k 군집에 따른 평균 구하기 -> 새로운 센터
        for i in range(k):
            new_cent[i] = np.mean(ds[k_label==i], axis = 0)
            
        # 수렴
        if np.all(np.abs(new_cent - cent) < threshold):
            break
        cent = new_cent
        
    return (ds, k_label)
    
def k_means(ds:np.ndarray, dist_fn, k, threshold=0.001):
    # ds.shape = [1500, 2] -> [n_samples, 2(x, y)]
    # 랜덤 센터 뽑기
    rand_idx = np.random.choice(ds.shape[0], k)
    centroid = ds[rand_idx, :] # (3, 2)
    
    # 각 센터에 대한 거리 구하기
    points, labels = _calc_distances(ds, centroid, dist_fn, k, threshold) 
    return (points, labels)

def main():
    np.random.seed(2025)
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    # 데이터셋 만들고~
    factory = dataset.MakeDataset(config["n_samples"], config["noise"])
    ds = factory.make("blobs")
    points, _ = ds.making()
    # Tuple[np.ndarray, np.ndarray] = ([n_samples, 2(x, y)], [1500, 0])

    dist = Distance.euclidean
    point, label = k_means(points, dist, 3)
    # point -> Tuple[n_samples, [x, y, k]]
    datasets_to_plot = []
    datasets_to_plot.append(("blobs", point, label))
    dataset.visualization2D(datasets_to_plot, visual_param=config['visual'])
    
if __name__ == "__main__":
    main()