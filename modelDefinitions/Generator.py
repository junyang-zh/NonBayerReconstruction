import torch.nn as nn
import torch.nn.functional as F
import torch
from torchsummary import summary

def init_weights(m):
    if isinstance(m, nn.Conv2d):
        nn.init.xavier_uniform_(m.weight)

class pixelShuffleUpsampling(nn.Module):
    def __init__(self, inputFilters, scailingFactor=2):
        super(pixelShuffleUpsampling, self).__init__()
    
        self.upSample = nn.Sequential(  nn.Conv2d(inputFilters, inputFilters * (scailingFactor**2), 3, 1, 1),
                                        nn.BatchNorm2d(inputFilters * (scailingFactor**2)),
                                        nn.PixelShuffle(upscale_factor=scailingFactor),
                                        nn.PReLU()
                                    )
    def forward(self, tensor):
        return self.upSample(tensor)

class simpleConvNet(nn.Module):
    def __init__(self, squeezeFilters = 64, expandFilters = 64, depth = 3):
        super(simpleConvNet, self).__init__()

        # Input Block
        self.inputConv = nn.Conv2d(3, squeezeFilters, 3,1,1)
        self.down1 = nn.Conv2d(64, 128, 3, 2, 1) 

        self.down2 = nn.Conv2d(128, 256, 3, 2, 1) 

        self.convUP1 = nn.Conv2d(256, 128, 3, 1, 1) 
        self.psUpsampling1 = pixelShuffleUpsampling(inputFilters=128, scailingFactor=2)

        self.convUP2 = nn.Conv2d(128, 64, 3, 1, 1) 
        self.psUpsampling2 = pixelShuffleUpsampling(inputFilters=64, scailingFactor=2)

        # Output Block
        self.convOut = nn.Conv2d(squeezeFilters,3,1,)

        # Weight Initialization
        #self._initialize_weights()

    def forward(self, img):

        xInp = F.leaky_relu(self.inputConv(img))

        xDS1 = F.leaky_relu(self.down1(xInp))

        xDS2 = F.leaky_relu(self.down2(xDS1))

        xCP1 = F.leaky_relu(self.convUP1(xDS2))
        xPS1 = self.psUpsampling1(xCP1) 

        xCP2 = F.leaky_relu(self.convUP2(xPS1))
        xPS2 = self.psUpsampling2(xCP2)
        
        return torch.tanh(self.convOut(xPS2) + img)
        
        
    
    def _initialize_weights(self):

        self.inputConv.apply(init_weights)
        
        self.down1.apply(init_weights)
        
        self.down2.apply(init_weights)
        
        self.convUP1.apply(init_weights)
        self.psUpsampling1.apply(init_weights)
       
        self.convUP2.apply(init_weights)
        self.psUpsampling2.apply(init_weights)
        
        self.convOut.apply(init_weights)

#net = simpleConvNet()
#summary(net, input_size = (3, 128, 128))
#print ("reconstruction network")