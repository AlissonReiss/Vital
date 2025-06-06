from asyncio import constants
from email import message, message_from_string
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha: 
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')   
            return redirect('/usuarios/cadastro')
            
        
        if len(senha) < 6:
            message.add_message(request, constants.ERROR, 'A senha de ter no minimo 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        try:
            # Username deve ser único!
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except:  # noqa: E722
            return redirect('/usuarios/cadastro')


        return redirect('/usuarios/cadastro')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
						# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/usuarios/login')
        
def home(request):
    # Se o usuário estiver autenticado, passamos o nome dele para o template
    if request.user.is_authenticated:
        nome = request.user.first_name
        return render(request, 'home.html', {'nome': nome})
    
    return render(request, 'home.html')

def sair(request):
    logout(request)
    return redirect('/')

