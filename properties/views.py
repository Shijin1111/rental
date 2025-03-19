from django.shortcuts import render
from .models import Property
from django.shortcuts import render, redirect

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})




from django.shortcuts import render, get_object_or_404
from .models import Property
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the User model dynamically
def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    # print(f"Property ID: {property_obj.property_id}")
    # print(f"Owner ID: {property_obj.owner.id if property_obj.owner else 'No Owner'}")

    owner = property_obj.owner if property_obj.owner else None  

    context = {
        'val': property_obj,
        'user': owner,  
        'type': 'House' if hasattr(property_obj, 'area') else 'Apartment'
    }
    
    return render(request, 'properties/property_detail.html', context)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Property
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_view(request, property_id, receiver_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            Message.objects.create(sender=request.user, receiver=receiver, property=property_obj, message=message_text)

    messages = Message.objects.filter(
        property=property_obj, 
        sender__in=[request.user, receiver], 
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    return render(request, "properties/chat_room.html", {"messages": messages, "receiver": receiver, "property": property_obj})




from django.db.models import Q

@login_required
def owner_chat(request):
    owner = request.user  # Logged-in owner
    
    # Get all properties owned by the owner
    owner_properties = Property.objects.filter(owner=owner)

    # Get all messages related to these properties, where the owner is the receiver
    messages = Message.objects.filter(
        property__in=owner_properties,  # Only messages related to owner's properties
        receiver=owner  # Messages where the owner is the receiver
    ).order_by("-timestamp")  # Order by latest messages first

    context = {"messages": messages}
    return render(request, "properties/owner_chat.html", context)
