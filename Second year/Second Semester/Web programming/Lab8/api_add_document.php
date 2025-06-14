<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }
require_once 'db_connect.php';
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    $title = trim($data['title'] ?? '');
    $author = trim($data['author'] ?? '');
    $pages = intval($data['pages'] ?? 0);
    $type = trim($data['type'] ?? '');
    $format = trim($data['format'] ?? '');
    $errors = [];
    if (empty($title)) $errors[] = 'Title is required';
    if (empty($author)) $errors[] = 'Author is required';
    if ($pages <= 0) $errors[] = 'Pages must be greater than 0';
    if (empty($type)) $errors[] = 'Type is required';
    if (empty($format)) $errors[] = 'Format is required';
    if (empty($errors)) {
        $sql = "INSERT INTO documents (title, author, pages, type, format) VALUES (?, ?, ?, ?, ?)";
        $params = array($title, $author, $pages, $type, $format);
        $stmt = sqlsrv_query($conn, $sql, $params);
        if ($stmt === false) {
            echo json_encode(['success' => false, 'error' => sqlsrv_errors()]);
        } else {
            echo json_encode(['success' => true]);
        }
    } else {
        echo json_encode(['success' => false, 'error' => $errors]);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Invalid request method']);
}
?> 