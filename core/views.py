from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator

def inicio(request):
    lista_posts = Post.objects.all().order_by('-fecha_publicacion')

    paginator = Paginator(lista_posts, 3)  
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'core/inicio.html', {'posts': posts})


def crear_post(request):

    # verificar que el usuario esté logueado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para publicar.")
        return redirect('inicio')

    perfil = request.user.perfil

    # regla para usuarios básicos
    if perfil.tipo_usuario == "basico":

        hace_una_semana = timezone.now() - timedelta(days=7)

        posts_recientes = Post.objects.filter(
            autor=request.user,
            fecha_publicacion__gte=hace_una_semana
        ).count()

        if posts_recientes >= 1:
            messages.error(
                request,
                "Los usuarios básicos solo pueden publicar 1 post por semana."
            )
            return redirect('inicio')

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            # 👤 asignar autor automáticamente
            post.autor = request.user

            # 🔗 crear slug
            post.slug = slugify(post.titulo)

            post.save()

            messages.success(request, "Post creado correctamente")
            return redirect('inicio')

    else:
        form = PostForm()

    return render(request, 'core/crear_post.html', {'form': form})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'core/detalle_post.html', {'post': post})


def nosotros(request):
    contexto = {
        "titulo": "¿Quiénes somos y cuál es nuestra participación en el mundo del ultrasonido?",
        "descripcion": "En este momento sólo existe una persona en este proyecto, pero se espera que en el futuro se unan más personas para enriquecer el contenido y la experiencia de los usuarios. La idea es crear una comunidad apasionada por el ultrasonido, donde podamos compartir conocimientos, experiencias y recursos relacionados con esta fascinante tecnología. ¡Únete a nosotros en este viaje de descubrimiento y aprendizaje sobre el ultrasonido!"
    }

    return render(request, 'core/nosotros.html', contexto)




def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect('inicio')
    else:
        form = UserCreationForm()

    return render(request, 'core/registro.html', {'form': form})