Installation and configuration instructions

I. In two docker containers
    1. Launch a container with a MongoDB database (see the official documentation)
    2. In the file `settings.py` specify the IP address and port of the container with the database (variable `MONGO_SERVER`)
        (it is better to give the containers names, and run them in conjunction - see the documentation `docker run --link`)
    3. In the project directory, run the `docker build -t cost_service .` command
    4. Launch the container using the command `docker run -dp 80:8080 cost_service`

II. In a single docker container
    1. Uncomment the required code block in the dockerfile
    2. In the project directory, run the `docker build -t cost_service .` command
    3. Launch the container using the command `docker run -dp 80:8080 cost_service`



Инструкция по установке и настройке

I. В двух docker-контейнерах
    1. Запустить контейнер с базой данных MongoDB (см.официальную документацию)
    2. В файле `settings.py` указать IP-адрес и порт контейнера с базой данных (переменная `MONGO_SERVER`)
        (лучше давать контейнерам названия, и запускать в связке - см.документацию `docker run --link`)
    3. В каталоге проекта выполнить команду `docker build -t cost_service .`
    4. Запустить контейнер c помощью команды `docker run -dp 80:8080 cost_service`

II. В одном docker-контейнере
    1. Раскомментировать необходимый блок кода в dockerfile
    2. В каталоге проекта выполнить команду `docker build -t cost_service .`
    3. Запустить контейнер c помощью команды `docker run -dp 80:8080 cost_service`



# local commands
sudo docker build -t cost_image .
sudo docker save -o ~/cost.tar cost_image
sudo scp /home/avagadro/cost.tar root@194.58.119.214:/usr/files

# server command
docker load -i /usr/files/cost.tar
docker run --name mongodata -d mongo
docker run --name cost_service -dp 80:8080 cost_image

# don't forget to setup the Mongo IP in settings.py!
