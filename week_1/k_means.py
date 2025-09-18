import dataset
import yaml
from typing import Tuple
import numpy as np

class Distance:
    @staticmethod
    def euclidean(p1, p2):
        return np.sqrt(np.sum((p1 - p2)**2, axis=1))
    
    @staticmethod
    def manhattan(p1, p2):
        return np.sum(np.abs(p1-p2), axis=1)
    
    @staticmethod    
    def cosine(p1, p2):
        return np.dot(p1, p2) / np.linalg.norm(p1)*np.linalg.norm(p2)
    
def _calc_distances(ds, cent, dist_fn, k, threshold):
    while True:
        # 중앙값(cent)와 포인트 간의 거리 구하기
        # 브로드 캐스팅 이용! -> 제대로 이해하기
        distance = dist_fn(ds[:, np.newaxis, :], cent[np.newaxis, :, :])
        
        # 제일 작은 값들의 인덱스 찾아주고, 새로운 k를 위한 공간 만들기
        k_label = np.argmin(distance, axis=1)
        new_cent = np.zeros_like(cent)
        
        # 각 k 군집에 따른 평균 구하기 -> 새로운 센터
        for i in range(k):
            new_cent[i] = np.mean(ds[k_label==i], axis = 0)
        # 수렴
        if np.all(np.abs(new_cent - cent) < threshold):
            break
        cent = new_cent
        
    return np.concatenate([ds, k_label[:, np.newaxis]], axis=1)
    
def k_means(ds:np.ndarray, dist_fn, k, threshold=0.001):
    # ds.shape = [1500, 2] -> [n_samples, 2(x, y)]
    # 랜덤 센터 뽑기
    rand_idx = np.random.choice(ds.shape[0], k)
    centroid = ds[rand_idx, :] 
    
    # 각 센터에 대한 거리 구하기
    clustered_ = _calc_distances(ds, centroid, dist_fn, k, threshold) 
    return clustered_

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
    point = k_means(points, dist, 3)
    # point -> Tuple[n_samples, [x, y, k]]
    dataset.visualization2D(point, visual_param=config['visual'])
    
if __name__ == "__main__":
    main()