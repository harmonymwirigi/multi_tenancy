import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from Clients.models import Client  # Import your Client model
from member.models import Member, MemberContact, MemberAge, MemberMaritalStatus, MemberResidence
from datetime import datetime

class Command(BaseCommand): 
    help = 'Imports dummy members from a CSV file into a specific tenant.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing member data.')
        parser.add_argument('tenant_schema', type=str, help='The schema_name of the tenant to import data into.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        tenant_schema = options['tenant_schema']

        try:
            tenant = Client.objects.get(schema_name=tenant_schema)
        except Client.DoesNotExist:
            raise CommandError(f"Tenant with schema '{tenant_schema}' not found.")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                with schema_context(tenant.schema_name):
                    for row in reader:
                        try:
                            username = row.get('username')
                            password = row.get('password')
                            first_name = row.get('first_name', '')
                            last_name = row.get('last_name', '')
                            email = row.get('email', '')
                            middle_name = row.get('middle_name', ' ')
                            gender = row.get('gender', None)
                            phone = row.get('phone', None)
                            dob_str = row.get('date_of_birth', None)
                            marital_status_str = row.get('marital_status', None)
                            town = row.get('town', None)
                            road = row.get('road', None)
                            street = row.get('street', None)
                            village_estate = row.get('village_estate', None)
                            residence_description = row.get('residence_description', None)

                            if not username or not password:
                                self.stdout.write(self.style.WARNING(f"Skipping row: Username and password are required."))
                                continue

                            user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name, 'email': email})
                            if created:
                                user.set_password(password)
                                user.save()
                                member = Member.objects.create(member=user, middle_name=middle_name, gender=gender)

                                if phone:
                                    MemberContact.objects.create(member=member, phone=phone)
                                if dob_str:
                                    try:
                                        d_o_b = datetime.strptime(dob_str, '%Y-%m-%d').date()  # The format differs, adjust it if needed
                                        MemberAge.objects.create(member=member, d_o_b=d_o_b)
                                    except ValueError:
                                        self.stdout.write(self.style.WARNING(f"Invalid date format for {username}: {dob_str}"))
                                if marital_status_str:
                                    MemberMaritalStatus.objects.create(member=member, status=marital_status_str.upper()[0]) # Assuming first letter matches your choices
                                if town or road or street or village_estate or residence_description:
                                    MemberResidence.objects.create(member=member, town=town, road=road, street=street, village_estate=village_estate, description=residence_description)

                                self.stdout.write(self.style.SUCCESS(f"Successfully imported member for tenant '{tenant_schema}': {username}"))
                            else:
                                self.stdout.write(self.style.WARNING(f"User with username '{username}' already exists in tenant '{tenant_schema}'."))

                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error processing row for tenant '{tenant_schema}': {row.get('username', 'N/A')} - {e}"))

        except FileNotFoundError:
            raise CommandError(f"CSV file '{csv_file_path}' not found.")