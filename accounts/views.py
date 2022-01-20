from django.http.response import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from geopy.distance import geodesic

from accounts.models import Friend_Request
from . import forms
from django.core.paginator import Paginator

from django.db.models import Q
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
    all_friend_request_recived = []
    all_friend_request_sent = []
    q1 = Friend_Request.objects.filter(to_user=request.user)
    for item in q1:        
        u=item.from_user
        all_friend_request_recived.append(u) #print(all_friend_request_recived)       

    q3 = Friend_Request.objects.filter(from_user=request.user)
    for item in q3:        
        u=item.to_user
        all_friend_request_sent.append(u) #print(all_friend_request_sent)
    
    
    logged_user = Profile.objects.get(user_id=request.user.id)
    logged_user_friends = logged_user.friends.all()  
    return render(request,  'accounts/user_detail.html', {'user_page':user_page, 
        'q1':all_friend_request_recived, 'q2':logged_user_friends,
             'q3':all_friend_request_sent,'all_friend_requests':q1 })
    

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

    if searched !=None:
        searched_list = User.objects.filter(Q(username__icontains = searched) | 
                    Q(first_name__icontains = searched)).order_by() #| Q(profile_location__icontains = searched))
        
    print(searched_list)    
    paginator = Paginator(searched_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/search_people.html', {'page_obj':page_obj})
    

@login_required
def send_friend_request(request, userID):       
    to_user = User.objects.get(id=userID)
    from_user = User.objects.get(id=request.user.id)

    created = Friend_Request.objects.get_or_create(
                                            to_user=to_user, from_user=from_user)                                       
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('Friend request was already sent')


@login_required
def cancel_friend_request(request, userID):       
    to_user = User.objects.get(id=userID)
    from_user = User.objects.get(id=request.user.id)

    picking_fr = Friend_Request.objects.get(to_user=to_user, from_user=from_user)

    if picking_fr:
        picking_fr.delete()
        return HttpResponse('Friend request cancelled')


@login_required
def accept_friend_request(request, requestID):
    to_user = User.objects.get(id=request.user.id)
    from_user = User.objects.get(id=requestID)
    friend_request = Friend_Request.objects.get(from_user=from_user,to_user=to_user)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.friends.add(friend_request.from_user)
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        HttpResponse('Friend request not accepted')


def friends_list(request,user_id):
    user_page = Profile.objects.get(user_id=user_id)
    logged_user = Profile.objects.get(user_id=request.user.id)
    page_user_friend_list = user_page.friends.all()
    logged_user_friend_list = logged_user.friends.all()
    mutual_friend = page_user_friend_list & logged_user_friend_list   
    
    return render(request,'accounts/user_friend_list.html',{'user_page':user_page,
                        'friend_list':page_user_friend_list, 'mutual_friend':mutual_friend})


@login_required
def unfriend(request, userID):
    removee = User.objects.get(id=userID)
    remover = User.objects.get(id=request.user.id)

    removee.profile.friends.remove(remover)
    remover.profile.friends.remove(removee)
    return HttpResponse('User is removed from Friends')


def distance(request):    
    friends = request.user.profile.friends.all()
    km = int(request.GET.get('km'))
    user_list = []
    
    for user in friends:
        p1 = (user.profile.lat,user.profile.long)
        p2 = (request.user.profile.lat,request.user.profile.long) #print(p1, p2)        

        d = geodesic(p1, p2).km
        print(user, d)
        if d < km:            
            user_list.append(user)    
    print(km)
    print(friends)
    print(request.user.profile.lat)
    print(user_list)
        
    
    return render(request, 'accounts/distance.html',{'user_list':user_list, 'km':km})