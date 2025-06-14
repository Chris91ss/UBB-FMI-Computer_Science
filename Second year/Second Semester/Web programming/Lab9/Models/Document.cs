using System.ComponentModel.DataAnnotations;

namespace DocumentManager.Models
{
    public class Document
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string Title { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        public string Author { get; set; } = string.Empty;

        [Required]
        public int NumberOfPages { get; set; }

        [Required]
        [StringLength(50)]
        public string Type { get; set; } = string.Empty;

        [Required]
        [StringLength(20)]
        public string Format { get; set; } = string.Empty;

        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public DateTime? UpdatedAt { get; set; }
    }
} 