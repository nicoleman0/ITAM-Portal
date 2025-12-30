from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Asset, Employee, Assignment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 25


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'model', 'category', 'status', 'purchase_date',
                    'warranty_expiry', 'warranty_status_display', 'qr_code_display']
    list_filter = ['status', 'category', 'purchase_date', 'warranty_expiry']
    search_fields = ['serial_number', 'model']
    date_hierarchy = 'purchase_date'
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at', 'qr_code_preview']
    actions = ['generate_qr_codes']

    fieldsets = (
        ('Basic Information', {
            'fields': ('serial_number', 'model', 'category', 'status')
        }),
        ('Purchase & Warranty Details', {
            'fields': ('purchase_date', 'warranty_expiry')
        }),
        ('QR Code', {
            'fields': ('qr_code', 'qr_code_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def warranty_status_display(self, obj):
        """Display warranty status with color highlighting"""
        if obj.is_warranty_expired():
            return format_html(
                '<span style="color: white; background-color: red; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">⚠ EXPIRED</span>'
            )
        return format_html(
            '<span style="color: white; background-color: green; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">✓ Active</span>'
        )
    warranty_status_display.short_description = 'Warranty Status'

    def qr_code_display(self, obj):
        """Display QR code status in list view"""
        if obj.qr_code:
            return format_html(
                '<span style="color: green;">✓</span>'
            )
        return format_html(
            '<span style="color: gray;">—</span>'
        )
    qr_code_display.short_description = 'QR'

    def qr_code_preview(self, obj):
        """Display QR code preview in detail view"""
        if obj.qr_code:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" /><br>'
                '<a href="{}" target="_blank">Download QR Code</a>',
                obj.qr_code.url,
                obj.qr_code.url
            )
        return "No QR code generated. Save the asset first, then use the 'Generate QR Codes' action."
    qr_code_preview.short_description = 'QR Code Preview'

    def generate_qr_codes(self, request, queryset):
        """Admin action to generate QR codes for selected assets"""
        count = 0
        for asset in queryset:
            asset.generate_qr_code()
            asset.save()
            count += 1

        self.message_user(
            request, f'Successfully generated QR codes for {count} asset(s).')
    generate_qr_codes.short_description = 'Generate QR codes for selected assets'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name',
                    'email', 'department', 'created_at']
    list_filter = ['department']
    search_fields = ['employee_id', 'full_name', 'email', 'department']
    list_per_page = 25


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['asset', 'employee', 'assigned_date', 'return_expected_date',
                    'actual_return_date', 'is_active_display']
    list_filter = ['assigned_date',
                   'return_expected_date', 'actual_return_date']
    search_fields = ['asset__serial_number', 'asset__model', 'employee__full_name',
                     'employee__employee_id']
    date_hierarchy = 'assigned_date'
    list_per_page = 25
    autocomplete_fields = ['asset', 'employee']

    fieldsets = (
        ('Assignment Details', {
            'fields': ('asset', 'employee', 'assigned_date')
        }),
        ('Return Information', {
            'fields': ('return_expected_date', 'actual_return_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

    def is_active_display(self, obj):
        """Display active status with visual indicator"""
        if obj.is_active():
            return format_html(
                '<span style="color: green; font-weight: bold;">● Active</span>'
            )
        return format_html(
            '<span style="color: gray;">○ Returned</span>'
        )
    is_active_display.short_description = 'Status'
