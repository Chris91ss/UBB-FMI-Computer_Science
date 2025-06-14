import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-document-filter',
  templateUrl: './document-filter.component.html',
  styleUrl: './document-filter.component.css',
  standalone: true,
  imports: [CommonModule]
})
export class DocumentFilterComponent {
  @Input() type: string = '';
  @Input() format: string = '';
  @Output() filterChange = new EventEmitter<{ type: string, format: string }>();

  onTypeChange(event: any) {
    this.type = event.target.value;
    this.emitChange();
  }
  onFormatChange(event: any) {
    this.format = event.target.value;
    this.emitChange();
  }
  emitChange() {
    this.filterChange.emit({ type: this.type, format: this.format });
  }
}
