<?php
$serverName = "DESKTOP-NT7IVQ1\SQLEXPRESS";
$connectionInfo = array(
    "Database" => "Lab7WebDB",
    "TrustServerCertificate" => true,
    "LoginTimeout" => 30
);

$conn = sqlsrv_connect($serverName, $connectionInfo);

if ($conn) {
    echo "Connection established.\n";
} else {
    echo "Connection could not be established.\n";
    die(print_r(sqlsrv_errors(), true));
}
?> 