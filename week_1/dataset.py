import yaml
import abc
import numpy as np
from typing import Tuple
from sklearn.datasets import make_blobs, make_moons, make_circles, make_s_curve, make_swiss_roll
import matplotlib.pyplot as plt


class Dataset(abc.ABC):
    def __init__(self, n_samples: int, noise: float):
        self.n_samples = n_samples
        self.noise = noise

    @abc.abstractmethod
    def making(self) -> Tuple[np.ndarray, np.ndarray]:
        pass

# Concrete dataset classes
class Blobs(Dataset):
    def making(self): # 빨간줄 그어지는거 어케 해결하지 괜히 팩토리를 만들었나..?
        return make_blobs(n_samples=self.n_samples, random_state=8)
class Moons(Dataset):
    def making(self):
        return make_moons(n_samples=self.n_samples, noise=self.noise, random_state=8)

class Circles(Dataset):
    def making(self):
        return make_circles(n_samples=self.n_samples, noise=self.noise, factor=0.5, random_state=8)

class S_Curve(Dataset):
    def making(self):
        return make_s_curve(n_samples=self.n_samples, noise=self.noise, random_state=8)

class Swiss_Roll(Dataset):
    def making(self):
        return make_swiss_roll(n_samples=self.n_samples, noise=self.noise, random_state=8)
    
class MakeDataset:
    dataset_map = {
            "blobs": Blobs,
            "moons": Moons,
            "circles": Circles,
            "s_curve": S_Curve,
            "swiss_roll": Swiss_Roll,
        }
    
    def __init__(self, n_samples: int, noise: float):
        self.n_samples = n_samples
        self.noise = noise
    
    # 이거 없앨까? 귀찮은데, 초기화 할 떄 바로 주면 안 되나? iter 넣을까?
    def make(self, dataset_type: str) -> Dataset:
        dataset_class = self.dataset_map.get(dataset_type.lower())
        if dataset_class:
            return dataset_class(self.n_samples, self.noise)
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}. Choose from: {list(self.dataset_map.keys())}")
        
# 귀찮으니 Gemini에게 맡기자
def visualization2D(datasets_to_plot, visual_param):
    # Plot each dataset in a separate subplot
    num_datasets = len(datasets_to_plot)
    fig, axes = plt.subplots(1, num_datasets, figsize=(5 * num_datasets, 5))
    
    # Handle the case of a single plot to avoid indexing errors
    if num_datasets == 1:
        axes = [axes]
    
    for i, (dataset_type, points, legend) in enumerate(datasets_to_plot):
        ax = axes[i]
        
        # Plot based on label type: discrete for blobs, moons, circles; continuous for others
        if dataset_type.lower() in ["blobs", "moons", "circles"]:
            colors = ['red', 'blue', 'green']
            for y_val in np.unique(legend):
                ax.scatter(
                    points[legend == y_val, 0],
                    points[legend == y_val, 1],
                    color=colors[int(y_val)],
                    label=f"Class {int(y_val)}",
                    s=visual_param['size'],
                    marker=visual_param['marker']
                )
            ax.legend()
        else:
            # Use a colormap for continuous labels like S-Curve and Swiss Roll - 이건 3D로 표시해야 제대로 나오겠다.
            scatter = ax.scatter(points[:, 0], points[:, 1], c=legend, cmap='viridis', s=visual_param['size'])
            fig.colorbar(scatter, ax=ax, label='Label (Continuous)')
            
        ax.set_title(f"Dataset: {dataset_type.capitalize()}")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.grid(True)
        
    plt.tight_layout()
    plt.show()
    
def save_txt(datasets_to_plot):
    for i, (data_type, points, legend) in enumerate(datasets_to_plot):
        with open(f"dataset_{data_type.capitalize()}.txt", "w") as f:
            x, y = points.shape
            f.write(f"{x}, {y+1} \n")
            for (x, y), l in zip(points, legend):
                f.write(f"{x}, {y}, {l} \n")

if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    exec_mode = int(config['mode']) # 비트마스크
    n_samples = config['n_samples']
    noise = config['noise']
    visual_param = config['visual']
    
    dataset_factory = MakeDataset(n_samples, noise)
    
    datasets_to_plot = []
    for dataset_type in config['datasets']['type']:
        dataset_generator = dataset_factory.make(dataset_type)
        points, legend = dataset_generator.making()
        datasets_to_plot.append((dataset_type, points, legend))
    num_datasets = len(datasets_to_plot)
    
    # 비트 마스킹
    if exec_mode & 1:
        # visualization
        visualization2D(datasets_to_plot, visual_param)
        
    if exec_mode & 2:
        # save to txt file, easy to read in C
        save_txt(datasets_to_plot)
    