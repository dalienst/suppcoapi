# Accounts

## User

### All Users
`/api/v1/auth/`

Method: `GET`

### User Detail
`/api/v1/auth/user/<str:username>/`

Method: `GET`

### Login
`/api/v1/auth/login/`

Method: `POST`

```json
{
    "email": "email@example.com",
    "password": "Passsword@123",
}
```

### Contractor
`/api/v1/auth/signup/contractor/`

Method: `POST`

```json
{
    "email": "email@example.com",
    "password": "Passsword@123",
}
```

### Supplier
`/api/v1/auth/signup/supplier/`

Method: `POST`

```json
{
    "email": "email@example.com",
    "password": "Passsword@123",
}
```

### Profile
`/api/v1/auth/<str:id>/`

Method: `GET`

`/api/v1/auth/<str:id>/`

Method: `PATCH`


