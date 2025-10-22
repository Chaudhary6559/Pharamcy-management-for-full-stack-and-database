## Pharmacy Management (WinForms, .NET Framework 4.7.2)

This is a Windows Forms app for basic pharmacy management with two roles: Administrator and Pharmacist. It uses SQL Server for data and Guna.UI2 controls for UI. Printing is supported via an embedded `DGVPrinter` helper.

### Prerequisites
- Windows with .NET Framework 4.7.2 Developer Pack
- SQL Server (Express is fine) with local access
- Visual Studio 2019/2022 (Desktop development with C# workload)

### Getting started
1. Open the solution `PHARMACY 1.sln` in Visual Studio.
2. Ensure the `Guna.UI2.dll` exists under `bin/Debug/`. The project references it from there and will copy-local at build time. If you prefer another location, update the project reference `HintPath` accordingly.
3. Set up the database:
   - In SQL Server, run the script `database.sql`. It will create database `DBMSPHARMA`, required tables, and seed a default admin.
4. Configure connection string (optional):
   - Default is `Data Source=localhost\SQLEXPRESS;Initial Catalog=DBMSPHARMA;Integrated Security=True`.
   - To change, edit `App.config` key `PharmacyDb`.
5. Build and run. The startup form is `Form1` (login).

### Login
- If no users exist, you can login with:
  - Username: `root`
  - Password: `root`
- Otherwise, login with created users. Admin can add users via Administrator -> Add User.

### Notable files
- `function.cs`: Central DB access (reads from `App.config` connection string `PharmacyDb`).
- `PharmacistUC/*`: Pharmacist user controls (add/view/update/sell/validity check/dashboard).
- `Administrator UC/*`: Admin user controls (dashboard, add user, view user, profile).
- `DGVPrinter.cs`: Embedded DataGridView printing helper.

### Changes made in this repository
- Read DB connection string from `App.config` instead of hard-coded.
- Fixed SQL typos (quantity numeric compare and missing quote), and a profile update binding bug.
- Adjusted Guna UI reference to `bin/Debug/Guna.UI2.dll` and added `System.Configuration` reference.
- Added `database.sql` for quick setup.

### Troubleshooting
- Can’t connect to SQL Server: update `App.config` connection string to your server name/instance.
- Missing `Guna.UI2.dll`: place it at `bin/Debug/` or update the project reference path.
- Printing issues: ensure printers are installed and the `DGVPrinter` is used on a populated `DataGridView`.

### Security note
This sample uses concatenated SQL for clarity and to reflect the original code. For production, use parameterized queries and hashed passwords.
