from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Prescription(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='prescriptions')
    prescription = models.FileField(upload_to='prescriptions/')
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"