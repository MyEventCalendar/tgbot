# EventCalendarBot

### build docker image
```shell
docker build . -t event-calendar-bot
```

### create env.file with secrets
```shell
cat << EOF > file.env
API_KEY=YOUR_API_KEY
API_URL=YOUR_API_URL
EOF
```

### start docker container
```shell
docker run -d --env-file file.env event-calendar-bot

```

