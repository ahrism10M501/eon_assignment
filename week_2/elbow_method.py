import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
from week_1 import dataset
import yaml
from week_1.k_means import k_means, Distance

import matplotlib.pyplot as plt

class ElbowMethod:
    @staticmethod
    def process(cluster_fn, data, dist_fn, max_k=9):
        wss = []
        for iter in range(max_k):
            point, label, cent = k_means(data, dist_fn, iter+1)
            unique_label = np.unique(label)
            cluster_wss = 0
            for k in unique_label:
                cluster_ = point[np.where(label == k)]
                cent_ = cent[k]
                distance = dist_fn(
                    cent_[np.newaxis, np.newaxis, :],
                    cluster_[np.newaxis, :, :]
                )
                cluster_wss += np.sum(distance**2)
            wss.append(cluster_wss)
        return np.array(wss)
    
def main():
    np.random.seed(2025)
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    factory = dataset.MakeDataset(config["n_samples"], config["noise"])
    ds = factory.make("blobs")
    points, _ = ds.making()
    
    dist = Distance.euclidean
    num_k = 9
    wss = ElbowMethod.process(k_means, points, dist, num_k)
    
    plt.figure()
    plt.plot(range(1, num_k+1), wss)
    plt.show()
    
if __name__ == "__main__":
    main()