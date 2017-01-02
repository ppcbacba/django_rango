from django import template

from rango.models import Category

register = template.Library()#全局register变量，它是用来注册你自定义标签和过滤器的


@register.inclusion_tag('rango/cats.html')#注册tag
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),'act_cat':cat}
