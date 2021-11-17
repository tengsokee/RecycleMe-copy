"""socialMedia views.py

This script defines the views for socialMedia functionalities. 

Author: Desmond, Akshita and Sok Ee 

This file can also be imported as a module and contains the following
classes or functions:
    * PostListView - returns posts order by publication dates
    * PostDetailView - the a specific post with its comments
    * PostEditView - returns the specific post for editing
"""
# import packages for getting url paths and http objects
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

# import packages for views
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from .models import User, PostManager, Post, Comment, CommentManager, Image

# packages for authentication
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth import authenticate, login
# from .decorators import unauthenticated_user, admin_only, allow_permission_users
# from django.contrib.auth.models import Group


from .forms import PostForm, CommentForm, UserRegisterForm
from . import urls
from django.conf.urls import include, url
from .models import character_limit

class PostListView(LoginRequiredMixin, View):
    """ Creates view for post list 
    """
    def get(self, request, *args, **kwargs):
        """ Function for getting list of posts to display
        """
        posts = Post.objects.all().order_by('-pub_date')
        form = PostForm()
        bookmarked_posts = Post.objects.filter(bookmark = request.user)

        context = {
            'post_list': posts,
            'form': form,
            'bookmarked_posts': bookmarked_posts
        }

        return render(request, 'socialMedia/post_list.html', context)

    def post(self, request, *args, **kwargs):
        """ Function for sending users' posts to django server
        """
        posts = Post.objects.all().order_by('-pub_date')
        form = PostForm(request.POST)

        if form.is_valid():
            if(len(form.cleaned_data['content'])>character_limit):
                error_message = "Not posted! 255-character-limit exceeded"
            else:
                error_message = ""
                new_post = form.save(commit=False)
                new_post.author = User.objects.get(username=request.user)
                new_post.save()
                return HttpResponseRedirect(reverse('community:home'))
        context = {
            'post_list': posts,
            'form': form,
            'error_message':error_message
        }

        return render(request, 'socialMedia/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    """ Creates view for post details 
    """
    def get(self, request, pk, *args, **kwargs):
        """ Function for getting post details and its list of comments """

        post = Post.objects.get(pk=pk)
        form = CommentForm()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post).order_by('-pub_date')
        is_bookmarked = False

        if stuff.bookmark.filter(id=self.request.user.id).exists():
            is_bookmarked=True

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'test1': request.user,
            'test2': post.author,
            'is_bookmarked': is_bookmarked,
        }

        return render(request, 'socialMedia/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        """ Function for uploading posts and comments
        """
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            if(len(form.cleaned_data['content'])>character_limit):
                error_message = "Not posted! 255-character-limit exceeded"
            else:
                new_comment = form.save(commit=False)
                new_comment.author = User.objects.get(username=request.user)
                new_comment.post = post
                new_comment.save()
                return HttpResponseRedirect(reverse('community:post-detail', kwargs = {"pk":pk}))

        comments = Comment.objects.filter(post=post).order_by('-pub_date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'error_message':error_message
        }

        return render(request, 'socialMedia/post_detail.html', context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Creates view when post is edited 
    """
    model = Post
    fields = ['content']
    template_name = 'socialMedia/post_edit.html'

    def get_context_data(self, **kwargs):
        """ Function specifies the content to return for the view
        """
        context = super(PostEditView, self).get_context_data(**kwargs)
        context['post_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        """ Function will get the url to the page 
        """
        pk = self.kwargs['pk']
        return reverse_lazy('community:post-detail', kwargs={'pk': pk})

    def test_func(self):
        """ Function will get the author of post 
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Creates view when post is deleted 
    """
    model = Post
    template_name = 'socialMedia/post_delete.html'
    success_url = reverse_lazy('community:home')

    def test_func(self):
        """ Function will get the author of post 
        """
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Creates view when comment is deleted 
    """
    model = Comment
    template_name = 'socialMedia/comment_delete.html'

    def get_context_data(self, **kwargs):
        """ Function specifies the content to return for the view
        """
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context['post_id'] = self.kwargs['post_pk']
        return context

    def get_success_url(self):
        """ Function will get the url to the page
        """
        pk = self.kwargs['post_pk']
        return reverse_lazy('community:post-detail', kwargs={'pk': pk})

    def test_func(self):
        """ Function will get the author of post 
        """
        post = self.get_object()
        return self.request.user == post.author


class ProfileView(View):
    """ Creates view for profile 
    """
    def get(self, request, *args, **kwargs):
        """ Function will get profile information for display
        """
        user = request.user
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(author=user).order_by('-pub_date')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
        }
        return render(request, 'socialMedia/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Creates view when profile is edited 
    """
    model = Profile
    fields = ['name', 'bio', 'image']
    template_name = 'socialMedia/profile_edit.html'

    def get_success_url(self):
        """ Function will get the url to the page 
        """
        pk = self.kwargs['pk']
        return reverse_lazy('community:profile', kwargs={'slug': pk})

    def test_func(self):
        """ Function will get the author of post 
        """
        profile = self.get_object()
        return self.request.user == profile.user



def register(request):
    """ This function will register account with admin privileges 
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # group = Group.objects.get(name='user')
            # user.groups.add(group)
            messages.success(request, f'Your account has been created! You can now login!')
            return redirect('community:loginPage')
        """ If registering is successful, they will be redirected to the login page 
        """

    else:
        form = UserRegisterForm()
    return render(request, 'socialMedia/register.html', {'form': form})



def registerAdmin(request):
    """ This function will register account with admin privileges 
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # group = Group.objects.get(name='admin')
            # user.groups.add(group)
            messages.success(request, f'Your account has been created! You can now login!')
            return redirect('community:loginPage')
        """ If registering is successful, they will be redirected to the login page 
        """

    else:
        form = UserRegisterForm()
    return render(request, 'socialMedia/registeradmin.html', {'form': form})



def accountManager(username, password):
    """ This function will check if users are authenticated

        Parameters
        ----------
        username : str
            Unique string of user
        password : str
            Unique string of password

        Returns
        -------
        user
            A user

    """
    user = authenticate(username=username, password=password)
    """ It will check if their username and password set are found in the database or not 
    """

    return user



def loginPage(request):
    """ This function will allow users to login to their account 
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = accountManager(username, password)
        """ Calls account manager to authenticate account 
        """
        if user is not None:
            login(request, user)
            return redirect('community:home')
            """ If a user was found, they will be redirected to the homepage 
            """
        else:
            messages.info(request, 'Username OR password is incorrect. Please try again.')
            """ Else a message will be shown 
            """

    context = {}
    return render(request, 'socialMedia/login.html', context)


class AddLike(LoginRequiredMixin, View):
    """ Creates likes when user presses the like button
    """
    def post(self, request, pk, *args, **kwargs):
        """ This function updates likes for a post.
        """
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(LoginRequiredMixin, View):
    """ Creates dislikes when user presses the dislike button
    """
    def post(self, request, pk, *args, **kwargs):
        """ This function will updates dislikes for a post.
        """
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class BookmarkPost(LoginRequiredMixin, View):
    """ This function will allow users to bookmark posts
    """
    def post(self, request, pk, *args, **kwargs):
        """ This function update bookmark for a post
        """
        post = Post.objects.get(pk=pk)

        is_bookmarked = False
        if post.bookmark.filter(id=request.user.id).exists():
            post.bookmark.remove(request.user)
            is_bookmarked = False
        else:
            post.bookmark.add(request.user)
            is_bookmarked = True

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class BookmarkListView(LoginRequiredMixin, View):
    """ Creates bookmark list view
    """
    model = Post
    def get(self, request, *args, **kwargs):
        """ This function will get bookmarks for a user
        """
        posts = Post.objects.filter(bookmark = request.user).order_by('-pub_date')

        context = {
            'posts': posts,
        }

        return render(request, 'socialMedia/bookmark_list.html', context)
