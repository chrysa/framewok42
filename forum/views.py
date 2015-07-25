#-*-coding:utf-8 -*-
"""
:module: FORUM.VIEWS
:synopsis: generate QLL CONTENT OF FORUM

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015:
:var logger_error: logger error
:var logger_info: logger info
:seealso: forum.models
:seealso: forum.forms.CreateTopic.TopicForm
:seealso: forum.forms.ReplyTopic.PostForm
:seealso: generate_logs.functions.info_load_log_message
"""
import datetime
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.text import slugify

from forum import models
from generate_logs.functions import info_load_log_message
from forum.forms.CreateTopic import TopicForm
from forum.forms.ReplyTopic import PostForm

logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


@login_required
def display_all(request):
    """display forum's category

    :param request: object contain context of request
    :type request: object
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    return render(
        request,
        "forum/home.html",
        {
            'cat': models.ForumCat.objects.all().order_by('Name'),
        }
    )


@login_required
def display_cat(request, cat):
    """display category's topic list

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
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


@login_required
def display_topic(request, cat, topic):
    """display category's topic list

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :param topic: slug of topic
    :type topic: slug
    :var cat: get the the selected category
    :var thr: get the first message of the topic
    :var post: get lit of related post of thr
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    cat = models.ForumCat.objects.filter(slug=cat)[0]
    thr = models.ForumTopic.objects.get(slug=topic)
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


@login_required
def create_topic(request, cat):
    logger_info.info(info_load_log_message(request))
    form = TopicForm(request.POST)
    cat = models.ForumCat.objects.get(slug=cat)
    if form.is_valid():
        try:
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
        except:
            logger_error.error(_('save_topic'))
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


@login_required
def reply_topic(request, cat, topic):
    logger_info.info(info_load_log_message(request))
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


@login_required
def edit_topic(request, cat, topic):
    logger_info.info(info_load_log_message(request))
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


@login_required
def edit_post(request, cat, topic, post):
    logger_info.info(info_load_log_message(request))
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
