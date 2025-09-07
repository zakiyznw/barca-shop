from django.shortcuts import render

<<<<<<< HEAD
def show_main(request):
    return render(request, "main.html")
=======
# Create your views here.
def show_main(request):
    context = {
        'npm' : '240123456',
        'name': 'Haru Urara',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)
>>>>>>> cf934d4 (Complete tugas Individu 2)
