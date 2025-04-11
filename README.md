# Sorting Hat + Docker

Recognizing the importance of **open source**, we strived to build a solid project. We believe **Docker** is one of the most reliable solutions for creating ready-to-use projects, ensuring ease of deployment and scalability.<br>
We offer two straightforward methods to build *Sorting Hat* from scratch. 
While we recommend using the prebuilt Docker image directly, you’re also free to build `Dockerfile`.<br><br>
The current repository contains all the *Sorting Hat* repositories:<br>
1. [Sorting Hat](https://github.com/davixdedem/Sorting-Hat.git)

Before starting please check all the [Requirements]().

# Requirements
- **CPU**: ARMv7 (for Raspberry Pi 3) or ARMv8 (for Raspberry Pi 4) architecture
- **RAM**: At least 2GB (4GB+ recommended for larger workloads)
- **Storage**: At least 8GB free space (Docker image + dependencies, may vary based on workload)
- **Docker**: Docker Engine installed (Follow the installation guide for Raspberry Pi here: https://docs.docker.com/engine/install/raspberry-pi/)

# Getting started
*-5 minutes-*<br> 
**Docker Engine** is the core component of Docker, responsible for managing and running containers on your system. For detailed installation instructions, please refer to the official Docker installation guide for Raspberry Pi: **Docker Engine Installation Guide for Raspberry Pi**.<br>
This will direct users to the correct installation guide for Raspberry Pi rather than the one for Ubuntu. Let me know if you need more changes!

# How to Build

### Method 1 - Recommended --> *Not yet available*

Pull the Docker image from the official registry.<br>
If you're targeting ARM:
```
docker pull sorting-hat-linux/arm64-cuda-supported
```

If you're targeting ARM32:
```
docker pull sorting-hat-linux/arm32v7-cuda-supported
```

Please notes:
- arm32v7: For Raspberry Pi 3 and older models, which use 32-bit ARM.
- arm64v7: For Raspberry Pi 4 and later, which can use 64-bit ARM (depending on OS and Raspberry Pi configuration).

### Method 2
*-39 minutes-*<br>
- Clone this repository:
```
git clone --branch docker https://github.com/davixdedem/Sorting-Hat.git
```

- Enter the directory:
```
cd Sorting-Hat
```

- Download all submodules:
```
git submodule update --init --recursive
```

- Explicitly set them to track `main`:
```
git submodule foreach --recursive git checkout main
git submodule foreach --recursive git pull origin main
```

- Build docker (*this will take a while*):
```
docker build --no-cache -t sorting-hat-docker .
```

# How to Start

###  Method 1

Run it and get a command shell:
```
docker run --rm --privileged -p 8888:8888 -it -v $(pwd)/src:/app sorting-hat-docker /bin/bash
```
- Start **Sorting Hat**:
```
python3 main.py
```
**You're done!**

# How to let it speak!

If you'd like to try a shot, we provide an example script **ready-to-run**.

- Get a command shell and run the example:
```
docker exec -it $(docker ps -qf "ancestor=sorting-hat-docker") bash -c "python3 main.py"
```

###  Method 2
Copy daemon service to systemd directory:
```
sudo cp daemon_sorting_hat.service /etc/systemd/system/ && sudo systemctl daemon-reload
```
Enable service and start it:
```
sudo systemctl enable daemon_sorting_hat && sudo systemctl start daemon_sorting_hat
```

