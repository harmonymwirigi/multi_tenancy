# from django.core.management.base import BaseCommand
# from Clients.models import Client, Domain
# from django.utils import timezone

# class Command(BaseCommand):
#     help = 'Creates the initial public tenant'

#     def handle(self, *args, **options):
#         try:
#             # Check if the public tenant already exists
#             if not Client.objects.filter(schema_name='public').exists():
#                 # Create the public tenant
#                 tenant = Client(
#                     schema_name='public',
#                     name='Schemas Inc.',
#                     paid_until=timezone.datetime(2024, 12, 5, tzinfo=timezone.utc),
#                     on_trial=False
#                 )
#                 tenant.save()
#                 self.stdout.write(self.style.SUCCESS('Successfully created public tenant: %s' % tenant.name))

#                 # Add the primary domain for the tenant
#                 domain = Domain()
#                 domain.domain = 'dashboard.ruarakamethodist.org'  # Replace with your actual domain
#                 domain.tenant = tenant
#                 domain.is_primary = True
#                 domain.save()
#                 self.stdout.write(self.style.SUCCESS('Successfully created primary domain: %s for tenant %s' % (domain.domain, tenant.name)))
#             else:
#                 self.stdout.write(self.style.WARNING('Public tenant already exists.'))

#         except Exception as e:
#             self.stderr.write(self.style.ERROR('Error creating public tenant: %s' % e))


# from django.core.management.base import BaseCommand
# from Clients.models import Client, Domain
# from django.utils import timezone
# import pytz  # Import the pytz library

# class Command(BaseCommand):
#     help = 'Creates the initial public tenant'

#     def handle(self, *args, **options):
#         try:
#             # Check if the public tenant already exists
#             if not Client.objects.filter(schema_name='public').exists():
#                 # Create the public tenant
#                 utc_timezone = pytz.utc  # Get the UTC timezone object
#                 tenant = Client(
#                     schema_name='public',
#                     name='Schemas Inc.',
#                     paid_until=timezone.datetime(2016, 12, 5, tzinfo=utc_timezone),
#                     on_trial=False
#                 )
#                 tenant.save()
#                 self.stdout.write(self.style.SUCCESS('Successfully created public tenant: %s' % tenant.name))

#                 # Add the primary domain for the tenant
#                 domain = Domain()
#                 domain.domain = 'dashboard.ruarakamethodist.org'  # Replace with your actual domain
#                 domain.tenant = tenant
#                 domain.is_primary = True
#                 domain.save()
#                 self.stdout.write(self.style.SUCCESS('Successfully created primary domain: %s for tenant %s' % (domain.domain, tenant.name)))
#             else:
#                 self.stdout.write(self.style.WARNING('Public tenant already exists.'))

#         except Exception as e:
#             self.stderr.write(self.style.ERROR('Error creating public tenant: %s' % e))


from Clients.models import Client, Domain

# create your public tenant
tenant = Client(schema_name='public',
                name='Schemachurch',
                paid_until='2016-12-05',
                on_trial=False)
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'dashboard.ruarakamethodist.org' # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()