from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates a superuser for a specific tenant."

    def handle(self, *args, **options):
        tenant_schema = 'newchurch'  # Replace with your tenant's schema name
        
        # Activate the tenant's schema (this is crucial!)
        #  The method to activate the schema depends on your django-tenant-schemas setup
        #  The below method is correct
        from django_tenant_schemas.utils import run_on_tenant
        run_on_tenant(tenant_schema, lambda: call_command('createsuperuser'))
        
        self.stdout.write(self.style.SUCCESS(f"Superuser created for tenant schema '{tenant_schema}'"))