from django import template


register = template.Library()


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(description):
    replace_value = {"редиска": "р******"}
    for i, j in replace_value.items():
        description = description.replace(i, j)
    return description

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
