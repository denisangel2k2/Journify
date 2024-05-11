import torch
import torch.nn as nn

from classification.Classifier import Classifier

label_to_emotion = {
    0: 'Sad',
    1: 'Happy',
    2: 'Energetic',
    3: 'Calm'
}
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



class SpotifyClassifier(Classifier):

    __model = None

    def __init__(self):
        self.__model = self.buildModel()
        self.__model.load_state_dict(torch.load('classification/saved/ann_model.pth'))
    def buildModel(self):
        input_size = 11
        hidden_sizes = [256, 128, 64, 32]
        num_classes = 4

        model = ANN(input_size=input_size, hidden_sizes=hidden_sizes, num_classes=num_classes)
        return model

    def classify(self, input_features):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_features = input_features.to(device).float()
        self.__model.to(device)
        self.__model.eval()

        with torch.no_grad():

            prediction = self.__model(input_features)
            _, preds = torch.max(prediction, 1)

        return label_to_emotion[preds.item()]





