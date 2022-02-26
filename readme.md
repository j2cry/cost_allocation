### Setup instructions
1. Create docker network
```commandline
docker network create cost-net
```

2. Run mongo container with
```commandline
docker run --net cost-net --hostname mongo_data --name mongo_data -d mongo:5.0.6
```

3. Make application docker image with
```commandline
docker build -t cost_image .
```

4. Run application container with
```commandline
docker run --net cost-net --name cost_app -dp 80:8080 cost_image
```

<hr>

To start with Traefik:
```commandline
docker-compose -f cost-compose.yml up -d
```