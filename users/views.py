from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm

"""
Módulo de vistas de autenticación de usuarios.

Este módulo gestiona el sistema de acceso de usuarios al sistema EnviroPro,
utilizando el sistema de autenticación integrado de Django.

Incluye las siguientes funcionalidades:
- Página inicial pública (home).
- Inicio de sesión de usuarios.
- Cierre de sesión.
- Registro de nuevas cuentas.

Estas vistas controlan el acceso a las funcionalidades protegidas del sistema,
garantizando que solo usuarios autenticados puedan acceder al dashboard y a la
gestión de datos.
"""

# Home
# Página pública inicial antes del login.
def home_view(request):
    return render(request, "users/home.html")

# Login
# Autentica al usuario mediante username y contraseña.
# Si las credenciales son correctas se inicia sesión, si son incorrectas salta un error.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, "Login realizado correctamente")
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "users/login.html")

# Logout
# Cierra la sesión del usuario autenticado.
def logout_view(request):
    #list(messages.get_messages(request))  # limpia mensajes pendientes
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("home")

# Registro del usuario
# Permite crear nuevas cuentas en el sistema.
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect("login")
        else:
            messages.error(request, "Error al crear el usuario")

    return render(request, "users/register.html", {"form": form})
