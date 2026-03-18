from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    # 👤 autor del post
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo



class Perfil(models.Model):

    TIPOS_USUARIO = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPOS_USUARIO,
        default='basico'
    )

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)