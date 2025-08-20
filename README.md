# Kudos App — Django Backend

A simple backend for a weekly “kudos” system. Each user gets **3 kudos per week** (not cumulative) to give to teammates in their organization. Includes a minimal REST API and Django Admin.

---

## Tech Stack
- Python 3.11+
- Django 5.x
- Django REST Framework

---

## Features
- Custom `User` (extends `AbstractUser`) with optional `Organization`
- `Kudo(from_user, to_user, message, created_at)`
- Weekly quota logic (3 per ISO week, non-accumulating)
- Endpoints to:
  - Get current user
  - List users (same organization)
  - List kudos (received/given)
  - Give a kudo (enforces weekly quota)
- Django Admin

---

## Quick Start

### 1) Clone & Enter
```bash
git clone https://github.com/pallaviiii0309/Kudos-BE.git
cd KUDOS-BACKEND
py manage.py runserver
```

### 2) create/activate enviroment and install pacakages
```bash
#windows
python -m venv myenv
myenv\Scripts\activate
pip install requirements.txt
```

### 3) For Admin Login
```bash
URL: http://localhost:8000/admin/
USERNAME: admin
PASSWORD: admin@123
```



