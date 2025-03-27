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



import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Property

def booking(request, property_id, user_id):
    property_obj = get_object_or_404(Property, property_id=property_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment_data = {
        "amount": int(property_obj.rent * 100),  # Convert to paise
        "currency": "INR",
        "receipt": f"order_rcpt_{property_id}_{user_id}",
        "payment_capture": 1
    }
    order = client.order.create(data=payment_data)

    context = {
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "property": property_obj
    }
    return render(request, "properties/payment.html", context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property

@login_required
def rent_property(request, property_id, user_id):
    property_obj = get_object_or_404(Property, property_id=property_id)

    if not property_obj.is_rented:  # Check if the property is available
        property_obj.rented_by = request.user
        property_obj.is_rented = True
        property_obj.save()
        return redirect("properties:property_detail", property_id=property_id)  # Redirect to property details

    return redirect("properties:property_detail", property_id=property_id)  # Redirect if already rented


from django.shortcuts import get_object_or_404, redirect
from .models import Property

def view_on_map(request, property_id):
    property_obj = get_object_or_404(Property, property_id=property_id)
    owner = property_obj.owner if property_obj.owner else None 
    context = {
        'val': property_obj,
        'user': owner,  
        'type': 'House' if hasattr(property_obj, 'area') else 'Apartment',
        "map_link": property_obj.google_map_link,
    }
    if property_obj.google_map_link:
        return render(request, "properties/map.html", context)  

    # If no map link is provided, redirect to property details page
    property_obj = get_object_or_404(Property, pk=property_id)
    # print(f"Property ID: {property_obj.property_id}")
    # print(f"Owner ID: {property_obj.owner.id if property_obj.owner else 'No Owner'}")

    owner = property_obj.owner if property_obj.owner else None  

    return redirect("properties:property_details", property_id=property_id)



from django.shortcuts import render, get_object_or_404
from .models import Property

def property_vr_view(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    return render(request, "properties/property_vr_view.html", {"vr_image_url": property.vr_image.url})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Property  # Import the Property model

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user

    # Fetch properties posted by the user
    user_properties = Property.objects.filter(owner=user)

    context = {
        'user': user,
        'property_no': user_properties.count(),  # Count of properties
        'properties': user_properties,
    }
    
    return render(request, 'properties/profile.html', context)



from django.shortcuts import render, redirect
from .models import Property
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Property
from django.contrib.auth.decorators import login_required

@login_required
def post_property(request):
    if request.method == "POST":
        area = request.POST.get("area")
        floor = request.POST.get("floor")
        location = request.POST.get("location")
        city = request.POST.get("city")
        state = request.POST.get("state")
        rent = request.POST.get("rent")
        bedrooms = request.POST.get("bedrooms")
        kitchen = request.POST.get("kitchen")
        hall = request.POST.get("hall")
        balcony = request.POST.get("balcony")
        AC = request.POST.get("AC")
        google_map_link = request.POST.get("google_map_link")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        vr_image = request.FILES.get("vr_image")

        property_obj = Property.objects.create(
            owner=request.user,
            area=area,
            floor=floor,
            location=location,
            city=city,
            state=state,
            rent=rent,
            bedrooms=bedrooms,
            kitchen=kitchen,
            hall=hall,
            balcony=balcony,
            AC=AC,
            google_map_link=google_map_link,
            description=description,
            image=image,
            vr_image=vr_image
        )
        return redirect("properties:profile")  # Change "home" to your property listing page

    return render(request, "properties/post_property.html")



from django.shortcuts import render
from .models import Property

def property_explore(request):
    # Get all properties initially
    properties = Property.objects.all()

    # Get search query and filter parameters from GET request
    search_query = request.GET.get('search', '')
    min_rent = request.GET.get('min_rent')
    max_rent = request.GET.get('max_rent')
    bedrooms = request.GET.get('bedrooms')
    city = request.GET.get('city')
    state = request.GET.get('state')

    # Apply search filter (location, city, state, description)
    if search_query:
        properties = properties.filter(
            location__icontains=search_query
        ) | properties.filter(
            city__icontains=search_query
        ) | properties.filter(
            state__icontains=search_query
        ) | properties.filter(
            description__icontains=search_query
        )

    # Apply filters
    if min_rent:
        properties = properties.filter(rent__gte=min_rent)
    if max_rent:
        properties = properties.filter(rent__lte=max_rent)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    if city:
        properties = properties.filter(city__iexact=city)
    if state:
        properties = properties.filter(state__iexact=state)

    return render(request, 'properties/property_explore.html', {'properties': properties})
