# Wind_Energy_Dashboard

##Create docker image
```
docker build -t dashboard .
```
## Spin Up a Container
```
docker run -p 8987:8000 -d dashboard
```