# Pharmacy Management System (C# WinForms)

A Windows desktop application for managing a retail pharmacy. It supports user authentication (Administrator, Pharmacist), medicine inventory (add, view, update, delete), sales with cart/receipt printing, and visual dashboards.

> Built with .NET Framework 4.7.2 (Windows Forms) and SQL Server. UI components use Guna.UI2 WinForms.

## Features

- **Authentication**
  - Login for Administrator and Pharmacist
  - Default credentials fallback: if no `users` exist, use `root` / `root`

- **Administrator module**
  - **Dashboard**: counts of users by role
  - **Add User**: create Administrator/Pharmacist accounts
  - **View Users**: search, filter, delete users
  - **Profile**: view/update current user profile

- **Pharmacist module**
  - **Dashboard**: chart of valid vs expired medicines
  - **Add Medicine**: create new medicine entries (ID, name, batch, dates, quantity, price)
  - **View Medicine**: search and delete medicines
  - **Update Medicine**: edit medicine details and adjust stock
  - **Medicine Validity Check**: filter by valid/expired/all
  - **Sell Medicine**:
    - Search by name (valid and in-stock only)
    - Auto-fill ID, expiry, unit price
    - Compute total, add to cart, persist stock decrements
    - Purchase & print receipt using DGVPrinter

## Technology

- **Framework**: .NET Framework 4.7.2 (Windows Forms)
- **Database**: Microsoft SQL Server (tested with SQL Server Express)
- **UI Library**: Guna.UI2 WinForms
- **Charts**: System.Windows.Forms.DataVisualization

## Project Structure (high level)

- `Form1.*` — Login form
- `Administrator.*` — Admin shell containing:
  - `Administrator UC/UCADDUSER.*` — Add user
  - `Administrator UC/UC_ViewUser.*` — View/search/delete users
  - `Administrator UC/UC_Profile.*` — View/update profile
  - `Administrator UC/UCDASHBOARD.*` — Admin dashboard
- `Pharmacist.*` — Pharmacist shell containing:
  - `PharmacistUC/UC_P_Dashboard.*` — Valid vs expired chart
  - `PharmacistUC/UC_P_AddMedicine.*` — Add medicine
  - `PharmacistUC/UC_P_ViewMedicine.*` — Search/delete medicines
  - `PharmacistUC/UC_P_UpdateMedicine.*` — Update medicines and stock
  - `PharmacistUC/UC_P_MediValidCheck.*` — Validity filter
  - `PharmacistUC/UC_P_SellMedicine.*` — Sales/cart/printing
- `function.cs` — DB helper (connection, query helpers)
- `DGVPrinter.cs` and `PharmacistUC/DVGPrinter.cs` — Receipt printing
- `App.config` — Connection string
- `database.sql` — Schema and seed data

## Database

- Default database name: `DBMSPHARMA`
- Tables used:
  - `users` (`userRole`, `name`, `dob`, `mobile`, `email`, `username`, `pass`)
  - `medic` (`mid`, `mname`, `mnumber`, `mDate`, `eDate`, `quantity`, `Perunit`)
- A ready-to-run script is provided in `database.sql` to create the database, tables, and sample data (includes a seed admin if no users exist).

## Configuration

Connection string is defined in `App.config` under key `PharmacyDb`:

```xml
<add name="PharmacyDb"
     connectionString="Data Source=localhost\SQLEXPRESS;Initial Catalog=DBMSPHARMA;Integrated Security=True"
     providerName="System.Data.SqlClient" />
```

Update `Data Source` and authentication to match your SQL Server instance.

## Prerequisites

- Windows 10/11
- Visual Studio 2019/2022 with .NET desktop development workload
- .NET Framework 4.7.2 Developer Pack
- SQL Server Express (or any SQL Server instance you can connect to)

## Setup & Run

1. **Clone**
   - Open `PHARMACY 1.sln` in Visual Studio.

2. **Database**
   - Open `database.sql` in SQL Server Management Studio and execute it.
   - Or manually create `DBMSPHARMA` and run the table/seed statements.

3. **Connection String**
   - Edit `App.config` to point to your SQL Server instance.

4. **UI Library (Guna.UI2)**
   - Recommended: install via NuGet: `Guna.UI2.WinForms`
   - Alternatively: keep the existing reference to `bin/Debug/Guna.UI2.dll` (as configured in the project), or update the project reference to point to your installed package/dll.

5. **Build & Run**
   - Set `PHARMACY 1` as the startup project and run.

6. **Login**
   - If `users` table is empty, login with `root` / `root` to access Administrator.
   - Otherwise, use credentials you created in the database or via Add User.

## Notes

- Queries currently use string concatenation; for production, parameterize SQL to prevent injection.
- The app targets Windows; running on non-Windows environments is not supported.

## License

Add a `LICENSE` file if you intend to distribute.

## Credits

- Guna.UI2 WinForms — modern UI controls for WinForms
- DGVPrinter — DataGridView printing helper
