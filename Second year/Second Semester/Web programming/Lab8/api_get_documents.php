<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }
require_once 'db_connect.php';
header('Content-Type: application/json');

$type = isset($_GET['type']) ? $_GET['type'] : '';
$format = isset($_GET['format']) ? $_GET['format'] : '';

$sql = "SELECT * FROM documents WHERE 1=1";
$params = array();
if (!empty($type)) { $sql .= " AND type = ?"; $params[] = $type; }
if (!empty($format)) { $sql .= " AND format = ?"; $params[] = $format; }
$sql .= " ORDER BY created_at DESC";

$stmt = sqlsrv_query($conn, $sql, $params);
$documents = [];
if ($stmt !== false) {
    while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC)) {
        $documents[] = $row;
    }
}
echo json_encode($documents);
?> 