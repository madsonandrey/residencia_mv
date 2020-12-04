from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from .form import *
from django.contrib import auth, messages


def index(request):
    return render(request, 'laboratorio/index.html')


def login_lab(request):
    if request.method != 'POST':
        return render(request, 'laboratorio/login_lab.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'laboratorio/login_lab.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('dash_lab')


def logout_lab(request):
    auth.logout(request)
    return redirect('login_lab')


def cadastrar_lab(request):
    form1 = UserForm(request.POST or None)
    form2 = LaboratorioForm(request.POST or None)

    cnpj = request.POST.get('cnpj')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    email = request.POST.get('email')

    if request.method != 'POST':
        form1 = UserForm()
        form2 = LaboratorioForm()
        return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})

    # CNPJ

    if len(cnpj) != 14:
        messages.error(request, 'CNPJ inválido')
        form1 = UserForm()
        form2 = LaboratorioForm()
        return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = LaboratorioForm()
        return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = LaboratorioForm()
        return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})

    # E-MAIL

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        user.groups.add(2)
        if form2.is_valid():
            laboratorio = form2.save(commit=False)
            laboratorio.dados = user
            form1.save()
            form2.save()
            messages.success(request, 'Laboratório cadastrado com sucesso')
            return redirect('login_lab')

    return render(request, 'laboratorio/cadastro_laboratorio.html', {'form1': form1, 'form2': form2})


def dash_lab(request):
    return render(request, 'laboratorio/dash_lab.html')


# Editar cadastro de laboratório

def editar_lab(request, lab_id):
    obj = get_object_or_404(Laboratorio, id=lab_id)

    email = request.POST.get('email')
    cnpj = request.POST.get('cnpj')

    form1 = UserForm(request.POST or None, instance=obj.dados)
    form2 = LaboratorioForm(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = LaboratorioForm()
            return render(request, 'laboratorio/editar_laboratorio.html', {'form1': form1, 'form2': form2})

        if len(cnpj) != 14:
            messages.error(request, 'CNPJ inválido')
            form1 = UserForm()
            form2 = LaboratorioForm()
            return render(request, 'laboratorio/editar_laboratorio.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return redirect('dash_lab')

    return render(request, 'laboratorio/editar_laboratorio.html', {'form1': form1, 'form2': form2})
