import os
import signal
from ctypes import *
import torch
import time
import torchvision.models as models
from threading import Thread
import sys
import signal
from ctypes import *

# Set Run on GPU
GPU_NUM = 0 
device = torch.device(f'cuda:{GPU_NUM}' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cpu') # Set Run on CPU 
torch.cuda.set_device(device)

pid = os.getpid()

# CPU pinning
"""
affinity_mask = {6} # CPU num = 6
os.sched_setaffinity(pid, affinity_mask)
affi = os.sched_getaffinity(pid)
print("Used CPU NUM is ", affi)
"""

# 프로세스가 실행하는 DNN 종류별 개수
dense_num = 0  
res_num = 0
alex_num = 0
vgg_num = 1
wide_num = 0
squeeze_num = 0
mobile_num = 0
mnas_num = 0
inception_num = 0
shuffle_num = 0
resx_num = 0

# Warmup 횟수
warming_NUM = 0

def predict(model, inputs):
    #start = time.time()
    out = model(inputs)
    #end = time.time()
    print(out[0,0])
    print(model.__class__.__name__)
    return (model.__class__.__name__)

inputs = torch.ones(1,3,224,224).cuda()
inputs2 = torch.ones(1,3, 299, 299).cuda()

# model load
if(dense_num > 0): 
    dense = models.densenet201(pretrained=True).cuda().eval()

if(res_num > 0): 
    res = models.resnet152(pretrained=True).cuda().eval()

if(alex_num > 0): 
    alex = models.alexnet(pretrained=True).cuda().eval()

if(vgg_num > 0): 
    vgg = models.vgg16(pretrained=True).cuda().eval()

if(wide_num > 0): 
    wide = models.wide_resnet50_2(pretrained=True).cuda().eval()

if(squeeze_num > 0): 
    squeeze = models.squeezenet1_0(pretrained=True).cuda().eval()

if(mobile_num > 0): 
    mobile = models.mobilenet_v2(pretrained=True).cuda().eval()

if(mnas_num > 0): 
    mnas = models.mnasnet1_0(pretrained=True).cuda().eval()

if(inception_num > 0): 
    inception = models.inception_v3(pretrained=True).cuda().eval()

if(shuffle_num > 0): 
    shuffle = models.shufflenet_v2_x1_0(pretrained=True).cuda().eval()

if(resx_num > 0): 
    resx = models.resnext101_32x8d(pretrained=True).cuda().eval() 


# WARM UP
for i in range(warming_NUM):
    dense(inputs)

for i in range(warming_NUM):
    res(inputs)

for i in range(warming_NUM):
    alex(inputs)

for i in range(warming_NUM):
    vgg(inputs)

for i in range(warming_NUM):
    wide(inputs)

for i in range(warming_NUM):
    squeeze(inputs)

for i in range(warming_NUM):
    mobile(inputs)

for i in range(warming_NUM):
    mnas(inputs)

for i in range(warming_NUM):
    inception(inputs2)

for i in range(warming_NUM):
    shuffle(inputs)

for i in range(warming_NUM):
    resx(inputs)
torch.cuda.synchronize()
if(warming_NUM != 0):
    print("warm up end")


model_list=[] 
inception_list=[]


# 모델 실행
for i in range(dense_num):
    model_list.append(dense)

for i in range(res_num):
    model_list.append(res)

for i in range(alex_num):
    model_list.append(alex)

for i in range(vgg_num):
    model_list.append(vgg)

for i in range(wide_num):
    model_list.append(wide)

for i in range(squeeze_num):
    model_list.append(squeeze)

for i in range(mobile_num):
    model_list.append(mobile)

for i in range(mnas_num):
    model_list.append(mnas)

for i in range(inception_num):
    inception_list.append(inception)

for i in range(shuffle_num):
    model_list.append(shuffle)

for i in range(resx_num):
    model_list.append(resx)



# thread_list = []
# print('start')
# start = time.time()

# for model in model_list:
#     my_thread = Thread(target=predict, args=(model, inputs))
#     # target은 predict함수를 실행하고 return값(output값)을 target에 저장
#     # args는 predict함수에 전달되는 2개의 parameter
#     my_thread.start()
#     thread_list.append(my_thread)

# for model in inception_list:
#     my_thread = Thread(target=predict, args=(model, inputs2))
#     my_thread.start()
#     thread_list.append(my_thread)

# for th in thread_list:
#     th.join()   # thread 종료

# torch.cuda.synchronize()
# end = time.time()
# print('pytorch-ori MULTI-THREAD',end-start)




# thread_list = []
# start_total = time.time()

# for model in model_list:
#     fut = torch.jit.fork(predict, model, inputs) # jit 컴파일러가 최적화를 해줌
#     thread_list.append(fut)

# for model in inception_list:
#     fut = torch.jit.fork(predict, model, inputs2)
#     thread_list.append(fut)

# torch.cuda.synchronize()
# end_total = time.time()
# print('pytorch-ori. SERIAL',end_total-start_total)

if len(sys.argv) is not 3 :
    print ("Usage : <.exe file> <PID> <nice value>")


nicevalue = os.nice(int(sys.argv[2])) # nicevalue 초기값 설정 (minimum -20)
resultpid = int(sys.argv[1]) # result.cpp 의 pid

# Switch 신호 대기
print("set nicevalue : ", nicevalue)
print("wait for switch")

#f = open("switch_python.txt", 'r')
while 1:
    if(os.stat("switch_python.txt").st_size !=0): # txt파일에 아무값이나 적으면 실행시작
        break
#f.close()

print('start')
#start = torch.cuda.Event(enable_timing = True)
#end = torch.cuda.Event(enable_timing = True)
#start.record()
for model in model_list:
    predict(model,inputs) 
for model in inception_list:
    predict(model,inputs2)
#end.record()    
#torch.cuda.synchronize()

#print('pytorch-ori exe time : ', start.elapsed_time(end)/1000,"'s")

#결과 나오면 sigQ
c = cdll.LoadLibrary("libc.so.6")
c.sigqueue(resultpid, 34, nicevalue)



