# Luminos backend

This Git repository hosts backend for Luminos mobile app.

# Introduction

The backend that hosts APIs required by both Luminos mobile app for IOS and Android.

## Technology

- Django 2
- Python 3
- Amazon Web Services
    - Elastic Beanstalk
- Twilio
    - SMS Account Verification
- One Signal
    - For hanlding push notifications
- React-Native
    - Mobile app
- Redux
    - Mobile app state management

## Authorization

The Luminos app uses token authentication.

Post to `/api/v1/verification/` with `country_code` and `phone_number` to request Twilio to send a SMS Verification Code to phone number that is part of sent payload.

Post to `/api/v1/verification/token/` with `country_code`, `phone_number` and `token` set (JSON, form-data and x-www-form-urlencoded supported) to obtain the token.  
`token` is a Twilio generated code that you have received on your device.

In Postman, create a global variable named `TOKEN` with your token.

# Launching Django backend

## Requirements:  
1. `docker`
2. `docker-compose`
3. `One Signal account` - optional
4. `Twilio account` - optional

## Running:  
1. Copy and paste `config.template.env` file under name: `config.env` and fill all variables:
2. `LUMINOS_DB_ENGINE=django.db.backends.postgresql` -> database engine to run as storage for backend, if you are okay with PostgreSQL then you can leave it as it is
3. `LUMINOS_DB_NAME=luminos` -> database name that is suppose to be created / used by Luminos backend, you can leave it as it is for development purpose
4. `LUMINOS_DB_USER=masteruser` -> database username that is suppose to connect from Luminos backend, you can leave it as it is for development purposes
5. `LUMINOS_DB_PASSWORD=pass_luminos_db_docker` -> database password for given username that is suppose to be used together in order to conenct to database from Luminos backend, you can leave it as it is for development purposes
6. `LUMINOS_DB_HOST=database` -> database hostname that Luminos backend should connect to. Passing `database` works for local development because in `docker-compose.yml` backend container is linked to database container via `database` name
7. `LUMINOS_DB_PORT=5432` -> database port
8. `AUTHY_DISABLE=1` -> `1` if Twilio SMS verification should be disabled, if `0`, you also need to provide `AUTHY_ACCOUNT_SECURITY_API_KEY`. `1` is useful for local developmnet as authentication will pass any veriifcation code
9. `AUTHY_ACCOUNT_SECURITY_API_KEY=12345` - `Twilio` API Key, required if `AUTHY_DISABLE=0`
10. `ONESIGNAL_DISABLE=1` -> `1` if push notifications integration via OneSignal should be disabled, if `0`, you also need to provide `ONESIGNAL_API_ENDPOINT` and `ONESIGNAL_AUTHORIZATION_HEADER`. If `1` then push notifications are not send to mobile devices.
11. `ONESIGNAL_API_ENDPOINT=https://onesignal.com/api/v1/notifications` -> URL pointing to One Signal API for push notifications, should not change
12. `ONESIGNAL_AUTHORIZATION_HEADER=` -> API Key for One Signal, allowing backend to create new push notifications
13. `ONESIGNAL_APPID=` -> ID of Your One Signal Application
14. Execute `docker-compose up -d` in the root directory of the repository
15. Check if containers started with `docker ps`
16. You can now access DJango backend via `localhost:8000`
17. You can now access database via `localhost:5432` with credentials used in `config.env`