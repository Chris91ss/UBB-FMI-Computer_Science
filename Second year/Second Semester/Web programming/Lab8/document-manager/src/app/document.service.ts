import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Document {
  id?: number;
  title: string;
  author: string;
  pages: number;
  type: string;
  format: string;
  created_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = 'http://localhost:8000/'; // <-- Updated to match your PHP backend path

  constructor(private http: HttpClient) { }

  getDocuments(type = '', format = ''): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}api_get_documents.php?type=${type}&format=${format}`);
  }

  addDocument(doc: Document): Observable<any> {
    return this.http.post(`${this.apiUrl}api_add_document.php`, doc);
  }

  editDocument(id: number, doc: Document): Observable<any> {
    return this.http.post(`${this.apiUrl}api_edit_document.php?id=${id}`, doc);
  }

  deleteDocument(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}api_delete_document.php`, { id });
  }
}
