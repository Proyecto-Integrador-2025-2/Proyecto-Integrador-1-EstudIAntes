from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Challenge, Story, Tag

def challenges_list(request):
    q = request.GET.get("q", "").strip()
    tag = request.GET.get("tag")
    qs = Challenge.objects.filter(is_published=True)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(body__icontains=q))
    if tag:
        qs = qs.filter(tags__name=tag)
    page = Paginator(qs.order_by("-created_at").only("title","slug","summary","created_at"), 9).get_page(request.GET.get("page"))
    tags = Tag.objects.all().order_by("name")
    ctx = {"page": page, "q": q, "tag": tag, "tags": tags}
    return render(request, "content/challenges_list.html", ctx)

def challenge_detail(request, slug):
    obj = get_object_or_404(Challenge, slug=slug, is_published=True)
    return render(request, "content/challenge_detail.html", {"challenge": obj})

def stories_list(request):
    q = request.GET.get("q", "").strip()
    tag = request.GET.get("tag")
    qs = Story.objects.filter(is_published=True)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(teaser__icontains=q) | Q(body__icontains=q))
    if tag:
        qs = qs.filter(tags__name=tag)
    page = Paginator(qs.order_by("-created_at").only("title","slug","teaser","created_at"), 9).get_page(request.GET.get("page"))
    tags = Tag.objects.all().order_by("name")
    ctx = {"page": page, "q": q, "tag": tag, "tags": tags}
    return render(request, "content/stories_list.html", ctx)

def story_body_partial(request, slug):
    story = get_object_or_404(Story, slug=slug, is_published=True)
    return render(request, "content/_story_body.html", {"story": story})