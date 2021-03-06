from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import registrationForm,UpdateUser,UpdateProfile,CommentForm
from django.contrib.auth.models import User
from .models import Image,Profile,Comments,Preference
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

def is_users(image_user, logged_user):
    return image_user == logged_user

class CreateDetail(LoginRequiredMixin,CreateView):
    model = Image
    fields = ['image','caption']
    

    def form_valid(self,form):
        form.instance.username = self.request.user
        return super().form_valid(form)

class CreateComment(LoginRequiredMixin,CreateView):
    model = Comments
    fields = ['comments']
    
    template_name = 'blog/comment-detail.html'
    def form_valid(self,form):
        form.instance.username = self.request.user
        return super().form_valid(form)

class UpdateDetail(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Image
    fields = ['image','caption']
    def test_func(self):
        image = self.get_object()
        if self.request.user == image.username:
            return True
        return False


    def form_valid(self,form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class ImageView(ListView):
    
    model = Image
   
    template_name = 'blog/home.html'
    context_object_name = 'images'

class CommentView(ListView):
    model = Comments
    template_name = 'blog/image-detail.html'
    context_object_name = 'comments'




        
    
   
def register(request):
    if request.method == 'POST':
       form = registrationForm(request.POST)
       if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request,f'Account created for {username}')
           return redirect('blog-login')

    else:
       form = registrationForm()
    return render (request,'blog/register.html',{'form':form})


def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = Image.search_by_username(search_term)
        message = f"{search_term}"

        return render(request, 'blog/search.html',{"message":message,"users": searched_users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'searches/search.html',{"message":message})

@login_required
def profile(request):
    if request.method == 'POST':

       user_form = UpdateUser(request.POST,instance=request.user)
       profile_form = UpdateProfile(request.POST,request.FILES,instance = request.user.profile)
       
       if user_form.is_valid() and profile_form.is_valid():
           user_form.save()
           profile_form.save()
           
           messages.success(request,f'Account updated')
           return redirect('blog-profile')
    else:
       user_form = UpdateUser(instance=request.user)
       profile_form = UpdateProfile(instance = request.user.profile)
       
    context = {
        'user_form':user_form,
        'profile_form': profile_form,
        
        
        
       }
    return render(request,'blog/profile.html',context )

# def details(request,image_id):
#     image = Image.objects.get(pk = image_id)
#     comments = Image.get_comments(image_id)
#     current_user = request.user
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit = False)
#             comment.image = image
#             comment.user = current_user
#             comment.save()


#     else:
#         form = CommentForm
#     return render(request,'blog/image-detail.html'{'form':form,'image':image,'comments':comments})

class ImageDetail(DetailView):
    model = Image
    template_name = 'blog/image-detail.html'
    context_object_name = 'image'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comments.objects.filter(image=self.get_object())
        data['comments'] = comments_connected
        data['form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comments(comments=request.POST.get('comments'),
                              username=self.request.user,
                              image=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)

class ImageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    template_name = 'blog/image-delete.html'
    context_object_name = 'image'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().username, self.request.user)

@login_required
def imagepreference(request, imageid, userpreference):

        if request.method == "POST":
                eachpost= get_object_or_404(Image, id=imageid)
                obj=''
                valueobj=''
                try:
                        obj= Preference.objects.get(user= request.user, image= eachpost)
                        valueobj= obj.value 
                        valueobj= int(valueobj)
                        userpreference= int(userpreference)
                        if valueobj != userpreference:
                                obj.delete()
                                upref= Preference()
                                upref.user= request.user
                                upref.image= eachpost
                                upref.value= userpreference
                                if userpreference == 1 and valueobj != 1:
                                        eachpost.likes += 1
                                        eachpost.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        eachpost.dislikes += 1
                                        eachpost.likes -= 1
                                upref.save()
                                eachpost.save()
                                context= {'eachpost': eachpost,
                                  'imageid': imageid}
                                return redirect('image-detail')
                        elif valueobj == userpreference:
                                obj.delete()
                                if userpreference == 1:
                                        eachpost.likes -= 1
                                elif userpreference == 2:
                                        eachpost.dislikes -= 1
                                eachpost.save()
                                context= {'eachpost': eachpost,
                                  'imageid': imageid}
                                return redirect('image-detail')
                                
                except Preference.DoesNotExist:
                        upref= Preference()
                        upref.user= request.user
                        upref.post= eachpost
                        upref.value= userpreference
                        userpreference= int(userpreference)
                        if userpreference == 1:
                                eachpost.likes += 1
                        elif userpreference == 2:
                                eachpost.dislikes +=1
                        upref.save()
                        eachpost.save()                            

                        context= {'post': eachpost,
                          'imageid': imageid}

                        return redirect('blog-home')

        else:
                eachpost= get_object_or_404(Image, id=imageid)
                context= {'eachpost': eachpost,
                          'imageid': imageid}

                return redirect('image-detail')