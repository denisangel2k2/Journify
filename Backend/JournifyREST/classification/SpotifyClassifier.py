import torch
import torch.nn as nn


class ANN(nn.Module):
    def __init__(self, input_size, hidden_sizes, num_classes, dropout_prob=0.5):
        super(ANN, self).__init__()
        layers = []
        last_dim = input_size
        for size in hidden_sizes:
            layers.append(nn.Linear(last_dim, size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_prob))
            last_dim = size
        layers.append(nn.Linear(last_dim, num_classes))
        self.net = nn.Sequential(*layers)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.net(x)
        out = self.softmax(out)
        return out


class Classifier:
    pass


class SpotifyClassifier(Classifier):
    def buildModel(self):
        input_size = 10 # how many features
        hidden_sizes = [256, 128, 64, 32]
        num_classes = 4
        learning_rate = 0.0048
        batch_size = 8
        num_epochs = 200

        model = ANN(input_size=input_size, hidden_sizes=hidden_sizes, num_classes=num_classes)
        return model

    def classify(self):
        pass

