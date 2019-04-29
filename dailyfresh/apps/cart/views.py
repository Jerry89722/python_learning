from django.shortcuts import render

# Create your views here.


def test(request, token):
    print(token)
    return render(request, 'cart.html')
