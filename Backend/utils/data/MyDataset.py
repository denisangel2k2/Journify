import numpy as np
from torchvision import datasets, models, transforms
import os
from torch.utils.data import Dataset,DataLoader
import torch.nn as nn
import pandas as pd


class MyDataset(Dataset):
    def __init__(self, data, transform=None):
        self.inputs = []
        self.labels = []
        self.transform=transform
        for i in range(4):
            for filename in os.listdir(data + str(i)):
                audio_file = str(data + str(i) + "/" + filename)
                spectrogram = extract_features(audio_file)
                print(audio_file+' '+str(spectrogram.shape))
                if spectrogram is not None:  
                    self.inputs.append(spectrogram)
                    self.labels.append(i)


        self.inputs = np.stack(self.inputs)
        self.labels = np.array(self.labels)

        self.inputs = torch.tensor(self.inputs, dtype=torch.float32).unsqueeze(1)
        self.labels = torch.tensor(self.labels)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        item = self.inputs[idx]
        target = self.labels[idx]

        if self.transform:
            item = self.transform(item)

        return item, target
    