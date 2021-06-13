from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.http import HttpResponseNotFound
from .forms import PostForm, CommentForm, RegistrationForm


def home(request):
    user_can_add_posts = False
    if request.user.is_authenticated and request.user.has_perm("blog.add_post") or request.user.is_superuser:
        user_can_add_posts = True

    if request.method == 'POST' and user_can_add_posts:
        received_post_form = PostForm(request.POST)
        if received_post_form.is_valid():
            obj = received_post_form.save(commit=False)
            obj.author = request.user
            obj.save()

    context = {
            "all_posts": Post.objects.all(),
            "post_form": PostForm(),
            "can_add_posts": user_can_add_posts,
    }
    return render(request, "home.html", context)


def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound("Пост не найден :(")

    if request.method == 'POST' and request.user.is_authenticated:
        received_comment_form = CommentForm(request.POST)
        if received_comment_form.is_valid():
            obj = received_comment_form.save(commit=False)
            obj.author = request.user
            obj.post = post
            obj.save()

    try:
        comments = Comment.objects.filter(post_id=pk)
    except Comment.DoesNotExist:
        comments = None

    context = {
            "post": post,
            "comments": comments,
            "comment_form": CommentForm
    }
    return render(request, 'post_detail.html', context)


def registration(request):
    def username_check(username):
        answer = []

        users = list(get_user_model().objects.all())
        for user in users:
            if username == user.username:
                answer.append("Такое имя пользователя уже занято")
                break
        return answer

    def password_check(password, password_repeat):
        answer = []

        if password != password_repeat:
            answer.append("Пароли не совпадают")

        strlength = len(password)
        if strlength < 8:
            answer.append("Пароль слишком короткий")

        chars = set('0123456789')
        nums_amount = 0
        for char in password:
            if char in chars:
                nums_amount += 1

        if nums_amount == strlength:
            answer.append("В вашем пароле должны быть другие символы, помимо цифр")

        return answer

    context = {
        "form": RegistrationForm(),
    }

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context['form'] = form
        data = dict(form.data)

        response = username_check(data['username'][0])
        response += password_check(data['password1'][0], data['password2'][0])
        if form.is_valid() and len(response) == 0:
            form.save()
            context['form'] = form
            return render(request, 'registration/registration_done.html', context)
        elif len(response) != 0:
            context['errors'] = response

    return render(request, 'registration/registration.html', context)

