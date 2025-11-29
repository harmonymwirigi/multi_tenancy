# Multi-Tenant SaaS Platform - Church Management System

A production-ready Django-based multi-tenant SaaS platform demonstrating enterprise-level architecture patterns for tenant isolation, RBAC, and scalable deployment.

## 🏗️ Architecture Overview

This project showcases a complete multi-tenant SaaS architecture built with Django and PostgreSQL, featuring:

- **PostgreSQL Schema-Based Tenant Isolation** - Each tenant gets their own database schema
- **Role-Based Access Control (RBAC)** - Granular permission system with multiple access levels
- **RESTful API** - Django REST Framework with JWT authentication
- **Real-time Features** - Django Channels with Redis for WebSocket support
- **Background Job Processing** - Scheduled tasks for tenant management
- **Production Deployment** - Docker containerization with Nginx reverse proxy
- **Modern Frontend** - Vue.js SPA with responsive design

## 🔑 Key Multi-Tenancy Features

### 1. Tenant Isolation at Database Level

The platform uses **django-tenants** library with PostgreSQL's schema-based multi-tenancy:

- **Schema-per-tenant architecture**: Each tenant (church) gets an isolated PostgreSQL schema
- **Automatic schema creation**: New tenants automatically get their own schema
- **Query-level isolation**: All queries are automatically scoped to the current tenant's schema
- **Shared and tenant-specific apps**: Clear separation between shared infrastructure and tenant data

**Implementation Details:**
```python
# backend/churchis/settings.py
TENANT_MODEL = "Clients.Client"
TENANT_DOMAIN_MODEL = "Clients.Domain"
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

# Tenant isolation is handled automatically by middleware
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    # ... other middleware
]
```

**Tenant Model:**
```python
# backend/Clients/models.py
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    auto_create_schema = True  # Automatically creates schema on tenant creation
    paid = models.BooleanField(default=False)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
```

**Schema Context Usage:**
```python
# Accessing tenant-specific data with explicit schema context
with schema_context(tenant.schema_name):
    members = Member.objects.all()  # Only returns members for this tenant
```

### 2. Role-Based Access Control (RBAC)

Comprehensive permission system with multiple access levels:

**Permission Levels:**
- **Level 0**: Super Admin - Can view, add and edit everything
- **Level 1**: Finance Admin - Can view, add and edit finances
- **Level 2**: Finance Viewer - Can view finances (read-only)
- **Level 3**: Finance Stats Viewer - Can view finance statistics only
- **Level 4**: Member Viewer - Can view members
- **Level 5**: Regular Member - Basic access

**Implementation:**
```python
# backend/member/models.py
class Role(models.Model):
    PERMISSION_LEVELS = (
        (0, 'can view and edit everything'),
        (1, 'can view and edit finances'),
        (2, 'can view finances'),
        (3, 'can view finances stats'),
        (4, 'can view members'),
        (5, 'member'),
    )
    permission_level = models.SmallIntegerField(default=5, choices=PERMISSION_LEVELS)
    role = models.CharField(max_length=20, default="member", unique=True)
    description = models.TextField(max_length=50, blank=True, null=True)

class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
```

**API Endpoint for Permission Checking:**
```python
# backend/member/api/views/detailviews.py
class GetPermissionLevel(APIView):
    def get(self, request):
        # Returns current user's permission level
        access_level = MemberRole.objects.filter(
            member__member=request.user
        ).values_list('role__permission_level', flat=True).first()
        return Response(access_level)
```

### 3. Background Job Processing

Scheduled background tasks for tenant management and billing:

**Credit Update Job:**
```python
# backend/Clients/management/commands/start_client_credit_update_job.py
class Command(BaseCommand):
    def job(self):
        # Updates client credits daily at midnight
        for client_detail in ClientDetail.objects.all():
            price_per_month = client_detail.tier['price_per_month']
            final_credit = float(initial_credit) - (price_per_month / 30)
            client_detail.credit = final_credit
            client_detail.save()
    
    def scheduleJobs(self):
        schedule.every().day.at("00:00").do(self.job)
```

**Redis Integration:**
- Django Channels for WebSocket support
- Redis channel layer for real-time communication
- Background task queue ready for Celery integration

### 4. Production Deployment Architecture

**Docker Configuration:**
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim
WORKDIR /app
# PostgreSQL client libraries
RUN apt-get update && apt-get install -y gcc libpq-dev
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn
# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "churchis.wsgi:application"]
```

**Nginx Configuration:**
```nginx
# backend/nginx.template.conf
server {
    listen 80;
    server_name church.nanocomputing.co.ke;
    
    location / {
        proxy_pass http://unix:/home/nanoafrika/run/church_is.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
    }
}
```

**Gunicorn Supervisor Configuration:**
- Unix socket for Nginx communication
- Multiple worker processes for handling concurrent requests
- Production-ready logging and error handling

## 📁 Project Structure

```
multi-tenancy/
├── backend/                 # Django backend
│   ├── Clients/            # Tenant management app
│   │   ├── models.py       # Client (Tenant) and Domain models
│   │   └── management/     # Background job commands
│   ├── member/             # Member management with RBAC
│   │   ├── models.py       # Role and MemberRole models
│   │   └── api/            # REST API endpoints
│   ├── finance/            # Finance module (tenant-specific)
│   ├── groups/             # Groups module (tenant-specific)
│   ├── churchis/           # Django project settings
│   │   ├── settings.py     # Multi-tenant configuration
│   │   └── urls.py         # URL routing
│   ├── Dockerfile          # Docker configuration
│   ├── nginx.template.conf # Nginx reverse proxy config
│   └── requirements.txt    # Python dependencies
└── frontend/               # Vue.js frontend
    ├── src/
    │   ├── components/     # Vue components
    │   ├── router/         # Vue Router configuration
    │   └── store/          # Vuex state management
    └── package.json        # Node dependencies
```

## 🚀 Technology Stack

### Backend
- **Django 5.1.6** - Web framework
- **django-tenants 3.7.0** - Multi-tenancy support
- **PostgreSQL** - Database with schema-based isolation
- **Django REST Framework** - RESTful API
- **JWT Authentication** - Secure token-based auth
- **Django Channels** - WebSocket support
- **Redis** - Channel layer and caching
- **Gunicorn** - WSGI HTTP server
- **Docker** - Containerization

### Frontend
- **Vue.js** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Vuex** - State management
- **Axios** - HTTP client

## 🔐 Security Features

- **Tenant Isolation**: Complete data separation at database level
- **JWT Authentication**: Secure token-based authentication
- **CORS Configuration**: Controlled cross-origin resource sharing
- **Permission-Based Access**: Role-based access control at API level
- **Environment Variables**: Sensitive data stored in environment variables

## 📊 Tenant Management

**Tenant Creation:**
- Automatic schema creation on tenant registration
- Domain-based tenant routing
- Subscription and billing tracking
- Credit-based usage monitoring

**Tenant Features:**
- Isolated member management
- Separate finance tracking
- Independent group management
- Tenant-specific SMS services
- Custom website content per tenant

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis
- Node.js 14+
- Docker (optional)

### Backend Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database and Redis credentials
```

4. **Run migrations:**
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure API endpoint:**
Edit `src/helpers.js` with your backend URL

3. **Run development server:**
```bash
npm run serve
```

### Docker Deployment

1. **Build and run:**
```bash
cd backend
docker build -t multi-tenant-backend .
docker run -p 8000:8000 multi-tenant-backend
```

## 📝 API Documentation

The API is documented using Swagger/OpenAPI. Access the interactive documentation at:
- `/swagger/` - Swagger UI
- `/redoc/` - ReDoc

## 🧪 Testing

Run tests for tenant-specific functionality:
```bash
python manage.py test --settings=churchis.settings_test
```

## 📈 Production Considerations

- **Database**: Use PostgreSQL with proper connection pooling
- **Redis**: Configure Redis for production with persistence
- **Nginx**: Set up SSL/TLS certificates
- **Monitoring**: Implement logging and monitoring solutions
- **Backups**: Regular database backups with schema-aware tools
- **Scaling**: Consider horizontal scaling with load balancers

## 🎯 Key Demonstrations

This project demonstrates:

1. ✅ **Multi-tenant user/role systems** - Complete RBAC implementation
2. ✅ **RBAC (Admin / Analyst / Viewer)** - Multiple permission levels
3. ✅ **Tenant isolation with PostgreSQL** - Schema-based isolation
4. ✅ **Background job queues** - Scheduled tasks and async processing
5. ✅ **SaaS-style dashboards** - Vue.js frontend with authentication
6. ✅ **Subscription/billing workflows** - Credit-based billing system

## 📄 License

This project is a demonstration of multi-tenant SaaS architecture patterns.

## 👤 Author

Harmony Mwirigi
- GitHub: [@harmonymwirigi](https://github.com/harmonymwirigi)

---

**Note**: This is a production-ready multi-tenant SaaS platform demonstrating enterprise-level architecture. The codebase showcases real-world patterns for tenant isolation, RBAC, and scalable deployment strategies.

