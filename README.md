# 💊 Pharmacy Management System

A comprehensive Windows Forms application built with C# for managing pharmacy operations, including medicine inventory, sales, user management, and more.

## 📋 Overview

This Pharmacy Management System is designed to streamline pharmacy operations with separate interfaces for Administrators and Pharmacists. The system provides complete medicine inventory management, user management, sales tracking, and medicine validity monitoring.

## ✨ Features

### 👨‍💼 Administrator Module
- **Dashboard**: Overview of system statistics and operations
- **User Management**: Add, view, and manage system users
- **Profile Management**: View and update administrator profile
- **Role-based Access Control**: Manage pharmacist and administrator accounts

### 👨‍⚕️ Pharmacist Module
- **Dashboard**: Quick access to pharmacy statistics
- **Medicine Management**:
  - Add new medicines to inventory
  - View all medicines in stock
  - Update medicine information
  - Check medicine validity/expiry dates
- **Sales Operations**:
  - Sell medicines
  - Generate bills and receipts
  - Print invoices using DGV Printer

## 🛠️ Technology Stack

- **Language**: C# (.NET Framework 4.7.2)
- **UI Framework**: Windows Forms with Guna.UI2
- **Database**: SQL Server (DBMSPHARMA)
- **IDE**: Visual Studio 2015+

## 📦 Prerequisites

Before running this application, ensure you have:

1. **Visual Studio 2015 or later** with .NET Framework 4.7.2
2. **SQL Server** (2012 or later recommended)
3. **Guna.UI2 Library** (included in `bin/Debug/Guna.UI2.dll`)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pharmacy-management-system
```

### 2. Database Setup
1. Open SQL Server Management Studio (SSMS)
2. Execute the `database.sql` script to create the database and tables
3. The script will create:
   - `DBMSPHARMA` database
   - `users` table for authentication and user management
   - `medic` table for medicine inventory
   - Default admin account (username: `root`, password: `root`)

### 3. Configure Database Connection
Update the connection string in your application:
- Default server: `localhost` (SQL Server)
- Database: `DBMSPHARMA`
- Authentication: Windows Authentication (modify in code if using SQL Server Authentication)

### 4. Build and Run
1. Open `PHARMACY 1.sln` in Visual Studio
2. Restore NuGet packages if needed
3. Build the solution (F6)
4. Run the application (F5)

## 📂 Project Structure

```
PHARMACY 1/
├── Administrator UC/          # Administrator user controls
│   ├── UCDASHBOARD.cs        # Administrator dashboard
│   ├── UCADDUSER.cs          # Add new users
│   ├── UC_ViewUser.cs        # View all users
│   └── UC_Profile.cs         # User profile management
├── PharmacistUC/             # Pharmacist user controls
│   ├── UC_P_Dashboard.cs     # Pharmacist dashboard
│   ├── UC_P_AddMedicine.cs   # Add new medicines
│   ├── UC_P_ViewMedicine.cs  # View medicine inventory
│   ├── UC_P_UpdateMedicine.cs # Update medicine details
│   ├── UC_P_MediValidCheck.cs # Check medicine validity
│   ├── UC_P_SellMedicine.cs  # Sell medicines
│   └── DVGPrinter.cs         # Print functionality
├── Administrator.cs           # Administrator form
├── Pharmacist.cs             # Pharmacist form
├── Form1.cs                  # Login form
├── Forgot Passward.cs        # Password recovery
├── function.cs               # Helper functions
├── DGVPrinter.cs            # DataGridView printing utility
├── Program.cs               # Application entry point
├── database.sql             # Database schema
└── bin/Debug/
    └── Guna.UI2.dll         # UI library
```

## 🔑 Default Credentials

**Administrator Account:**
- Username: `root`
- Password: `root`

⚠️ **Important**: Change the default password after first login for security purposes.

## 💾 Database Schema

### Users Table
```sql
- id (INT, Primary Key)
- userRole (NVARCHAR) - Administrator/Pharmacist
- name (NVARCHAR)
- dob (DATE)
- mobile (BIGINT)
- email (NVARCHAR)
- username (NVARCHAR, Unique)
- pass (NVARCHAR)
```

### Medicine Table
```sql
- id (INT, Primary Key)
- mid (NVARCHAR, Unique) - Medicine ID
- mname (NVARCHAR) - Medicine Name
- mnumber (NVARCHAR) - Medicine Number/Batch
- mDate (DATE) - Manufacturing Date
- eDate (DATE) - Expiry Date
- quantity (BIGINT) - Stock Quantity
- Perunit (BIGINT) - Price Per Unit
```

## 🎯 Key Functionalities

### Medicine Management
- Add medicines with complete details (ID, name, batch number, dates, quantity, price)
- Update existing medicine information
- Monitor medicine expiry dates
- Track inventory levels
- View complete medicine list with search functionality

### Sales Management
- Process medicine sales
- Generate itemized bills
- Print receipts and invoices
- Automatic inventory updates

### User Management
- Add new users (Administrators and Pharmacists)
- Assign roles and permissions
- View all registered users
- Update user profiles

## 🖥️ System Requirements

**Minimum:**
- OS: Windows 7 or later
- RAM: 2 GB
- Storage: 100 MB free space
- .NET Framework 4.7.2

**Recommended:**
- OS: Windows 10/11
- RAM: 4 GB or more
- Storage: 500 MB free space
- SQL Server 2016 or later

## 🔧 Configuration

### Database Connection
Update the connection string in `function.cs` or relevant data access files:
```csharp
string connectionString = "Data Source=localhost;Initial Catalog=DBMSPHARMA;Integrated Security=True";
```

### UI Customization
The application uses Guna.UI2 framework for modern UI components. Customize colors, themes, and styles through the Designer files (.Designer.cs).

## 📝 Usage Guide

### For Administrators:
1. Login with administrator credentials
2. Access Dashboard for system overview
3. Add new users (pharmacists or administrators)
4. View and manage existing users
5. Update profile information

### For Pharmacists:
1. Login with pharmacist credentials
2. View Dashboard for quick stats
3. Manage medicine inventory:
   - Add new medicines
   - Update medicine details
   - Check expiry dates
4. Process sales and generate bills
5. Print invoices for customers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is available for educational and commercial use.

## 👥 Contact

For questions or support, please open an issue in the repository.

## 🔒 Security Notes

- Change default credentials immediately after installation
- Use strong passwords for all user accounts
- Regularly backup the database
- Keep SQL Server updated with latest security patches
- Implement proper network security for production deployment

## 🐛 Known Issues

- None currently reported

## 📅 Version History

- **v1.0**: Initial release with core functionality
  - User authentication
  - Medicine management
  - Sales processing
  - Inventory tracking

---

**Built with ❤️ for efficient pharmacy management**
