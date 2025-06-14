import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DocumentService, Document } from '../document.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-document-form',
  templateUrl: './document-form.component.html',
  styleUrl: './document-form.component.css',
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class DocumentFormComponent implements OnInit {
  document: Document = { title: '', author: '', pages: 1, type: '', format: '' };
  isEdit = false;
  error = '';
  loading = false;

  constructor(
    private docService: DocumentService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.loading = true;
      this.docService.getDocuments().subscribe(docs => {
        const doc = docs.find(d => d.id == +id);
        if (doc) this.document = doc;
        this.loading = false;
      });
    }
  }

  submit() {
    this.loading = true;
    if (this.isEdit && this.document.id) {
      this.docService.editDocument(this.document.id, this.document).subscribe({
        next: res => { if (res.success) this.router.navigate(['/']); else this.error = 'Update failed'; this.loading = false; },
        error: () => { this.error = 'Update failed'; this.loading = false; }
      });
    } else {
      this.docService.addDocument(this.document).subscribe({
        next: res => { if (res.success) this.router.navigate(['/']); else this.error = 'Add failed'; this.loading = false; },
        error: () => { this.error = 'Add failed'; this.loading = false; }
      });
    }
  }

  cancel() {
    this.router.navigate(['/']);
  }
}
