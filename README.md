# ImageFlaskWebserver

Basic webserver that listens to json requests from the dds-translator python program. It displays finished images in a video stream.

## Getting Started

### Requirements

- docker
- python 3.11
- a kubernetes distribution

Python requirements

- flask

### Run locally 

```bash
docker compose build . 
docker compose up
```

Access the webserver on localhost:5000

### Deploy on kubernetes

#### Using docker registry

The charts are using a local registry to deploy using docker hub follow this guide [here](https://docs.docker.com/docker-hub/quickstart/) and 
modify the ``image`` field in deployment.yaml.

```yaml
spec:
      containers:
      - name: web-server-app
        image: localhost:5001/web-server-app:latest
        ports:
        - containerPort: 5000
```

#### If using a local registry

Deploy a local registry, ONLY if you do not have one deployed check using ``docker ps`` and look for registry
in the image name.

```bash
sudo docker run -d -p 5001:5000 --restart=always --name registry registry:latest
```

#### Build the image 

```bash
docker build -t web-server-app .
docker tag web-server-app localhost:5001/web-server-app:latest
docker push localhost:5001/web-server-app:latest
```

```bash
cd charts
kubectl apply -f service.yaml
kubectl apply -f deployment.yaml
```

Check if the web-server-app is deployed and running, look for web-server-app-#######-#####

```bash
kubectl get pods -A
```




