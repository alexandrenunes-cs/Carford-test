# Carford Town


## Develop

clone repo
``` 
git clone https://github.com/alexandrenunes-cs/Carford-test.git
``` 


build and up docker container
``` 
docker-compose up --build -d
```


Enter in docker container
``` 
docker exec -it carford_town bash
```

activate pipenv shell 
``` 
pipenv shell
```

### How to test?

All functions
``` 
python -m pytest
```

A especific function
``` 
python -m pytest path/to/test/file.py::ClassName::function_name
```

