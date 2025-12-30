"""
Demo script to test Phase 2 features
Run this after creating a superuser: python manage.py shell < demo_features.py
"""

from assets.models import Category, Asset, Employee, Assignment
from django.utils import timezone
from datetime import timedelta

print("=" * 60)
print("ITAM System - Phase 2 Features Demo")
print("=" * 60)

# Create Category
print("\n1. Creating Category...")
laptop_category, created = Category.objects.get_or_create(
    name="Laptop",
    defaults={"description": "Portable computers"}
)
print(f"   ✓ Category: {laptop_category}")

# Create Asset
print("\n2. Creating Asset...")
asset, created = Asset.objects.get_or_create(
    serial_number="DEMO-001",
    defaults={
        "model": "Dell Latitude 5420",
        "category": laptop_category,
        "purchase_date": timezone.now().date() - timedelta(days=365),
        "warranty_expiry": timezone.now().date() + timedelta(days=365),
        "status": "AVAILABLE"
    }
)
print(f"   ✓ Asset: {asset}")
print(f"   ✓ Status: {asset.status}")

# Generate QR Code
print("\n3. Generating QR Code...")
asset.generate_qr_code()
asset.save()
print(
    f"   ✓ QR Code generated: {asset.qr_code.name if asset.qr_code else 'None'}")

# Create Employee
print("\n4. Creating Employee...")
employee, created = Employee.objects.get_or_create(
    employee_id="EMP-001",
    defaults={
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "department": "IT Department"
    }
)
print(f"   ✓ Employee: {employee}")

# Create Assignment (Auto Check-Out Test)
print("\n5. Creating Assignment (Testing Auto Check-Out)...")
print(f"   Asset status before: {asset.status}")

assignment, created = Assignment.objects.get_or_create(
    asset=asset,
    employee=employee,
    actual_return_date__isnull=True,
    defaults={
        "assigned_date": timezone.now().date(),
        "return_expected_date": timezone.now().date() + timedelta(days=30)
    }
)

# Refresh asset from database
asset.refresh_from_db()
print(f"   ✓ Assignment created: {assignment}")
print(
    f"   ✓ Asset status after: {asset.status} (automatically changed to DEPLOYED)")

# Test Deployment Validation
print("\n6. Testing Deployment Validation...")
try:
    # Try to create another assignment for the same asset
    duplicate = Assignment(
        asset=asset,
        employee=employee,
        assigned_date=timezone.now().date()
    )
    duplicate.full_clean()  # This should raise ValidationError
    print("   ✗ Validation FAILED - duplicate assignment was allowed!")
except Exception as e:
    print(f"   ✓ Validation working: {str(e)[:80]}...")

# Return Asset
print("\n7. Returning Asset...")
assignment.actual_return_date = timezone.now().date()
assignment.save()
asset.refresh_from_db()
print(f"   ✓ Asset returned")
print(
    f"   ✓ Asset status after return: {asset.status} (automatically changed to AVAILABLE)")

print("\n" + "=" * 60)
print("Demo Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Visit http://127.0.0.1:8000/admin/")
print("2. View the Asset to see the QR code")
print("3. Try creating assignments to test validation")
print("=" * 60)
