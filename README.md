# 🧾 Django Automatic Resume Builder

A Django-based web application that automatically generates resumes by fetching employee and project details from a database. Users can search for an employee by ID or name, and generate a downloadable PDF resume with one click.

---

## 🔧 Technologies Used

| Feature         | Technology           |
|-----------------|----------------------|
| Framework       | Django               |
| PDF Generation  | xhtml2pdf, WeasyPrint|
| Styling         | HTML, CSS, Bootstrap |
| Search Feature  | JavaScript / Django Query |
| Database        | SQLite               |

---

## 📚 Libraries Used for PDF Generation

### ✅ xhtml2pdf
- Converts HTML templates to PDF.
- Used to render dynamic resume data with Django templates.

### ✅ WeasyPrint
- Advanced rendering engine that supports modern HTML & CSS.
- Used for high-quality PDF export with better layout precision.

> You can choose either xhtml2pdf or WeasyPrint depending on your layout and styling needs.

---

## 💼 Features

- Fetch employee details (summary, personal, technical)
- Fetch project details
- Map employees to projects
- Search employee by name or ID
- One-click resume download in PDF format
- Clean and customizable resume layout

---

