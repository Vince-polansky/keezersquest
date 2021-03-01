docker build -t keezersquest .
docker run -dt --rm -p 80:80 -p 443:443 --name keezersquest_server keezersquest
docker exec -it keezersquest_server bash
docker kill keezersquest_server
