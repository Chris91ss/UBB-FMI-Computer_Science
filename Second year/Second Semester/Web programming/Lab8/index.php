<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Management System</title>
    <!-- Link to external CSS file for styling -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Main container for the entire application -->
    <div class="container">
        <h1>Document Management System</h1>
        
        <!-- Navigation menu -->
        <nav>
            <a href="index.php">Home</a>
            <a href="add_document.php">Add Document</a>
        </nav>

        <!-- Filter section for document type and format -->
        <div class="filters">
            <!-- Dropdown for filtering by document type -->
            <select id="typeFilter" onchange="filterDocuments()">
                <option value="">All Types</option>
                <option value="PDF">PDF</option>
                <option value="DOC">DOC</option>
                <option value="TXT">TXT</option>
            </select>
            
            <!-- Dropdown for filtering by document format -->
            <select id="formatFilter" onchange="filterDocuments()">
                <option value="">All Formats</option>
                <option value="Digital">Digital</option>
                <option value="Physical">Physical</option>
            </select>
        </div>

        <!-- Container for document list, populated via AJAX -->
        <div id="documentList">
            <!-- Documents will be loaded here via AJAX -->
        </div>
    </div>

    <!-- Link to external JavaScript file for AJAX and interactivity -->
    <script src="script.js"></script>
</body>
</html> 