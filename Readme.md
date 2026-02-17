# 📘 Ramzaan Registration Form – Production Guide

This guide documents the procedures for managing the live production environment of the Ramzaan Registration Form system.

## 📂 Project Structure

```text
/var/www/Ramzaan_Registration_Form/
│
├── backend/              # Django backend
│   ├── venv/             # Python virtual environment
│   ├── registrations/    # Main Django app
│   ├── media/            # Uploaded audition files (audition files/)
│   ├── staticfiles/      # Collected static files
│   └── manage.py
│
├── public_html/          # PHP frontend
│
└── Readme.md             # This production guide
```

## 🚀 How to Restart Backend (Gunicorn)

**Service name:** `sherullah-backend.service`

### Safe restart:

```bash
sudo systemctl restart sherullah-backend.service
```

### Check status:

```bash
sudo systemctl status sherullah-backend.service
```

### View logs:

```bash
journalctl -u sherullah-backend.service -n 100 --no-pager
```

## 🔁 How to Restart Celery Worker

**Service name:** `sherullah-celery.service`

### Restart:

```bash
sudo systemctl restart sherullah-celery.service
```

### Check status:

```bash
sudo systemctl status sherullah-celery.service
```

### View logs:

```bash
journalctl -u sherullah-celery.service -n 100 --no-pager
```

## 🌐 How to Reload Nginx Safely

### Reload (NO downtime):

```bash
sudo systemctl reload nginx
```

### Check status:

```bash
sudo systemctl status nginx
```

## 🛠 How to Apply Django Migrations (SAFE)

### Navigate to backend:

```bash
cd /var/www/Ramzaan_Registration_Form/backend
source venv/bin/activate
```

### Make migrations:

```bash
python manage.py makemigrations
```

### Apply migrations:

```bash
python manage.py migrate
```

### Then restart backend:

```bash
sudo systemctl restart sherullah-backend.service
```

⚠ **Never delete migration files in production.**

## 🧪 How to Run Django Shell

```bash
cd /var/www/Ramzaan_Registration_Form/backend
source venv/bin/activate
python manage.py shell
```

## 📦 How to Pull Latest Code from GitHub

```bash
cd /var/www/Ramzaan_Registration_Form
git pull origin main
```

### Then restart backend + celery:

```bash
sudo systemctl restart sherullah-backend.service
sudo systemctl restart sherullah-celery.service
```

## 🔐 Environment Variables Location

`/var/www/Ramzaan_Registration_Form/backend/.env`

⚠ **Never commit .env to GitHub.**

## 📊 Where Uploaded Files Are Stored

`/var/www/Ramzaan_Registration_Form/backend/media/`

Do **NOT** delete files manually from this folder.

## ⚠ Important Production Safety Rules

- **Never** drop database tables manually.
- **Never** delete the `backend/media/` folder.
- **Never** remove migration files from `registrations/migrations/`.
- **Always** test with one test user after any deployment.
- **Always** monitor logs immediately after a service restart.
- **Use `reload`** instead of `restart` for Nginx whenever possible.
- **Keep a backup** of the database and media folder before major updates.

## 🧯 Emergency Recovery

### If backend fails (502/504 Bad Gateway):

```bash
sudo systemctl restart sherullah-backend.service
journalctl -u sherullah-backend.service -xe
```

### If Celery fails (Notifications not sending):

```bash
sudo systemctl restart sherullah-celery.service
journalctl -u sherullah-celery.service -xe
```

## 🧠 Deployment Order (Safe)

1. **Pull** latest code (`git pull`).
2. **Apply** migrations (`python manage.py migrate`).
3. **Restart** backend (`sudo systemctl restart sherullah-backend.service`).
4. **Restart** Celery (`sudo systemctl restart sherullah-celery.service`).
5. **Reload** Nginx (`sudo systemctl reload nginx`).
6. **Test** with one registration.
7. **Monitor** logs for any errors.
