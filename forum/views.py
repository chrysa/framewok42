# -*-coding:utf-8 -*-
"""
:module: forum.views
:synopsis: generate all content of forum

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
        "forum/home.html", {
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
    try:
        cat = models.ForumCat.objects.get(slug=cat)
        last_mod = models.ForumTopic.objects.filter(
            CatParent=cat
        ).order_by('LastReply').order_by('CreateDate').reverse()
        return render(
            request,
            "forum/cat.html", {
                'cat': cat,
                'last_mod': last_mod,
            }
        )
    except:
        return display_all(request)


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
    try:
        cat = models.ForumCat.objects.filter(slug=cat)[0]
        try:
            thr = models.ForumTopic.objects.get(slug=topic)
            post = models.ForumPost.objects.filter(TopicParent=thr)
            return render(
                request,
                "forum/topic.html", {
                    'cat': cat,
                    'topic': thr,
                    'posts': post,
                    'reply': PostForm(),
                }
            )
        except:
            return display_cat(request, cat)
    except:
        return display_all(request)


@login_required
def create_topic(request, cat):
    """create new topic

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :var cat: categorie object selected by slug
    :var form: form for create topic
    :var errors: dict of process error
    :var create: new topic
    :var topic: get the new topic
    :var context: define the context for display page
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    cat = models.ForumCat.objects.get(slug=cat)
    form = TopicForm(request.POST)
    error = {}
    if request.method == 'POST':
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
                error['save_topic'] = _('topic_fail')
        else:
            if not request.POST['Title']:
                error['no_title'] = _("topic_must_contain_title")
            if not request.POST['Message']:
                error['no_title'] = _("topic_must_contain_message")
    context = {
        'cat': cat,
        'form': form,
        'error': error,
    }
    return render(
        request,
        "forum/create_topic.html",
        context,
    )


@login_required
def reply_topic(request, cat, topic):
    """save new reply

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :var topic: topic slug
    :type topic: slug
    :var form: form for topic reply
    :var top: get the new topic
    :return: HTTPResponse
    """
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
            return display_all(request)


@login_required
def edit_topic(request, cat, topic):
    """display process for edit topic

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :param topic: slug of topic
    :type topic: slug
    :var cat: select category by slug
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    try:
        cat = models.ForumCat.objects.get(slug=cat)
        wrong_cat = 0
    except:
        wrong_cat = 1
    try:
        models.ForumTopic.objects.get(slug=topic)
        wrong_topic = 0
    except:
        wrong_topic = 1
    if not wrong_cat and not wrong_topic and request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            update = models.ForumTopic.objects.filter(slug=topic).update(
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
                )
                return redirect(
                    reverse(
                        'topic_cat',
                        kwargs={
                            'cat': cat.slug,
                            'topic': topic[0].slug
                        }
                    ),
                    permanent=True
                )
            else:
                context = {
                    'cat': cat,
                    'error': _('thread_fail'),
                    'form': form
                }
        else:
            top = models.ForumTopic.objects.get(slug=topic)
            form = TopicForm(
                {
                    'Title': top.Title,
                    'Message': top.Message
                }
            )
            context = {
                'cat': cat,
                'form': form
            }
    elif wrong_cat and wrong_topic:
        return redirect(
            reverse('forum'),
            permanent=True
        )
    elif wrong_cat:
        top = models.ForumTopic.objects.get(slug=topic)
        return redirect(
            reverse(
                'edit_topic', kwargs={
                    'cat': top.CatParent.slug,
                    'topic': top.slug
                }
            ),
            permanent=True
        )
    elif wrong_topic:
        return redirect(
            reverse(
                'cat', kwargs={
                    'cat': cat
                }
            ),
            permanent=True
        )
    else:
        top = models.ForumTopic.objects.get(slug=topic)
        topic = {
            'Title': top.Title,
            'Message': top.Message
        }
        form = TopicForm(topic)
        context = {
            'cat': cat,
            'form': form,
            'edit': 1
        }
    return render(
        request,
        "forum/create_topic.html",
        context
    )


@login_required
def edit_post(request, cat, topic, post):
    """display process for edit post

    :param request: object contain context of request
    :type request: object
    :param cat: slug of categorie
    :type cat: slug
    :var topic: topic slug
    :type topic: slug
    :var errors: dict of process error
    :var cat: select cat by slug
    :var form: form for edit post
    :var update: select post to update and update him
    :var post_sel: get the post
    :var context: define the context for display topic
    :return: HTTPResponse
    """
    error = {}
    logger_info.info(info_load_log_message(request))
    cat = models.ForumCat.objects.get(slug=cat)
    if request.POST:
        form = PostForm(request.POST)
        if request.POST['Message'] is not None and form.is_valid():
            try:
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
            except:
                return display_topic(request, cat, topic)
        else:
            post_sel = models.ForumPost.objects.get(pk=post)
            error['Message'] = _('post_must_contain_message')
    else:
        post_sel = models.ForumPost.objects.get(pk=post)
    return render(
        request,
        "forum/edit_post.html", {
            'cat': cat,
            'topic': topic,
            'post': post,
            'error': error,
            'form': PostForm({'Message': post_sel.Message}),
        },
    )
