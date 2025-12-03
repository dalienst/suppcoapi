# Company

## Supplier/Contractor Company Detail and Update
`/api/v1/companies/my/`

Method: `GET`

`/api/v1/companies/<str:identity>/`

Method: `PATCH`

## Roles
### Create
`/api/v1/roles/`

Method: `POST`

```json
{
    "name": "role-name",
    "company": "company-identity",
    "is_head": true, // false by default
}
```

### List
`/api/v1/roles/`

Method: `GET`

### Update
`/api/v1/roles/<str:identity>/`

Method: `PATCH`

## Employees
### Create
`/api/v1/auth/add/employee/`

Method: `POST`

```json
{
    "email": "email@example.com",
    "password": "Passsword@123",
    "company": "company-identity",
    "role": "role-identity",
}
```

## Branches - Suppliers
### Create
`/api/v1/branches/`

Method: `POST`

```json
{
    "name": "branch-name",
    "address": "branch-address",
}
```

### List
`/api/v1/branches/`

Method: `GET`

### Update
`/api/v1/branches/<str:identity>/`

Method: `PATCH`

### Assign Employee
`/api/v1/employees/assign/`

Method: `POST`

```json
{
    "employee_username": "employee-username",
    "branch": "branch-identity",
}
```

### Unassign Employee
`/api/v1/employees/unassign/`

Method: `POST`

```json
{
    "employee_username": "employee-username",
    "branch": "branch-identity",
}
```

## Sites - Contractors
### Create
`/api/v1/sites/`

Method: `POST`

```json
{
    "name": "site-name",
    "address": "site-address",
}
```

### List
`/api/v1/sites/`

Method: `GET`

### Update
`/api/v1/sites/<str:identity>/`

Method: `PATCH`

### Assign Employee
`/api/v1/employees/assign/`

Method: `POST`

```json
{
    "employee_username": "employee-username",
    "site": "site-identity",
}
```

### Unassign Employee
`/api/v1/employees/unassign/`

Method: `POST`

```json
{
    "employee_username": "employee-username",
    "site": "site-identity",
}
```
