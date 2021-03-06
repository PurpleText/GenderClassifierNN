import model
import torch 
from torch import nn , optim
from dataset import getdata
import ctypes

def main():
    ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')
    #Batch_Size & lenght of a namevector
    batch_size =  27
    name_len = 12
    split = 0.8
    patience = 3

    #Loading feautres and labels training and validation
    t_getter , v_getter , len_data = getdata(batch_size , name_len , split)
    t_pop = int(len_data*split)
    v_pop = int(len_data*(1 - split))

    tnn = model.mod2(batch_size , name_len).cuda()
    criterion = nn.MSELoss()
    opt = optim.Adam(tnn.parameters() , lr = 0.00169)
    sof = nn.Softmax(dim = 1)
    old_value = float('inf')
    counter = 0
    save_state = None

    print("training on cuda")
    print("training_population {}".format(t_pop))
    print("validation_population {}".format(v_pop))
    k = 0

    while True :
        train_loss = 0 
        valid_loss = 0 
        tnn.train()
        for fet , label in t_getter:
            opt.zero_grad()
            if fet.shape[0] != batch_size : break
            output = tnn.forward(fet)
            t_loss = criterion(output.view(batch_size , 2) , label)
            opt.zero_grad()
            t_loss.backward()
            opt.step()
            train_loss +=t_loss.item()

        print ("\nLOSS --> " , (train_loss/t_pop))

        #validation process 
        with torch.no_grad():
            for fet , label in v_getter:
                if fet.shape[0] != batch_size : break
                output = tnn.forward(fet)
                v_loss = criterion(output.view(batch_size , 2) , label)
                valid_loss += v_loss.item()

        print ("valid_loss --->" , valid_loss/v_pop)
        print ("epoch no---> " , k)
        print()

        k += 1
        if old_value <  valid_loss : 
            if counter == 0 : 
                save_state  = tnn.state_dict()
            if counter == patience - 1 : 
                break 
            counter += 1
        else :
            counter = 0
            old_value = valid_loss

    torch.save(save_state , "weights:{}.pth".format(old_value))

if __name__  == '__main__':
    main()
