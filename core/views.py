from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm


def inicio(request):
    posts_list = Post.objects.all().order_by('-fecha_creacion')

    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'core/inicio.html', {'posts': posts})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'core/detalle_post.html', {'post': post})


def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post creado correctamente 🎉")
            return redirect('detalle_post', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'core/crear_post.html', {'form': form})


def nosotros(request):
    contexto = {
        "titulo": "Trabaja con Django: descubrirás bases de datos relacionadas a la ecografía",
        "descripcion": "Acá aprenderás desde la base física hasta la introducción a la práctica clínica en ecografía. ¿Estás listo para comenzar? 😎"
    }
    return render(request, 'core/nosotros.html', contexto)