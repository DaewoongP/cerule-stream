# Cuda 9.0

## 1. Install Graphic Driver

```shell
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-396
```

## 2. Install Cuda 9.0
[CUDA Toolkit 9.0 Downloads](https://developer.nvidia.com/cuda-90-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1604&target_type=debnetwork)
[Installation Guide Linux :: CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation)

```shell
sudo dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda-9-0
```

**Export Env**

```
export PATH=/usr/local/cuda-9.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64:${LD_LIBRARY_PATH}
```

```shell
nvcc --version
nvidia-smi
```

```shell
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2017 NVIDIA Corporation
Built on Fri_Sep__1_21:08:03_CDT_2017
Cuda compilation tools, release 9.0, V9.0.176
nvidia-smi
Wed May 23 13:09:00 2018      
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 396.26                 Driver Version: 396.26                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 1080    Off  | 00000000:01:00.0  On |                  N/A |
|  0%   49C    P8    15W / 200W |    237MiB /  8111MiB |      2%      Default |
+-------------------------------+----------------------+----------------------+
                                                                             
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1063      G   /usr/lib/xorg/Xorg                           114MiB |
|    0      1381      G   gala                                          84MiB |
|    0      7042      G   /proc/self/exe                                35MiB |
+-----------------------------------------------------------------------------+
```

## 3. Install CuDnn

[CuDNN Downloads](https://developer.nvidia.com/rdp/cudnn-download)

## 4. Install [PyTorch](https://pytorch.org/)

```shell
pip3 install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp35-cp35m-linux_x86_64.whl
pip3 install torchvision
```

## 4. Install [TensorFlow](https://github.com/tensorflow/tensorflow)

```shell
pip3 install --upgrade tensorflow-gpu
```

## 5. Install [Nvidia Docker](https://github.com/NVIDIA/nvidia-docker)

[NVIDIA Container Runtime for Docker](https://github.com/NVIDIA/nvidia-docker)
[Using TensorFlow via Docker](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker)



