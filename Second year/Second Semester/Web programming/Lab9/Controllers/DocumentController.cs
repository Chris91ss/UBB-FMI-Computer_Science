using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DocumentManager.Data;
using DocumentManager.Models;

namespace DocumentManager.Controllers
{
    [Authorize]
    public class DocumentController : Controller
    {
        private readonly ApplicationDbContext _context;

        public DocumentController(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index(string type, string format)
        {
            ViewBag.CurrentType = type;
            ViewBag.CurrentFormat = format;
            ViewBag.Types = _context.Documents.Select(d => d.Type).Distinct().ToList();
            ViewBag.Formats = _context.Documents.Select(d => d.Format).Distinct().ToList();

            var documents = _context.Documents.AsQueryable();

            if (!string.IsNullOrEmpty(type))
            {
                documents = documents.Where(d => d.Type == type);
            }

            if (!string.IsNullOrEmpty(format))
            {
                documents = documents.Where(d => d.Format == format);
            }

            return View(await documents.ToListAsync());
        }

        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Document document)
        {
            if (ModelState.IsValid)
            {
                document.CreatedAt = DateTime.Now;
                _context.Add(document);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(document);
        }

        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var document = await _context.Documents.FindAsync(id);
            if (document == null)
            {
                return NotFound();
            }
            return View(document);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Document document)
        {
            if (id != document.Id)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    document.UpdatedAt = DateTime.Now;
                    _context.Update(document);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!DocumentExists(document.Id))
                    {
                        return NotFound();
                    }
                    else
                    {
                        throw;
                    }
                }
                return RedirectToAction(nameof(Index));
            }
            return View(document);
        }

        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var document = await _context.Documents
                .FirstOrDefaultAsync(m => m.Id == id);
            if (document == null)
            {
                return NotFound();
            }

            return View(document);
        }

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var document = await _context.Documents.FindAsync(id);
            if (document != null)
            {
                _context.Documents.Remove(document);
                await _context.SaveChangesAsync();
            }
            return RedirectToAction(nameof(Index));
        }

        private bool DocumentExists(int id)
        {
            return _context.Documents.Any(e => e.Id == id);
        }
    }
} 