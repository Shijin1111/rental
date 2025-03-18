from django.shortcuts import render
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})




from django.shortcuts import render, get_object_or_404
from .models import Property
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the User model dynamically

def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    # Get owner details
    owner = property_obj.owner if property_obj.owner else None  

    context = {
        'val': property_obj,
        'user': owner,  # Use 'owner' instead of 'user_email'
        'type': 'House' if hasattr(property_obj, 'area') else 'Apartment'
    }
    return render(request, 'properties/property_detail.html', context)
