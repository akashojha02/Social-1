from django.http.response import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import Friend_Request
from . import forms
from django.core.paginator import Paginator
from itertools import chain

from accounts.models import Profile
from groups.models import Group
from django.contrib.auth import get_user_model
User= get_user_model()
user_list = User.objects.all()
group_list = Group.objects.all()


# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url= reverse_lazy('login')
    template_name='accounts/signup.html'

def user_detail(request, pk):
    
    user_page = User.objects.get(pk=pk)
    all_friend_requests = Friend_Request.objects.filter(to_user=request.user)
    print(all_friend_requests)
    return render(request,  'accounts/user_detail.html', {'user_page':user_page,
     'all_friend_requests':all_friend_requests })
    

def update_profile(request):
    current_user= user_list.filter(username=request.user).values('id')[0]['id']
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            url = reverse('accounts:user_detail',kwargs={'pk': current_user} )
            return HttpResponseRedirect(url)            
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def search_profile(request):
    searched= request.GET.get('searched')

    if searched !=None and len(searched) > 0:
        searched_user = user_list.filter(username__icontains = searched)
        searched_group = group_list.filter(name__icontains = searched)
        searched_list = sorted(chain(searched_user, searched_group), 
                                key= lambda instance: instance.pk)
        
    paginator = Paginator(searched_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/search_people.html', {'page_obj':page_obj})
    

@login_required
def send_friend_request(request, userID):
    print(request.user.id)
    print(userID)
        
    to_user = User.objects.get(id=userID)
    print(to_user)
    from_user = User.objects.get(id=request.user.id)
    print(from_user)

    created = Friend_Request.objects.get_or_create(
                                            to_user=to_user, from_user=from_user)                                       
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('Friend request was already sent')


@login_required
def accept_friend_request(request, requestID):
    to_user = User.objects.get(id=request.user.id)
    from_user = User.objects.get(id=requestID)
    print(to_user)
    print(from_user)
    friend_request = Friend_Request.objects.get(from_user=from_user,to_user=to_user)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.friends.add(friend_request.from_user)
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        HttpResponse('Friend request not accepted')