// Function to load documents from the server using AJAX
// Parameters:
//   type: optional filter for document type
//   format: optional filter for document format
function loadDocuments(type = '', format = '') {
    // Create new XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    // Set up GET request to get_documents.php with filter parameters
    xhr.open('GET', `get_documents.php?type=${type}&format=${format}`, true);
    
    // Define what happens when the request completes
    xhr.onload = function() {
        if (this.status === 200) {
            // If successful, update the document list with the response
            document.getElementById('documentList').innerHTML = this.responseText;
        }
    }
    
    // Send the request
    xhr.send();
}

// Function to handle filter changes
// Called when either type or format filter is changed
function filterDocuments() {
    // Get current values from both filter dropdowns
    const type = document.getElementById('typeFilter').value;
    const format = document.getElementById('formatFilter').value;
    // Load documents with the selected filters
    loadDocuments(type, format);
}

// Function to handle document deletion
// Parameter:
//   id: the ID of the document to delete
function deleteDocument(id) {
    // Show confirmation dialog
    if (confirm('Are you sure you want to delete this document?')) {
        // Create new XMLHttpRequest object
        const xhr = new XMLHttpRequest();
        // Set up POST request to delete_document.php
        xhr.open('POST', 'delete_document.php', true);
        // Set content type for POST data
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        
        // Define what happens when the request completes
        xhr.onload = function() {
            if (this.status === 200) {
                if (this.responseText.trim() === 'success') {
                    // If successful, reload the document list
                    filterDocuments();
                } else {
                    // If there was an error, show it to the user
                    alert('Error deleting document: ' + this.responseText);
                }
            } else {
                alert('Error: Server returned status ' + this.status);
            }
        }
        
        // Handle network errors
        xhr.onerror = function() {
            alert('Network error occurred while trying to delete the document');
        }
        
        // Send the request with the document ID
        xhr.send('id=' + id);
    }
}

// Function to navigate to edit page for a document
// Parameter:
//   id: the ID of the document to edit
function editDocument(id) {
    // Redirect to edit page with document ID
    window.location.href = 'edit_document.php?id=' + id;
}

// Load documents when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadDocuments();
}); 