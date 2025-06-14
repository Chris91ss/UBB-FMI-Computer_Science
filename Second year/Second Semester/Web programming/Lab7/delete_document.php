<?php
// Include database connection
require_once 'db_connect.php';

// Check if document ID is provided
if (isset($_POST['id'])) {
    $id = intval($_POST['id']);
    
    try {
        // Prepare SQL statement with parameter
        $sql = "DELETE FROM documents WHERE id = ?";
        $params = array($id);
        
        // Execute the query
        $stmt = sqlsrv_query($conn, $sql, $params);
        
        // Check if deletion was successful
        if ($stmt === false) {
            die("Error: " . print_r(sqlsrv_errors(), true));
        }
        
        // Return success response
        echo "success";
    } catch(Exception $e) {
        die("Error: " . $e->getMessage());
    }
} else {
    // If no ID provided, return error
    die("No document ID provided");
}
?> 