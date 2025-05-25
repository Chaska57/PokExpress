from django.shortcuts import render, get_object_or_404, redirect
from .models import Fish, User, UserFish
from .forms import UserProfileForm

def index(request):
    fishes = Fish.objects.all()
    users = User.objects.all()
    return render(request, 'index.html', {'fishes': fishes,'users': users})
# Create your views here.

def pokedex(request, user_id):
    user = get_object_or_404(User, id=user_id)
    fishes = Fish.objects.all()

    # Filtro por tipo de captura
    captura = request.GET.get('captura', '')  # "capturados", "no_capturados" o ""

    if captura == 'capturados':
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish, captured=True).first()
            }
            for fish in fishes
        ]
    elif captura == 'no_capturados':
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish, captured=False).first()
            }
            for fish in fishes
        ]
    else:
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish).first()
            }
            for fish in fishes
        ]

    # Contar capturados
    captured_count = sum(1 for data in user_fishes if data["captured"] and data["captured"].captured)

    # Ordenamiento
    orden = request.GET.get('orden', 'nombre_asc')

    if orden == 'nombre_asc':
        user_fishes.sort(key=lambda x: x['fish'].name)
    elif orden == 'nombre_desc':
        user_fishes.sort(key=lambda x: x['fish'].name, reverse=True)

    return render(request, "poke.html", {
        "user": user,
        "user_fishes": user_fishes,
        "captured_count": captured_count,
        "total_count": len(user_fishes),
    })


def edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            
            form.save()
            return redirect('edit', user_id=user.id)  # Redirige al perfil del usuario
    else:
        form = UserProfileForm(instance=user)

     # Obtener todos los UserFish del usuario
    fishes = Fish.objects.all()
    user_fishes = [
        {
            "fish": fish,
            "captured": UserFish.objects.filter(user=user, fish=fish).first()
        }
        for fish in fishes
    ]

    return render(request, 'edit.html', {
        'form': form,
        'user': user,
        'user_fishes': user_fishes,
    })

def edit_user_fish(request, user_id):
    user = get_object_or_404(User, id=user_id)
    fishes = Fish.objects.all()

   # Filtro por tipo de captura
    captura = request.GET.get('captura', '')  # "capturados", "no_capturados" o ""

    user_fishes = []
    for fish in fishes:
        user_fish = UserFish.objects.filter(user=user, fish=fish).first()
        
        if captura == 'capturados' and (not user_fish or not user_fish.captured):
            continue
        elif captura == 'no_capturados' and (not user_fish or user_fish.captured):
            continue

        user_fishes.append({
            "fish": fish,
            "user_fish": user_fish
        })
    if request.method == "POST":
        for data in user_fishes:
            fish = data["fish"]
            uf = data["user_fish"]

            # Si no existe, crear nuevo UserFish
            if not uf:
                uf = UserFish.objects.create(user=user, fish=fish)

            # Checkbox: capturado
            captured_str = request.POST.get(f'captured_{fish.id}', 'off')
            uf.captured = (captured_str == 'true')

            # Foto: si se sube una nueva
            uploaded_photo = request.FILES.get(f'photo_{fish.id}')
            if uploaded_photo:
                uf.photo = uploaded_photo

            uf.save()
            if uploaded_photo:
                print(f"Foto recibida para pez {fish.name}: {uploaded_photo.name}")

        return redirect(request.path)
    
   # Filtro por tipo de captura

    # Contar capturados
    captured_count = sum(1 for data in user_fishes if data["user_fish"] and data["user_fish"].captured)

    # Ordenamiento
    orden = request.GET.get('orden', 'nombre_asc')

    if orden == 'nombre_asc':
        user_fishes.sort(key=lambda x: x['fish'].name)
    elif orden == 'nombre_desc':
        user_fishes.sort(key=lambda x: x['fish'].name, reverse=True)

    context = {
        "user": user,
        "user_fishes": user_fishes,
        "captured_count": captured_count,
        "total_count": len(user_fishes),
    }
    return render(request, "edit_user_fish.html", context)
