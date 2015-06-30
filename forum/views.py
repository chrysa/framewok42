#-*-coding:utf-8 -*-
import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from forum import models
from forum.forms.CreateTopic import TopicForm
from forum.forms.ReplyTopic import PostForm

from django.utils.text import slugify


@login_required(login_url='/profil/login')
def display_all(request):
    return render(
        request,
        "forum/home.html",
        {
            'cat': models.ForumCat.objects.all().order_by('Name'),
        }
    )


@login_required(login_url='/profil/login')
def display_cat(request, cat):
    cat = models.ForumCat.objects.get(slug=cat)
    if cat is not None:
        last_mod = models.ForumTopic.objects.filter(CatParent=cat).order_by(
            'LastReply').order_by('CreateDate').reverse()
        return render(
            request,
            "forum/cat.html",
            {
                'cat': cat,
                'last_mod': last_mod,
            }
        )
    else:
        display_all(request)


@login_required(login_url='/profil/login')
def display_topic(request, cat, topic):
    thr = models.ForumTopic.objects.get(slug=topic)
    cat = models.ForumCat.objects.filter(slug=cat)[0]
    if thr is not None:
        post = models.ForumPost.objects.filter(TopicParent=thr)
        return render(
            request,
            "forum/topic.html",
            {
                'cat': cat,
                'topic': thr,
                'posts': post,
                'reply': PostForm(),
            }
        )
    else:
        cat = models.ForumCat.objects.filter(slug=cat)
        if cat is not None:
            display_cat(request, cat)
        else:
            display_all(request)


@login_required(login_url='/profil/login')
def create_topic(request, cat):
    form = TopicForm(request.POST)
    cat = models.ForumCat.objects.get(slug=cat)
    if form.is_valid():
        create = models.ForumTopic(
            CatParent=cat,
            Title=form.cleaned_data['Title'],
            Autor=request.user,
            Message=form.cleaned_data['Message'],
        ).save()
        if create is None:
            topic = models.ForumTopic.objects.filter(
                Title=form.cleaned_data['Title']
            ).filter(
                Autor=request.user
            ).filter(
                Message=form.cleaned_data['Message']
            )[0]
            return redirect(
                reverse(
                    'topic_cat',
                    kwargs={
                        'cat': cat.slug,
                        'topic': topic.slug,
                    }
                ),
                permanent=True
            )
        else:
            context = {
                'cat': cat,
                'error': _('thread_fail'),
                'form': form,
            }
    else:
        context = {
            'cat': cat,
            'form': form,
        }
    return render(
        request,
        "forum/create_topic.html",
        context,
    )


@login_required(login_url='/profil/login')
def reply_topic(request, cat, topic):
    form = PostForm(request.POST)
    top = models.ForumTopic.objects.get(slug=topic)
    if form.is_valid():
        models.ForumPost(
            TopicParent=top,
            Autor=request.user,
            Message=form.cleaned_data['Message'],
        ).save()
        models.ForumTopic.objects.filter(
            slug=topic
        ).update(
            LastReply=datetime.datetime.now()
        )
        return redirect(
            request.META['HTTP_REFERER'],
            permanent=True
        )
    else:
        if top.CatParent:
            return redirect(
                reverse(
                    'topic_cat',
                    kwargs={
                        'cat': cat.slug,
                        'topic': topic.slug,
                    }
                ),
                permanent=True
            )
        else:
            display_all(request)


@login_required(login_url='/profil/login')
def edit_topic(request, cat, topic):
    cat = models.ForumCat.objects.get(slug=cat)
    if request.POST:
        form = TopicForm(request.POST)
        if form.is_valid():
            update = models.ForumTopic.objects.filter(
                slug=topic
            ).update(
                Title=form.cleaned_data['Title'],
                Autor=request.user,
                slug=slugify(form.cleaned_data['Title']),
                Message=form.cleaned_data['Message'],
                LastModified=datetime.datetime.now()
            )
            if update is not None:
                topic = models.ForumTopic.objects.filter(
                    Title=form.cleaned_data['Title']
                ).filter(
                    Autor=request.user
                ).filter(
                    Message=form.cleaned_data['Message']
                )[0]
                return redirect(
                    reverse(
                        'topic_cat',
                        kwargs={
                            'cat': cat.slug,
                            'topic': topic.slug,
                        }
                    ),
                    permanent=True
                )
            else:
                context = {
                    'cat': cat,
                    'error': _('thread_fail'),
                    'form': form,
                }
        else:
            context = {
                'cat': cat,
                'form': form,
            }
    else:
        top = models.ForumTopic.objects.get(slug=topic)
        topic = {
            'Title': top.Title,
            'Message': top.Message,
        }
        form = TopicForm(topic)
        context = {
            'cat': cat,
            'form': form,
            'edit': 1,
        }
    return render(
        request,
        "forum/create_topic.html",
        context,
    )


@login_required(login_url='/profil/login')
def edit_post(request, cat, topic, post):
    cat = models.ForumCat.objects.get(slug=cat)
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            update = models.ForumPost.objects.filter(
                pk=post
            ).update(
                Message=form.cleaned_data['Message'],
                LastModified=datetime.datetime.now()
            )
            if update is not None:
                return redirect(
                    reverse(
                        'topic_cat',
                        kwargs={
                            'cat': cat.slug,
                            'topic': topic,
                        }
                    ),
                    permanent=True
                )

    else:
        post_sel = models.ForumPost.objects.get(pk=post)
        post_sel = {
            'Message': post_sel.Message,
        }
        context = {
            'cat': cat,
            'topic': topic,
            'post': post,
            'form': PostForm(post_sel),
        }
        return render(
            request,
            "forum/edit_post.html",
            context,
        )
