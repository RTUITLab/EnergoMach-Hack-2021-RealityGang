# EnergoMach-Hack-2021-RealityGang
🤍 Core backend service for LeadersOfDigital's "EnergoMach" hackathon 2021

## Launching project in production mode
#### Git, Docker and Docker Compose must be installed

1. Clone project with submodules

```
git clone https://github.com/RTUITLab/EnergoMach-Hack-2021-RealityGang em
cd em
git submodule init
git submodule update
```

2. Generate new DJANGO_SECRET_KEY and paste it to backend service as SECRET_KEY environment variable in docker-compose.yml

> To generate new DJANGO_SECRET_KEY use this instruction: https://stackoverflow.com/a/57678930/14355198

```
services:
  backend:
    environment:
      - SECRET_KEY=NEW_DJANGO_SECRET_KEY
```

3. Put your PRODUCTION_URL to frontend service as YOUR_PRODUCTION_URL environment variable in docker-compose.yml
```
services:
  frontend:
    environment:
      - REACT_APP_PRODUCTION_URL=http://YOUR_PRODUCTION_URL:8000/
```

4. Launch project

```
docker-compose up --build
```

> Done! Project launched on 8000 port!

<!---

-->

This project was made by RealityGang - team of RTU IT Lab.
