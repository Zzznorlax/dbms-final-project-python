# Database Systems Final Project


### Install dependencies
```shell
pip install -r requirements.txt
```

### Configure settings with `.env`
Create `.env`
```shell
touch .env
```

(Optional) Create sqlite database
```shell
touch test.db
```

Set the URI to link to a database in `.env`
```
SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
```

Generate JWT secret
```shell
>>> import os
>>> import binascii
>>> binascii.hexlify(os.urandom(24))
b'deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f'
```

Set JWT secret in `.env`
```
IMGUR_API_CLIENT_ID="deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f"
```

[Imgur API docs](https://apidocs.imgur.com)
[Register application to get imgur API client ID](https://api.imgur.com/oauth2/addclient)


Set Imgur client ID in `.env`
```
IMGUR_API_CLIENT_ID="008B8008B848B8"
```


### Start server
```shell
uvicorn main:app --reload
```
