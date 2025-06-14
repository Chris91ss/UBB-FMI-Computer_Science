<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }
require_once 'db_connect.php';
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    $id = intval($data['id'] ?? 0);
    if ($id > 0) {
        $sql = "DELETE FROM documents WHERE id = ?";
        $params = array($id);
        $stmt = sqlsrv_query($conn, $sql, $params);
        if ($stmt === false) {
            echo json_encode(['success' => false, 'error' => sqlsrv_errors()]);
        } else {
            echo json_encode(['success' => true]);
        }
    } else {
        echo json_encode(['success' => false, 'error' => 'Invalid document ID']);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Invalid request method']);
}
?> 