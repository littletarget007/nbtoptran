from django import template
from ..models import News

register = template.Library()

@register.simple_tag

def archives():
	return News.objects.dates('pub_date','month',order='DESC')
@register.simple_tag
def get_recent_news(num=3):
	return News.objects.all().order_by('-pub_date')[:num]
