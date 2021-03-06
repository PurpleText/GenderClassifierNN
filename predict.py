import torch
from torch.nn import functional as F
from sys import argv
import  model  
from tokenizer import tokenizer

def main() : 
    
    words = argv[1:]
    name_len = 20
    t_obj = tokenizer(name_len)
    tnn = model.mod2(1 , name_len).cuda()
    tnn.eval()
    tnn.load_state_dict(torch.load("weights-8674.pth"))

    with torch.no_grad():
        for word in words:
            word = torch.Tensor(t_obj.tkniz(word)).float().cuda()
            output = tnn.forward(word.unsqueeze(1))
            output = F.softmax(output , dim = 1)
            male , female = output[0] 
            print ("female : {} % probabilty \nmale : {} % probabilty ".format(male.item() , female.item()))
if __name__ == "__main__" : 
    main()
