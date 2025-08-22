# AI-RECOGNITION-DOCKER

这是配置`ai-service docker`的测试

经过精简，镜像大小从11G -> 2G，大大节省了空间


# HOW TO USE

- **启动AI服务**
```bash
cd ai-service
```

- **第一次需要构建镜像**
```bash
docker build -t ai-service .
```            

- **查看镜像大小**
```bash
docker images ai-service         
```

- **命名为ai-reco，启动容器**
```bash
docker run -d -p 5000:5000 --name ai-reco
```   

- **查看运行中的容器**
```bash
docker ps
```

- **关闭容器**
```bash
docker stop diet-ai
```

