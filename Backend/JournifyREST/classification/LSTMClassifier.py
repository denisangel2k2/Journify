
import torch.nn as nn
from torchvision import models
from classification.Classifier import Classifier
import torch
from torchvision import transforms
import torch.nn.functional as F

label_to_emotion = {
    0: 'Sad',
    1: 'Happy',
    2: 'Energetic',
    3: 'Calm'
}

transform=transforms.Compose([
    # transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


class ResNetBiLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, seq_length, num_layers, num_classes):
        super(ResNetBiLSTM, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.seq_length = seq_length

        resnet = models.resnet18(pretrained=True)
        resnet.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.resnet = nn.Sequential(*list(resnet.children())[:-1])
        self.resnet.eval()

        # Bidirectional LSTM
        self.lstm = nn.LSTM(input_size, hidden_size // 2, num_layers, bidirectional=True, batch_first=True)
        # Double the size of fc1 input
        self.fc1 = nn.Linear(hidden_size, num_classes)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def forward(self, x):
        sequences = []
        x = x.permute(1, 0, 2, 3, 4)
        for sequence in x:
            sequence = self.resnet(sequence)
            sequence = torch.flatten(sequence, 1)
            sequences.append(sequence)

        x = torch.stack(sequences)
        x = x.permute(1, 0, 2)

        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size // 2).to(self.device)
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size // 2).to(self.device)
        out, _ = self.lstm(x, (h0, c0))

        out = torch.cat((out[:, -1, :self.hidden_size // 2], out[:, 0, self.hidden_size // 2:]), dim=1)
        out = self.fc1(out)
        out = F.softmax(out, dim=1)
        return out


class LSTMClassifier(Classifier):
    __model = None

    def __init__(self):
        self.__model = self.buildModel()
        self.__model.load_state_dict(torch.load('classification/saved/lstmresnet_bi86acc3seq.pth'))

    def buildModel(self):
        model = ResNetBiLSTM(input_size=512, hidden_size=128, seq_length=3, num_layers=2, num_classes=4)
        return model


    def classify(self, input_features):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.to(device)
        self.__model.eval()

        input_tensor = transform(input_features)
        input_tensor = input_tensor.unsqueeze(0).to(device).float()
        print(input_tensor.shape)
        with torch.no_grad():
            prediction = self.__model(input_tensor)
            _, preds = torch.max(prediction, 1)
        return label_to_emotion[preds.item()]