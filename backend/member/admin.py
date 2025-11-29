# Register your models here.
from django.contrib import admin
from .models import Member, MemberContact, MemberAge, MemberMaritalStatus, MemberResidence, Role, MemberRole, Family, FamilyMembership, ImportantDateType, MemberImportantDate, MemberNote, CSV, OTP

class MemberContactInline(admin.StackedInline):
    model = MemberContact
    can_delete = False
    verbose_name_plural = 'Contact Information'
    fk_name = 'member'

class MemberAgeInline(admin.StackedInline):
    model = MemberAge
    can_delete = False
    verbose_name_plural = 'Age Information'
    fk_name = 'member'

class MemberMaritalStatusInline(admin.StackedInline):
    model = MemberMaritalStatus
    can_delete = False
    verbose_name_plural = 'Marital Status'
    fk_name = 'member'

class MemberResidenceInline(admin.StackedInline):
    model = MemberResidence
    can_delete = False
    verbose_name_plural = 'Residence Information'
    fk_name = 'member'

class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberContactInline, MemberAgeInline, MemberMaritalStatusInline, MemberResidenceInline]
    list_display = ('__str__', 'gender')
    search_fields = ('member__first_name', 'member__last_name', 'phone_number') # Assuming you want to search by name and phone
    # Add other fields you want to display or search

admin.site.register(Member, MemberAdmin)
admin.site.register(MemberContact) # Register separately if you want to manage them outside of Member
admin.site.register(MemberAge)     # Register separately if you want to manage them outside of Member
admin.site.register(MemberMaritalStatus) # Register separately if you want to manage them outside of Member
admin.site.register(MemberResidence) # Register separately if you want to manage them outside of Member
admin.site.register(Role)
admin.site.register(MemberRole)
admin.site.register(Family)
admin.site.register(FamilyMembership)
admin.site.register(ImportantDateType)
admin.site.register(MemberImportantDate)
admin.site.register(MemberNote)
admin.site.register(CSV)
admin.site.register(OTP)
