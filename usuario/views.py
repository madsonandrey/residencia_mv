from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .form import FormUsuario, UserForm, FormExames
from django.contrib import auth, messages
from django.core.validators import validate_email
from .models import Usuario


def home(request):
    return render(request, 'usuario/home.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'usuario/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'usuario/login.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('dash')


def logout(request):
    auth.logout(request)
    return redirect('login')


def is_usuario(user):
    return user.groups.filter(id=1).exists()


@user_passes_test(is_usuario)
def dash(request):
    return render(request, 'usuario/dash.html')


def cadastrar(request):
    form1 = UserForm(request.POST or None)
    form2 = FormUsuario(request.POST or None)
    if request.method != 'POST':
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    username = request.POST.get('username')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')

    # Validações

    # USUÁRIO

    if not username or not senha or not confirmar_senha or not first_name or not last_name or not cpf or not email:
        messages.error(request, 'Todos os campos devem ser preenchidos')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # CPF

    if len(cpf) != 11:
        messages.error(request, 'CPF inválido')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # E-MAIL
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        user.groups.add(1)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario = user
            form1.save()
            form2.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('login')

    return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})


# Editar cadastro
def editar(request, usuario_id):
    obj = get_object_or_404(Usuario, id=usuario_id)

    user = request.POST.get('usuario')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')

    form1 = UserForm(request.POST or None, instance=obj.usuario)
    form2 = FormUsuario(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})

        if len(cpf) != 11:
            messages.error(request, 'CPF inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return HttpResponseRedirect('/')

    return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})


def listar(request):
    usuarios = Usuario.objects.order_by('-id')

    paginator = Paginator(usuarios, 11)

    page = request.GET.get('page')

    usuarios = paginator.get_page(page)

    return render(request, 'usuario/lista_usuarios.html', {
        'usuarios': usuarios
    })


def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "GET":
        usuario.delete()
        messages.success(request, 'Usuário apagado com sucesso')
        return HttpResponseRedirect("/lista")

    return render(request, "usuario/delete_usuario.html")


# EXAMES

def novo_exame(request):
    form = FormExames(request.POST or None)
    current_user = request.user.id
    user = get_object_or_404(User, id=current_user)

    if request.method != 'POST':
        return render(request, 'usuario/cadastrar_exame.html', {'form': form})

    if form.is_valid():
        exame = form.save(commit=False)
        exame.paciente = user
        form.save()

    return render(request, 'usuario/cadastrar_exame.html', {'form': form})

