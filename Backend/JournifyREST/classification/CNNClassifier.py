import torch.nn as nn
from torchvision import models
from classification.Classifier import Classifier
import torch
from torchvision import transforms
label_to_emotion = {
    0: 'Sad',
    1: 'Happy',
    2: 'Energetic',
    3: 'Calm'
}

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
class CNNClassifier(Classifier):
    __model = None
    def __init__(self):
        self.__model = self.buildModel()
        self.__model.load_state_dict(torch.load('classification/saved/9e4SGD_88acc.pth'))

    def buildModel(self):
        model_conv = models.resnet18(weights='IMAGENET1K_V1')
        for param in model_conv.parameters():
            param.requires_grad = False

        num_ftrs = model_conv.fc.in_features
        model_conv.fc = nn.Linear(num_ftrs, 4)
        model_conv.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=1, padding=2, bias=True)

        return model_conv



    def classify(self, input_features):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.to(device)
        self.__model.eval()

        input_tensor = transform(input_features)
        input_tensor = input_tensor.unsqueeze(0).to(device).float()
        with torch.no_grad():
            prediction = self.__model(input_tensor)
            _, preds = torch.max(prediction, 1)
        return label_to_emotion[preds.item()]










