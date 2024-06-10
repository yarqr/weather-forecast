# Weather Forecast

This project is a small service for getting weather reports

## How to launch?

1. Download source code

```sh
git clone https://github.com/yarqr/weather-forecast.git
```

2. Go to project folder

```sh
cd weather-forecast
```

3. Create a config.toml file and fill it as config.example.toml

4. Run service

```sh
docker compose -f deploy/docker-compose.yaml up -d --build
```
