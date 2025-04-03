### Workflow
1. client request to login with username and password 
```sh
{
    "username": user123,
    "password": pass123
}
```
2. client receives the JWT token containing
```sh
{
    "alg": "HS256",
    "typ": "JWT"
}
```