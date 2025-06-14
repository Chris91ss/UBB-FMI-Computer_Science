<?php
// Database connection configuration
// Using Windows Authentication with SQL Server Express
$serverName = "DESKTOP-NT7IVQ1\SQLEXPRESS";
$connectionInfo = array(
    "Database" => "Lab7WebDB",        // Name of the database to connect to
    "TrustServerCertificate" => true,  // Skip certificate validation for development
    "LoginTimeout" => 30,             // Maximum time to wait for connection in seconds
    "CharacterSet" => "UTF-8"         // Character encoding for the connection
);

try {
    // Attempt to establish connection to SQL Server
    $conn = sqlsrv_connect($serverName, $connectionInfo);
    
    // Check if connection was successful
    if ($conn === false) {
        // If connection failed, print detailed error information
        die(print_r(sqlsrv_errors(), true));
    }
} catch(Exception $e) {
    // Catch any other exceptions that might occur during connection
    echo "Connection failed: " . $e->getMessage();
    die();
}
?> 