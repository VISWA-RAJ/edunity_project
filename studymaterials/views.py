# studymaterials/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db.models import Q # We must import Q to perform "OR" queries

@login_required
def materials_home_view(request):
    # This view for the main materials page remains unchanged
    recent_materials = Material.objects.all()[:2]
    context = {
        'recent_materials': recent_materials
    }
    return render(request, 'materials/materials.html', context)

@login_required
def material_list_view(request):
    """
    This view now handles searching and filtering before pagination.
    """
    # --- NEW SEARCH LOGIC STARTS HERE ---
    query = request.GET.get('q') # Get the search term from the URL
    
    # Start with all materials
    all_materials_list = Material.objects.all()

    if query:
        # If a search term was provided, filter the list.
        # The Q object allows us to search in the title OR the description.
        all_materials_list = all_materials_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    # --- SEARCH LOGIC ENDS HERE ---
    
    paginator = Paginator(all_materials_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # We pass the query back to the template so we can display it in the search box
    # and keep it in the pagination links.
    return render(request, 'materials/material_list.html', {'materials': page_obj, 'query': query})

@login_required
def upload_material_view(request):
    # This view remains unchanged
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploader = request.user
            material.save()
            return redirect('materials_home')
    else:
        form = MaterialForm()
    
    return render(request, 'materials/upload_material.html', {'form': form})