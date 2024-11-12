## Run translater app
```
python serve_translation.py
```
## Test
```
python client.py
```
## Run docker-compose
```
docker-compose up -d
```
### If ray version mismatch error occurs
1.Go inside ray conatiner
```
docker exec -it ray bash
```
2.Install 2.38.0 version ray
```
pip install ray==2.38.0
```
3.Restart ray container
```
docker restart ray
```
### Access ray dashboard at localhost:8265
### Access ray prometheus at localhost:9091
### Access ray grafana at localhost:3000