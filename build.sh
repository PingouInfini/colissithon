rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/dockerdist/main/ && cp -Rf ./main/* ./docker/context/dockerdist/main/
mkdir -p ./docker/context/dockerdist/samples/ && cp -Rf ./samples/* ./docker/context/dockerdist/samples/
cp -Rf ./colissithon.iml ./docker/context/dockerdist/
cp -Rf ./send_colis.py ./docker/context/dockerdist/
cp -Rf ./setup.py ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/

docker-compose -f ./docker/colissithon.yml build