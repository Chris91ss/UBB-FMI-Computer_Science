<?php
// Include database connection
require_once 'db_connect.php';

// Get filter parameters from URL
$type = isset($_GET['type']) ? $_GET['type'] : '';
$format = isset($_GET['format']) ? $_GET['format'] : '';

// Base SQL query
$sql = "SELECT * FROM documents WHERE 1=1";
$params = array();

// Add type filter if specified
if (!empty($type)) {
    $sql .= " AND type = ?";
    $params[] = $type;
}

// Add format filter if specified
if (!empty($format)) {
    $sql .= " AND format = ?";
    $params[] = $format;
}

// Add ordering by creation date
$sql .= " ORDER BY created_at DESC";

try {
    // Execute the query with parameters
    $stmt = sqlsrv_query($conn, $sql, $params);
    
    // Check if query execution was successful
    if ($stmt === false) {
        die(print_r(sqlsrv_errors(), true));
    }
    
    // Loop through results and generate HTML for each document
    while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC)) {
        // Start document item container
        echo '<div class="document-item">';
        // Display document title
        echo '<h3>' . htmlspecialchars($row['title']) . '</h3>';
        // Display document details
        echo '<p><strong>Author:</strong> ' . htmlspecialchars($row['author']) . '</p>';
        echo '<p><strong>Pages:</strong> ' . htmlspecialchars($row['pages']) . '</p>';
        echo '<p><strong>Type:</strong> ' . htmlspecialchars($row['type']) . '</p>';
        echo '<p><strong>Format:</strong> ' . htmlspecialchars($row['format']) . '</p>';
        // Add action buttons
        echo '<div class="document-actions">';
        echo '<button onclick="editDocument(' . $row['id'] . ')">Edit</button>';
        echo '<button class="delete-btn" onclick="deleteDocument(' . $row['id'] . ')">Delete</button>';
        echo '</div>';
        echo '</div>';
    }
} catch(Exception $e) {
    // Handle any errors that occur
    echo "Error: " . $e->getMessage();
}
?> 