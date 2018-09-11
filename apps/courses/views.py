from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from django.views.static import serve


class OrgView(View):
    def get(self,request):
        return render(request,"courses/org_list.html",{})