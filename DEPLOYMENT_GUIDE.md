# Deployment Guide: Fixing "Failed to Fetch" & File Upload Configuration

## Problem: "Failed to Fetch" Error

### Root Cause Analysis

The "Failed to fetch" error in Next.js occurs when the browser cannot complete the HTTP request. In your setup, the most likely causes are:

1. **Backend not accessible** - Django server not running or wrong URL
2. **CORS blocking** - Django rejecting requests from Next.js origin
3. **Request size too large** - File upload exceeds server limits
4. **Wrong API endpoint** - Incorrect URL in fetch() call
5. **Missing headers** - CORS or content-type issues
6. **Nginx/server timeout** - Upload takes too long

---

## PART 1: FIX THE "FAILED TO FETCH" ERROR

### Step 1: Verify Django is Running

```bash
# Check if Django is running
curl http://localhost:8000/api/registrations/

# Expected: Should return JSON response or 200 OK
# If connection refused: Django is not running
```

**Fix if not running:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### Step 2: Configure CORS in Django (CRITICAL)

Edit `backend/sherullah_service/settings.py`:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",           # Next.js dev
    "http://127.0.0.1:3000",           # Next.js dev
    "http://your-domain.com",          # Production domain
    "https://your-domain.com",         # Production HTTPS
]

# OR for development only (NOT recommended for production):
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### Step 3: Fix Next.js API URL

In your registration form component:

```typescript
// ❌ WRONG - localhost won't work in production
const API_URL = "http://localhost:8000/api/registrations/";

// ✅ CORRECT - Use environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/registrations/";
```

Create `.env.local` in Next.js project:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/registrations/
```

For production, create `.env.production`:
```env
NEXT_PUBLIC_API_URL=https://your-domain.com/api/registrations/
```

### Step 4: Correct Fetch Implementation

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  try {
    const formData = new FormData();
    formData.append('full_name', fullName);
    formData.append('its_number', itsNumber);
    formData.append('email', email);
    formData.append('phone_number', phoneNumber);
    formData.append('preference', preference);
    
    // Add audio files
    audioFiles.forEach((file) => {
      formData.append('audition_files', file);
    });
    
    const response = await fetch(process.env.NEXT_PUBLIC_API_URL!, {
      method: 'POST',
      body: formData,  // ✅ Do NOT set Content-Type header - browser will set it with boundary
      // ❌ WRONG: headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Success:', data);
    setSuccessMessage('Registration submitted successfully!');
    
  } catch (error) {
    console.error('Error:', error);
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      setErrorMessage('Unable to connect to server. Please check your connection and try again.');
    } else {
      setErrorMessage(error instanceof Error ? error.message : 'Registration failed. Please try again.');
    }
  }
};
```

---

## PART 2: RECOMMENDED FILE UPLOAD LIMITS

### Audio Files (Azaan/Takbira Recordings)

**Recommended Settings:**
- **Max files per user**: 5 (as per requirements)
- **Max size per file**: 10 MB
- **Allowed formats**: MP3, M4A, AAC, WAV
- **Recommended quality**: 128 kbps (clear voice, not HD)
- **Typical file size**: 1-3 MB for 1-2 minute recording

**Why these limits?**
- 128 kbps MP3: Crystal clear voice, no distortion
- 10 MB max: Covers even 5+ minute recordings
- Total per user: Max 50 MB (5 files × 10 MB)
- For 100 users: ~5 GB total storage (very safe for VPS)

### Video Files (Optional - if needed)

**Recommended Settings:**
- **Max files per user**: 1-2 (if allowed at all)
- **Max size per file**: 50 MB
- **Allowed formats**: MP4, MOV
- **Recommended quality**: 720p @ 1.5 Mbps (clear, not HD)
- **Typical file size**: 20-30 MB for 2-3 minute video

**Recommendation**: Stick to audio only for this project. Video is not necessary for Azaan/Takbira auditions.

---

## PART 3: DJANGO CONFIGURATION

### Update `backend/sherullah_service/settings.py`

Add these settings:

```python
# ==========================================
# FILE UPLOAD SETTINGS
# ==========================================

# Maximum size of request body (100 MB for safety)
# This covers form data + all files combined
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100 MB

# Maximum size of uploaded file (10 MB per file for audio)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

# Number of files allowed per request
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # Default is usually enough

# Where to store uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Allowed extensions (enforced at model validator level)
ALLOWED_AUDIO_EXTENSIONS = ['mp3', 'm4a', 'aac', 'wav']

# Maximum total files per registration
MAX_AUDITION_FILES = 5
```

### Update Model Validator

In `backend/registrations/models.py`, update the AuditionFile model:

```python
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    """Validate uploaded file size (max 10 MB)"""
    filesize = value.size
    max_size_mb = 10
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if filesize > max_size_bytes:
        raise ValidationError(f'Maximum file size is {max_size_mb}MB. Your file is {filesize / (1024*1024):.2f}MB.')

class AuditionFile(models.Model):
    registration = models.ForeignKey(
        Registration, 
        related_name='audition_files', 
        on_delete=models.CASCADE
    )
    audio_file = models.FileField(
        upload_to='auditions/',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'm4a', 'aac']),
            validate_file_size  # Add size validator
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Audio for {self.registration.full_name}"
```

### Update View to Enforce File Limit

In `backend/registrations/views.py`:

```python
@transaction.atomic
def create(self, request, *args, **kwargs):
    """
    Create new registration with audition file uploads.
    Max 5 audio files allowed.
    """
    from django.conf import settings
    
    # Validate registration data
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    # Create registration
    registration = serializer.save()
    
    # Handle audition file uploads
    files = request.FILES.getlist('audition_files')
    
    max_files = getattr(settings, 'MAX_AUDITION_FILES', 5)
    
    if len(files) > max_files:
        registration.delete()  # Rollback
        return Response(
            {'error': f'Maximum {max_files} audition files allowed. You uploaded {len(files)}.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(files) == 0:
        registration.delete()  # Rollback
        return Response(
            {'error': 'At least 1 audition file is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create audition file records
    for audio_file in files:
        try:
            AuditionFile.objects.create(
                registration=registration,
                audio_file=audio_file
            )
        except ValidationError as e:
            registration.delete()  # Rollback
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Return full registration data
    output_serializer = RegistrationSerializer(registration)
    
    logger.info(f"New registration created: {registration}")
    
    return Response(
        output_serializer.data,
        status=status.HTTP_201_CREATED
    )
```

---

## PART 4: NEXT.JS FRONTEND FIXES

### Add Client-Side File Validation

```typescript
'use client';

import { useState } from 'react';

const MAX_FILES = 5;
const MAX_FILE_SIZE_MB = 10;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
const ALLOWED_FORMATS = ['audio/mpeg', 'audio/mp4', 'audio/aac', 'audio/wav', 'audio/x-m4a'];

export default function RegistrationForm() {
  const [audioFiles, setAudioFiles] = useState<File[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');
  
  const validateFile = (file: File): string | null => {
    // Check file type
    if (!ALLOWED_FORMATS.includes(file.type)) {
      return `Invalid file type: ${file.name}. Please upload MP3, M4A, AAC, or WAV files only.`;
    }
    
    // Check file size
    if (file.size > MAX_FILE_SIZE_BYTES) {
      const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      return `File too large: ${file.name} (${fileSizeMB}MB). Maximum size is ${MAX_FILE_SIZE_MB}MB.`;
    }
    
    return null;
  };
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setErrorMessage('');
    
    const files = Array.from(e.target.files || []);
    
    // Check total count
    if (audioFiles.length + files.length > MAX_FILES) {
      setErrorMessage(`Maximum ${MAX_FILES} files allowed. You have ${audioFiles.length} and selected ${files.length} more.`);
      return;
    }
    
    // Validate each file
    for (const file of files) {
      const error = validateFile(file);
      if (error) {
        setErrorMessage(error);
        return;
      }
    }
    
    setAudioFiles(prev => [...prev, ...files]);
  };
  
  const removeFile = (index: number) => {
    setAudioFiles(prev => prev.filter((_, i) => i !== index));
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');
    
    // Validate before submit
    if (audioFiles.length === 0) {
      setErrorMessage('Please upload at least 1 audition file.');
      return;
    }
    
    if (audioFiles.length > MAX_FILES) {
      setErrorMessage(`Maximum ${MAX_FILES} audition files allowed.`);
      return;
    }
    
    // Show loading state
    setIsSubmitting(true);
    
    try {
      const formData = new FormData();
      formData.append('full_name', fullName);
      formData.append('its_number', itsNumber);
      formData.append('email', email);
      formData.append('phone_number', phoneNumber);
      formData.append('preference', preference);
      
      // Add audio files
      audioFiles.forEach((file) => {
        formData.append('audition_files', file);
      });
      
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/registrations/';
      
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.detail || `Server error: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Registration successful:', data);
      
      setSuccessMessage('Registration submitted successfully! You will receive an email confirmation.');
      
      // Reset form
      setFullName('');
      setItsNumber('');
      setEmail('');
      setPhoneNumber('');
      setPreference('BOTH');
      setAudioFiles([]);
      
    } catch (error) {
      console.error('Registration error:', error);
      
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        setErrorMessage('Unable to connect to server. Please check your internet connection and try again.');
      } else {
        setErrorMessage(error instanceof Error ? error.message : 'Registration failed. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields... */}
      
      {/* File upload section */}
      <div>
        <label>
          Audition Files (Audio only, max {MAX_FILES} files, {MAX_FILE_SIZE_MB}MB each)
        </label>
        <input
          type="file"
          accept="audio/*"
          multiple
          onChange={handleFileChange}
          disabled={audioFiles.length >= MAX_FILES}
        />
        
        {/* Display selected files */}
        {audioFiles.length > 0 && (
          <div>
            <p>{audioFiles.length} / {MAX_FILES} files selected</p>
            <ul>
              {audioFiles.map((file, index) => (
                <li key={index}>
                  {file.name} ({(file.size / (1024 * 1024)).toFixed(2)} MB)
                  <button type="button" onClick={() => removeFile(index)}>Remove</button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      
      {/* Error message */}
      {errorMessage && (
        <div style={{ color: 'red', padding: '10px', border: '1px solid red' }}>
          {errorMessage}
        </div>
      )}
      
      {/* Success message */}
      {successMessage && (
        <div style={{ color: 'green', padding: '10px', border: '1px solid green' }}>
          {successMessage}
        </div>
      )}
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit Registration'}
      </button>
    </form>
  );
}
```

---

## PART 5: HOSTINGER VPS CONFIGURATION

### Nginx Configuration (if using Nginx)

Edit `/etc/nginx/sites-available/your-site`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Upload size limits
    client_max_body_size 100M;  # Allow up to 100MB uploads
    client_body_timeout 300s;    # 5 minutes for large uploads
    
    # Django backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Upload timeouts
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
    }
    
    # Media files
    location /media/ {
        alias /path/to/backend/media/;
        expires 30d;
    }
    
    # Next.js frontend (if serving through Nginx)
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Gunicorn Configuration (if using Gunicorn)

Create `gunicorn.conf.py`:

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 2  # Low for small VPS
worker_class = "sync"
timeout = 300  # 5 minutes for uploads
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
```

Run Gunicorn:
```bash
gunicorn sherullah_service.wsgi:application -c gunicorn.conf.py
```

### VPS Resource Expectations

**For your use case (30 days, ~100 users):**

| Resource | Expected Usage | Recommendation |
|----------|----------------|----------------|
| Storage | 5-10 GB | Safe with 20GB+ VPS |
| RAM | 512 MB - 1 GB | 1-2 GB VPS sufficient |
| CPU | Minimal | 1 vCPU enough |
| Bandwidth | ~5-10 GB/month | Non-issue for most VPS |

**Why this is VPS-safe:**
- Total audio: ~5 GB (100 users × 5 files × 10 MB max)
- Database: < 100 MB
- Django + Next.js: ~500 MB RAM combined
- No video streaming, no heavy processing
- Short-term (30 days) usage

---

## PART 6: QUALITY GUIDELINES FOR USERS

Create a user guide document:

### Audio Recording Guidelines

**Recommended Settings:**
- **Format**: MP3
- **Bitrate**: 128 kbps (standard quality)
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono (sufficient for voice)
- **Duration**: 1-3 minutes per file

**Recording Tips:**
- Use smartphone voice recorder (built-in app)
- Record in quiet environment
- Hold phone 6-8 inches from mouth
- Speak clearly and naturally
- Export as MP3 at "Standard" or "Good" quality

**File Size Examples:**
- 1 minute @ 128 kbps MP3: ~1 MB
- 2 minutes @ 128 kbps MP3: ~2 MB
- 3 minutes @ 128 kbps MP3: ~3 MB

These files will be crystal clear for listening while keeping sizes reasonable.

---

## TROUBLESHOOTING CHECKLIST

### If "Failed to fetch" persists:

1. **Check Django is running:**
   ```bash
   curl http://localhost:8000/api/registrations/
   ```

2. **Check CORS headers in browser:**
   - Open DevTools → Network tab
   - Submit form
   - Check OPTIONS request
   - Look for `Access-Control-Allow-Origin` header

3. **Check file sizes:**
   - Verify files are under 10 MB each
   - Verify total upload is under 100 MB

4. **Check browser console:**
   - Look for CORS errors
   - Look for 413 (Payload Too Large) errors
   - Look for 500 (Server Error) errors

5. **Check Django logs:**
   ```bash
   tail -f backend/logs/django.log
   ```

6. **Test with small file first:**
   - Upload 1 small file (< 1 MB)
   - If works, issue is file size limits
   - If fails, issue is CORS or connectivity

### Common Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Failed to fetch | CORS not configured | Add CORS_ALLOWED_ORIGINS |
| 413 Payload Too Large | Nginx limit | Set client_max_body_size |
| 400 Bad Request | File validation failed | Check file type/size |
| 500 Server Error | Django crash | Check Django logs |
| Connection refused | Backend not running | Start Django server |

---

## PRODUCTION DEPLOYMENT CHECKLIST

Before going live:

- [ ] Update CORS_ALLOWED_ORIGINS with production domain
- [ ] Set NEXT_PUBLIC_API_URL in production .env
- [ ] Configure Nginx with proper limits
- [ ] Set up Gunicorn with timeout
- [ ] Create media/ directory with proper permissions
- [ ] Test file upload with different sizes
- [ ] Test from different browsers
- [ ] Monitor disk space during testing
- [ ] Set up automatic backups for media files
- [ ] Test HTTPS (if configured)

---

## SUMMARY

### File Size Limits (Final Recommendations)
```python
# Django settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100 MB total
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB per file
MAX_AUDITION_FILES = 5
```

```nginx
# Nginx
client_max_body_size 100M;
```

```typescript
// Next.js
const MAX_FILE_SIZE_MB = 10;
const MAX_FILES = 5;
```

### Why These Limits Work

1. **Audio quality**: 128 kbps MP3 is CD-quality for voice
2. **Storage**: 100 users × 50 MB = 5 GB (very manageable)
3. **Upload speed**: 10 MB uploads in < 30 seconds on normal connection
4. **VPS friendly**: Minimal RAM/CPU impact
5. **User friendly**: No unnecessary restrictions, but safe

Your app will run smoothly for the 30-day Ramazaan period without issues! 🕌
