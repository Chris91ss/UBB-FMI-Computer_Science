# Document Manager

A web application for managing documents built with ASP.NET Core MVC.

## Features

- User authentication (login/register)
- Document management (CRUD operations)
- Document filtering by type and format
- Responsive design using Bootstrap

## Prerequisites

- .NET 7.0 SDK or later
- SQL Server (LocalDB is sufficient for development)
- Visual Studio 2022 or Visual Studio Code

## Setup

1. Clone the repository
2. Open the solution in Visual Studio or your preferred IDE
3. Update the connection string in `appsettings.json` if needed
4. Open a terminal in the project directory and run the following commands:

```bash
dotnet restore
dotnet ef migrations add InitialCreate
dotnet ef database update
dotnet run
```

## Database

The application uses Entity Framework Core with SQL Server. The database will be created automatically when you run the migrations.

## Default User

After running the application for the first time, you'll need to register a new user account to access the document management features.

## Usage

1. Register a new account or login with existing credentials
2. Navigate to the Documents page
3. Use the filter options to find specific documents
4. Create, edit, or delete documents as needed

## Security

- Passwords are hashed using ASP.NET Core Identity
- All document management operations require authentication
- CSRF protection is enabled
- Input validation is implemented on all forms 