from django.db.models import Prefetch
from django.shortcuts import render
from articles.models import Article, Scope


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'

    articles_with_relations = Article.objects.prefetch_related(
        Prefetch(
            'scopes',
            queryset=Scope.objects.select_related('tag')
        )
    ).order_by(ordering)

    context = {
        'object_list': articles_with_relations,
    }

    return render(request, template, context)
