<?php
// Include database connection
require_once 'db_connect.php';

// Check if form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get and sanitize form data
    $title = trim($_POST['title']);
    $author = trim($_POST['author']);
    $pages = intval($_POST['pages']);
    $type = trim($_POST['type']);
    $format = trim($_POST['format']);
    
    // Initialize errors array
    $errors = [];
    
    // Validate input fields
    if (empty($title)) {
        $errors[] = "Title is required";
    }
    if (empty($author)) {
        $errors[] = "Author is required";
    }
    if ($pages <= 0) {
        $errors[] = "Pages must be greater than 0";
    }
    if (empty($type)) {
        $errors[] = "Type is required";
    }
    if (empty($format)) {
        $errors[] = "Format is required";
    }
    
    // If no validation errors, proceed with database insertion
    if (empty($errors)) {
        try {
            // Prepare SQL statement with parameters
            $sql = "INSERT INTO documents (title, author, pages, type, format) VALUES (?, ?, ?, ?, ?)";
            $params = array($title, $author, $pages, $type, $format);
            
            // Execute the query
            $stmt = sqlsrv_query($conn, $sql, $params);
            
            // Check if insertion was successful
            if ($stmt === false) {
                $errors[] = "Error: " . print_r(sqlsrv_errors(), true);
            } else {
                // Redirect to main page on success
                header("Location: index.php");
                exit();
            }
        } catch(Exception $e) {
            $errors[] = "Error: " . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Document</title>
    <!-- Link to external CSS file -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Add New Document</h1>
        
        <!-- Display validation errors if any -->
        <?php if (!empty($errors)): ?>
            <div class="errors">
                <?php foreach ($errors as $error): ?>
                    <p style="color: red;"><?php echo htmlspecialchars($error); ?></p>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
        
        <!-- Document creation form -->
        <form method="POST" action="">
            <!-- Title input field -->
            <div>
                <label for="title">Title:</label>
                <input type="text" id="title" name="title" 
                       value="<?php echo isset($_POST['title']) ? htmlspecialchars($_POST['title']) : ''; ?>" 
                       required>
            </div>
            
            <!-- Author input field -->
            <div>
                <label for="author">Author:</label>
                <input type="text" id="author" name="author" 
                       value="<?php echo isset($_POST['author']) ? htmlspecialchars($_POST['author']) : ''; ?>" 
                       required>
            </div>
            
            <!-- Pages input field -->
            <div>
                <label for="pages">Number of Pages:</label>
                <input type="number" id="pages" name="pages" min="1" 
                       value="<?php echo isset($_POST['pages']) ? htmlspecialchars($_POST['pages']) : ''; ?>" 
                       required>
            </div>
            
            <!-- Document type dropdown -->
            <div>
                <label for="type">Type:</label>
                <select id="type" name="type" required>
                    <option value="">Select Type</option>
                    <option value="PDF" <?php echo (isset($_POST['type']) && $_POST['type'] === 'PDF') ? 'selected' : ''; ?>>PDF</option>
                    <option value="DOC" <?php echo (isset($_POST['type']) && $_POST['type'] === 'DOC') ? 'selected' : ''; ?>>DOC</option>
                    <option value="TXT" <?php echo (isset($_POST['type']) && $_POST['type'] === 'TXT') ? 'selected' : ''; ?>>TXT</option>
                </select>
            </div>
            
            <!-- Document format dropdown -->
            <div>
                <label for="format">Format:</label>
                <select id="format" name="format" required>
                    <option value="">Select Format</option>
                    <option value="Digital" <?php echo (isset($_POST['format']) && $_POST['format'] === 'Digital') ? 'selected' : ''; ?>>Digital</option>
                    <option value="Physical" <?php echo (isset($_POST['format']) && $_POST['format'] === 'Physical') ? 'selected' : ''; ?>>Physical</option>
                </select>
            </div>
            
            <!-- Form submission buttons -->
            <button type="submit">Add Document</button>
            <a href="index.php" style="margin-left: 10px;">Cancel</a>
        </form>
    </div>
</body>
</html> 