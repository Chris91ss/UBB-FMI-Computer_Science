import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DocumentService, Document } from '../document.service';
import { CommonModule } from '@angular/common';
import { DocumentFilterComponent } from '../document-filter/document-filter.component';

@Component({
  selector: 'app-document-list',
  templateUrl: './document-list.component.html',
  styleUrl: './document-list.component.css',
  standalone: true,
  imports: [CommonModule, DocumentFilterComponent]
})
export class DocumentListComponent implements OnInit {
  documents: Document[] = [];
  typeFilter: string = '';
  formatFilter: string = '';
  loading = false;
  error = '';

  constructor(private docService: DocumentService, private router: Router) {}

  ngOnInit() {
    // Load last used filters from localStorage
    this.typeFilter = localStorage.getItem('typeFilter') || '';
    this.formatFilter = localStorage.getItem('formatFilter') || '';
    this.loadDocuments();
  }

  loadDocuments() {
    this.loading = true;
    this.docService.getDocuments(this.typeFilter, this.formatFilter).subscribe({
      next: docs => { this.documents = docs; this.loading = false; },
      error: err => { this.error = 'Failed to load documents'; this.loading = false; }
    });
  }

  onFilterChange(type: string, format: string) {
    this.typeFilter = type;
    this.formatFilter = format;
    localStorage.setItem('typeFilter', type);
    localStorage.setItem('formatFilter', format);
    this.loadDocuments();
  }

  addDocument() {
    this.router.navigate(['/add']);
  }

  editDocument(id: number) {
    this.router.navigate(['/edit', id]);
  }

  deleteDocument(id: number) {
    if (confirm('Are you sure you want to delete this document?')) {
      this.docService.deleteDocument(id).subscribe({
        next: res => { if (res.success) this.loadDocuments(); else alert('Delete failed'); },
        error: err => alert('Delete failed')
      });
    }
  }
}
