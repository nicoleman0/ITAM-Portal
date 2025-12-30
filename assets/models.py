from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File
import os


class Category(models.Model):
    """Model for asset categories (e.g., Laptop, Desktop, Server, Peripherals)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Asset(models.Model):
    """Model for IT assets"""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('DEPLOYED', 'Deployed'),
        ('BROKEN', 'Broken'),
        ('RETIRED', 'Retired'),
    ]

    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='assets')
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.model} ({self.serial_number})"

    def is_warranty_expired(self):
        """Check if the warranty has expired"""
        return timezone.now().date() > self.warranty_expiry

    def warranty_status(self):
        """Return warranty status as a string"""
        if self.is_warranty_expired():
            return "Expired"
        return "Active"

    def get_admin_url(self):
        """Get the admin URL for this asset"""
        return reverse('admin:assets_asset_change', args=[self.pk])

    def generate_qr_code(self):
        """Generate QR code containing the asset's admin URL"""
        if not self.pk:
            return  # Can't generate QR code for unsaved object

        # Build the full URL (you may need to adjust the domain for production)
        admin_url = self.get_admin_url()
        full_url = f"{settings.SITE_DOMAIN}{admin_url}" if hasattr(
            settings, 'SITE_DOMAIN') else admin_url

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(full_url)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")

        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Generate filename
        filename = f'asset_{self.serial_number}_qr.png'

        # Save to model's ImageField
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

        return self.qr_code


class Employee(models.Model):
    """Model for employees"""
    employee_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"


class Assignment(models.Model):
    """Model for tracking asset assignments to employees"""
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateField(default=timezone.now)
    return_expected_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.asset} assigned to {self.employee} on {self.assigned_date}"

    def is_active(self):
        """Check if assignment is currently active"""
        return self.actual_return_date is None

    def clean(self):
        """Validate that asset is not already deployed"""
        super().clean()

        # Skip validation if this is a return (actual_return_date is set)
        if self.actual_return_date:
            return

        # Check if this is a new assignment (not updating existing one)
        if not self.pk:
            # Check if asset is already deployed
            if self.asset.status == 'DEPLOYED':
                # Check if there's an active assignment
                active_assignments = Assignment.objects.filter(
                    asset=self.asset,
                    actual_return_date__isnull=True
                )
                if active_assignments.exists():
                    raise ValidationError({
                        'asset': f'Asset "{self.asset}" is already deployed to '
                        f'{active_assignments.first().employee}. '
                        f'Please return it first before reassigning.'
                    })

    def save(self, *args, **kwargs):
        """Override save to automatically update asset status"""
        # Run validation
        self.full_clean()

        # Check if this is a new assignment or returning an asset
        if self.actual_return_date:
            # Asset is being returned, set status to AVAILABLE
            self.asset.status = 'AVAILABLE'
            self.asset.save(update_fields=['status'])
        elif not self.pk or not self.actual_return_date:
            # New assignment or active assignment, set status to DEPLOYED
            self.asset.status = 'DEPLOYED'
            self.asset.save(update_fields=['status'])

        super().save(*args, **kwargs)
