import torch


class AE(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(19, 18),
            torch.nn.ReLU(),
            torch.nn.Linear(18, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 12),
            torch.nn.ReLU(),
            torch.nn.Linear(12, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 8)
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(8, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 12),
            torch.nn.ReLU(),
            torch.nn.Linear(12, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 18),
            torch.nn.ReLU(),
            torch.nn.Linear(18, 19),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
