# Azure Database Setup Guide

This guide details how to configure the application to use **Azure SQL Database** (Relational) and **Azure Cosmos DB for MongoDB** (NoSQL).

## 1. Azure SQL Database Setup

The project uses `mssql-django` to connect to Azure SQL Database.

### Prerequisites
- **ODBC Driver 18 for SQL Server** must be installed (see [SETUP.md](SETUP.md) for installation instructions).
- An active Azure SQL Database resource.

### Firewall Configuration
**Important:** You must configure the firewall to allow connections from your environment.

#### Local Development
1. Go to your SQL Server resource in the Azure Portal.
2. Select **Networking** or **Firewalls and virtual networks**.
3. Click **Add your client IPv4 address**.
4. Click **Save**.

#### App Service / Container Apps
To allow your deployed Azure application to connect:
1. In the **Networking** / **Firewalls** section.
2. Check the box **"Allow Azure services and resources to access this server"** (Exception).
   - *Note: This allows connections from any IP allowed by Azure, which is generally safe for PaaS but consider VNET integration for higher security.*
3. Click **Save**.

### Configuration (settings.py)
1. Open `azure_project/settings.py`.
2. Comment out the default SQLite configuration:
   ```python
   # DATABASES = {
   #     'default': {
   #         'ENGINE': 'django.db.backends.sqlite3',
   #         ...
   #     }
   # }
   ```
3. Uncomment and update the Azure SQL configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'mssql',
           'NAME': '<your-database-name>',
           'USER': '<your-admin-username>',
           'PASSWORD': '<your-password>',
           'HOST': '<your-server>.database.windows.net',
           'PORT': '1433',
           'OPTIONS': {
               'driver': 'ODBC Driver 18 for SQL Server',
           },
       },
   }
   ```

---

## 2. Azure Cosmos DB for MongoDB Setup

The project uses `pymongo` to connect to Azure Cosmos DB with the MongoDB API.

### Resource Creation
1. Create a new **Azure Cosmos DB** resource in the Azure Portal.
2. Select **Azure Cosmos DB for MongoDB** as the API.
3. Choose **vCore cluster** or **Request Units (RU)** based on your preference (vCore is generally more compatible with standard Mongo drivers).

### Networking / Firewall
- **Local Development**: Add your public IP to the firewall allowed list under **Networking**.
- **App Service / Container Apps**: Enable **"Allow access from Azure Portal"** (if needed for management) and ensure **"Accept connections from within public Azure datacenters"** is selected (for RU-based) or configure the firewall to allow Azure IPs.
  - *Recommendation*: For production, use **Private Link** or **Virtual Network Integration** for secure connectivity.

### Connection String
1. Navigate to your Cosmos DB resource.
2. Under **Settings**, select **Connection strings**.
3. Copy the **PRIMARY CONNECTION STRING**. It will look like:
   `mongodb://<user>:<password>@<host>:<port>/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@<appname>@`

### Configuration (settings.py)
1. Open `azure_project/settings.py`.
2. Locate the MongoDB configuration section.
3. Update `MONGO_URI` with your connection string:
   ```python
   # MongoDB Configuration
   MONGO_URI = '<your-cosmos-function-string>'
   MONGO_DB_NAME = 'django_store_reviews' # Or your preferred database name
   ```

### Important Note for Cosmos DB (RU-based)
If you are using the Request Unit (RU) based Cosmos DB, ensure you create the database (`django_store_reviews`) and collection (`reviews`) manually in the Data Explorer if `pymongo` does not automatically create them due to permissions or configuration consistency levels.

---

## 3. Querying Data (Azure Portal)

You can view and query your SQL data directly from the Azure Portal using the **Query Editor**.

### Accessing the Query Editor
1. Navigate to your **SQL Database** resource in the Azure Portal.
2. In the left-hand menu, under **Tools** (or sometimes directly at the top level), select **Query editor (preview)**.

### Logging In
1. You will be prompted to login.
2. **Authorization Type**: Select **SQL server authentication**.
3. **Login**: Enter the admin username you created (e.g., `bearlab-admin`).
4. **Password**: Enter your admin password.
5. Click **OK**.

> **Note:** If you see a firewall error, your IP might not be whitelisted.
> - If you are accessing it, you might need to add your current client IP to the firewall rules (see Section 1: Firewall Configuration).
> - Alternatively, check "Allow Azure services and resources to access this server" if you are debugging from another Azure resource, though for the portal, your client IP usually needs to be added.

### Sample Queries

Once logged in, you can run standard T-SQL queries. Here are some examples based on this project's tables:

**List all Stores:**
```sql
SELECT * FROM api_store;
```

**List all Products:**
```sql
SELECT * FROM api_product;
```

**List all Orders:**
```sql
SELECT * FROM api_order;
```

**Join Orders with Users:**
```sql
SELECT 
    o.id as OrderID, 
    u.username as Customer, 
    o.status, 
    o.created_at 
FROM api_order o
JOIN auth_user u ON o.user_id = u.id;
```
