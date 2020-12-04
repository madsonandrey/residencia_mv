from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from .form import UserForm, MedicoForm
from django.contrib import auth, messages

from .models import Medico


def index(request):
    return render(request, 'medico/index.html')


def login_med(request):
    if request.method != 'POST':
        return render(request, 'medico/login_medico.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'medico/login_medico.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('dash_med')


def logout_med(request):
    auth.logout(request)
    return redirect('login_med')


def cadastrar_med(request):
    form1 = UserForm(request.POST or None)
    form2 = MedicoForm(request.POST or None)

    if request.method != 'POST':
        return render(request, 'medico/cadastro_medico.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        user.groups.add(3)
        if form2.is_valid():
            medico = form2.save(commit=False)
            medico.dados_pessoais = user
            form1.save()
            form2.save()
            messages.success(request, 'Médico cadastrado com sucesso')
            return redirect('login_med')

    return render(request, 'medico/cadastro_medico.html', {'form1': form1, 'form2': form2})


def dash_med(request):
    return render(request, 'medico/dashboard_medico.html')


def editar_med(request, med_id):
    obj = get_object_or_404(Medico, id=med_id)

    email = request.POST.get('email')
    cpf = request.POST.get('cpf')
    crm = request.POST.get('crm')

    form1 = UserForm(request.POST or None, instance=obj.dados_pessoais)
    form2 = MedicoForm(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = MedicoForm()
            return render(request, 'medico/editar_medico.html', {'form1': form1, 'form2': form2})

        if len(crm) > 8:
            messages.error(request, 'CRM inválido')
            form1 = UserForm()
            form2 = MedicoForm()
            return render(request, 'medico/editar_medico.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            medico = form2.save(commit=False)
            medico.dados_pessoais = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return redirect('dash_med')

    return render(request, 'laboratorio/editar_laboratorio.html', {'form1': form1, 'form2': form2})


def deletar_med(request, med_id):
    medico = get_object_or_404(Medico, id=med_id)
    fk_user = medico.dados_pessoais
    user = get_object_or_404(User, id=fk_user)

    if request.method == "GET":
        medico.delete()
        user.delete()
        messages.success(request, 'Usuário apagado com sucesso')
        return redirect("/home")

    return render(request, "medico/delete_med.html")