using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using DocumentManager.Models;

namespace DocumentManager.Data
{
    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Document> Documents { get; set; }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            // Seed some initial document types and formats
            builder.Entity<Document>().HasData(
                new Document
                {
                    Id = 1,
                    Title = "Sample Document",
                    Author = "Admin",
                    NumberOfPages = 10,
                    Type = "Report",
                    Format = "PDF",
                    CreatedAt = DateTime.Now
                }
            );
        }
    }
} 