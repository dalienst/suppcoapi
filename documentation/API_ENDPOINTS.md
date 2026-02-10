# SUPPCO API Documentation

## Overview
This document outlines the available API endpoints for the SUPPCO application. All endpoints are prefixed with `api/v1/` unless otherwise noted (e.g., admin).

## Authentication & Accounts
**Base URL:** `api/v1/auth/`

| Endpoint | View | Description |
|----------|------|-------------|
| `login/` | `LoginView` | User login |
| `<str:id>/` | `UserDetailView` | Get user details by ID |
| `/` | `UsersListView` | List all users |
| `user/<str:username>/` | `UserPublicProfile` | Public user profile |
| `signup/supplier/` | `SupplierCreateView` | Register a new supplier |
| `signup/contractor/` | `ContractorCreateView` | Register a new contractor |
| `verify-email/<str:uidb64>/<str:token>/` | `VerifyAccountView` | Verify email address |
| `password/reset/` | `RequestPasswordResetView` | Request password reset |
| `password/new/` | `PasswordResetView` | Set new password |
| `owner/<str:id>/` | `OwnerDetailView` | Owner details |
| `add/employee/` | `EmployeeCreatedByOwnerView` | Add employee by owner |

## Companies
**Base URL:** `api/v1/companies/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `CompanyListView` | List all companies |
| `my/` | `MyCompanyListView` | List my companies |
| `<str:identity>/` | `CompanyDetailView` | Company details |

## Permissions
**Base URL:** `api/v1/permissions/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `PermissionListCreateView` | List or create permissions |
| `<str:reference>` | `PermissionDetailView` | Permission details |

## Roles
**Base URL:** `api/v1/roles/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `RoleListCreateView` | List or create roles |
| `<str:identity>/` | `RoleDetailView` | Role details |

## Branches
**Base URL:** `api/v1/branches/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `BranchListCreateView` | List or create branches |
| `<str:identity>/` | `BranchDetailView` | Branch details |

## Sites
**Base URL:** `api/v1/sites/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `SiteListCreateView` | List or create sites |
| `<str:identity>/` | `SiteDetailView` | Site details |

## Employment
**Base URL:** `api/v1/employees/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `EmploymentListView` | List employment records |
| `assign/` | `EmployeeAssignView` | Assign employee |
| `unassign/` | `EmployeeUnassignView` | Unassign employee |

## Inventory
**Base URL:** `api/v1/inventory/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `InventoryListView` | List inventory |
| `list-create/` | `InventoryListCreateView` | List or create inventory items |
| `<str:inventory_code>/` | `InventoryDetailView` | Inventory item details |

## Layers
**Base URL:** `api/v1/layers/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `LayerListView` | List layers |
| `list-create/` | `LayerListCreateView` | List or create layers |
| `<str:reference>/` | `LayerDetailView` | Layer details |

## Sublayers
**Base URL:** `api/v1/sublayers/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `SubLayerListView` | List sublayers |
| `list-create/` | `SubLayerListCreateView` | List or create sublayers |
| `<str:reference>/` | `SubLayerRetrieveUpdateDestroyView` | Sublayer details (Retrieve/Update/Destroy) |

## Sublayer Items
**Base URL:** `api/v1/sublayeritems/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `SublayerItemListView` | List sublayer items |
| `list-create/` | `SublayerItemListCreateView` | List or create sublayer items |
| `<str:reference>/` | `SublayerItemDetailView` | Sublayer item details |

## Brackets
**Base URL:** `api/v1/brackets/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `BracketListView` | List brackets |
| `list-create/` | `BracketListCreateView` | List or create brackets |
| `<str:reference>/` | `BracketRetrieveUpdateDestroyView` | Bracket details (Retrieve/Update/Destroy) |

## Products
**Base URL:** `api/v1/products/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `ProductListCreateView` | List or create products |
| `<str:reference>/` | `ProductDetailView` | Product details |

## Shell Equipment
**Base URL:** `api/v1/shellequipment/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `ShellEquipmentListView` | List shell equipment |
| `create/` | `ShellEquipmentListCreateView` | Create shell equipment |
| `<str:reference>/` | `ShellEquipmentRetrieveUpdateDestroyView` | Shell equipment details |

## Sites Equipment
**Base URL:** `api/v1/sitesequipment/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `SitesEquipmentListView` | List sites equipment |
| `create/` | `SitesEquipmentListCreateView` | Create sites equipment |
| `<str:reference>/` | `SitesEquipmentRetrieveUpdateDestroyView` | Sites equipment details |

## Plumbing
**Base URL:** `api/v1/plumbing/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `PlumbingListView` | List plumbing items |
| `create/` | `PlumbingListCreateView` | Create plumbing items |
| `<str:reference>/` | `PlumbingRetrieveUpdateDestroyView` | Plumbing item details |

## Electricity
**Base URL:** `api/v1/electricity/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `ElectricityListView` | List electricity items |
| `create/` | `ElectricityListCreateView` | Create electricity items |
| `<str:reference>/` | `ElectricityRetrieveUpdateDestroyView` | Electricity item details |

## Builders Plant
**Base URL:** `api/v1/buildersplant/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `BuilderPlantListView` | List builders plant items |
| `create/` | `BuilderPlantListCreateView` | Create builders plant items |
| `<str:reference>/` | `BuilderPlantRetrieveUpdateDestroyView` | Builders plant item details |

## Payment Options
**Base URL:** `api/v1/paymentoptions/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `PaymentOptionListCreateView` | List or create payment options |
| `<str:reference>/` | `PaymentOptionDetailView` | Payment option details |

## Payment Plans
**Base URL:** `api/v1/paymentplans/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `PaymentPlanListCreateView` | List or create payment plans |
| `<str:reference>/` | `PaymentPlanDetailView` | Payment plan details |

## Orders
**Base URL:** `api/v1/orders/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `OrderListCreateView` | List or create orders |
| `<str:reference>/` | `OrderRetrieveUpdateDestroyView` | Order details |

## Order Items
**Base URL:** `api/v1/orderitems/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `OrderItemListCreateView` | List order items |
| `<str:reference>/` | `OrderItemRetrieveUpdateDestroyView` | Order item details |

## Supplier Orders
**Base URL:** `api/v1/supplier-orders/`

| Endpoint | View | Description |
|----------|------|-------------|
| `/` | `SupplierOrderListCreateView` | List orders where user is the supplier |
| `<str:reference>/` | `SupplierOrderRetrieveUpdateDestroyView` | Get details of a supplier order |
