from core.permissions.permissions import IsFarmAdmin, HasRolePermission, IsFarmOwnerOrReadOnly



PERMISSION_MAP = {
    "users": {
        "read": [HasRolePermission("users.view")],
        "write": [HasRolePermission("users.manage")],
    },
    "farm_settings": {
        "read": [HasRolePermission("farm_settings.view")],
        "write": [HasRolePermission("farm_settings.manage")],
    },
    "people": {
        "read": [HasRolePermission("people.view")],
        "write": [HasRolePermission("people.manage")],
    },
    "suppliers": {
        "read": [HasRolePermission("suppliers.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("suppliers.manage")],
    },
    "warehouses": {
        "read": [HasRolePermission("warehouses.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("warehouses.manage")],
    },
    "warehouse_entries": {
        "read": [HasRolePermission("warehouses.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("warehouses.manage")],
    },
    "warehouse_quantity_schedules": {
        "read": [HasRolePermission("warehouses.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("warehouses.manage")],
    },
    "warehouse_reminders": {
        "read": [HasRolePermission("warehouses.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("warehouses.manage")],
    },

    "products": {
        "read": [HasRolePermission("products.view")],
        "write": [IsFarmAdmin(), HasRolePermission("products.manage")],
    },
    "personal_products": {
        "read": [HasRolePermission("products.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("products.manage")],
    },
    "projects": {
        "read": [HasRolePermission("products.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("products.manage")],
    },
    "animals": {
        "read": [HasRolePermission("animals.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("animals.manage")],
    },
    "animal_births": {
        "read": [HasRolePermission("animal_births.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("animal_births.manage")],
    },
    "animal_deaths": {
        "read": [HasRolePermission("animal_deaths.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("animal_deaths.manage")],
    },
    "custom_fields": {
        "read": [HasRolePermission("custom_fields.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("custom_fields.manage")],
    },
    "team": {
        "read": [HasRolePermission("team.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("team.manage")],
    },
    "roles": {
        "read": [HasRolePermission("roles.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("roles.manage")],
    },
    "lands": {
        "read": [HasRolePermission("lands.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("lands.manage")],
    },
    "land_purchases": {
        "read": [HasRolePermission("land_purchases.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("land_purchases.manage")],
    },
    "wilayas": {
        "read": [HasRolePermission("wilayas.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("wilayas.manage")],
    },
    "crop": {
        "read": [HasRolePermission("crop.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("crop.manage")],
    },

    "expenses": {
        "read": [HasRolePermission("finance.view_expenses")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("finance.manage")],
        },
    "receipts": {
        "read": [HasRolePermission("receipts.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("receipts.manage")],
     },
    "payments": {
        "read": [HasRolePermission("payments.manage")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("payments.manage")],
    },
    "revenues": {
        "read": [HasRolePermission("finance.view_revenues")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("finance.manage")],
    },
    "debts": {
        "read": [HasRolePermission("debts.manage")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("debts.view")],
    },
    "invoices": {
        "read": [HasRolePermission("invoices.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("invoices.manage")],
    },
    "subscriptions": {
        "read": [HasRolePermission("finance.view")],
        "write": [IsFarmOwnerOrReadOnly(), HasRolePermission("finance.manage")],
    },
    "finance_reports": {
        "read": [HasRolePermission("finance.view")],
        "write": [IsFarmAdmin()],  # Optional if write is ever needed
    },
     "warehouse": {
        "read": [HasRolePermission("warehouses.view")],
        "write": [IsFarmOwnerOrReadOnly(), IsFarmAdmin(), HasRolePermission("warehouses.manage")],
    },


}
