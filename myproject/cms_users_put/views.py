from django.shortcuts import render
from django.http import HttpResponse
from cms_users_put.models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
# Create your views here.
def milogout(request):
    logout(request)
    return redirect(barra) #('/')

def barra(request):
    respuesta = "Direcciones disponibles son: "
    list_pages = Pages.objects.all()
    for page in list_pages:
        respuesta += "<br>-/" + page.name + " --> " + page.page


    #plantilla = get_template("miplantilla.html") #la cojo de las transpas la de title y content
    #contexto = Context({'title': "SOLO PUEDES VER LAS PAGINAS",'content':respuesta})
    #return HttpResponse(plantilla.render(contexto))
    return HttpResponse(respuesta)

@csrf_exempt
def process(request, nombre_pag):
    if request.method == "GET":
        try:
            page = Pages.objects.get(name=nombre_pag)
            resp = "La página solicitada es /" + page.name + " -> " + page.page
        except Pages.DoesNotExist:
            resp = "No se encuentra la página en nuestra base de datos, la puedes crear:"
            resp += "<form action='/" + nombre_pag + "' method=POST>"
            resp += "Nombre: <input type='text' name='nombre'>"
            resp += "<br>Página: <input type='text' name='page'>"
            resp += "<input type='submit' value='Enviar'></form>"
    elif request.method == "POST":
        if request.user.is_authenticated():
            nombre = request.POST['nombre']
            page = request.POST['page']
            pagina = Pages(name=nombre, page=page)
            pagina.save()
            resp = "Has creado la página " + nombre
        else:
            resp = "Necesitas < a href= '/login/'>hacer login</a>"
    elif request.method == "PUT":
        try:
            page = Pages.objects.get(name=req)
            resp = "Ya existe una página con ese nombre"
        except Pages.DoesNotExist:
            page = request.body
            pagina = Pages(name=nombre_pag, page=page)
            pagina.save()
            resp = "Has creado la página " + nombre_pag
    else:
        resp = "Error. Method not supported."

    resp += "<br/><br/>Eres  " + request.user.username + '<a href="/logout/"> haz logout</a>.'
    return HttpResponse(resp)
