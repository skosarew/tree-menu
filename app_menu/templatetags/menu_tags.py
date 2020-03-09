from django import template
from django.http import Http404
from app_menu.models import Category

register = template.Library()


def get_next_level_children(menu, root):
    subtree = []
    for m in menu:
        if m.left > root.left and m.right < root.right and m.level == \
                root.level + 1:
            subtree.append(m)
    return subtree


def get_requested_menu_item(menu, requested_url):
    for m in menu:
        if m.named_url == requested_url:
            return m


def get_parents_ids(menu, requested_menu_item):
    if requested_menu_item.parent_id:
        for m in menu:
            if m.id == requested_menu_item.parent_id:
                return get_parents_ids(menu, m) + [
                    requested_menu_item.parent_id]
    else:
        return []


def get_current_menu_item(menu, menu_name):
    for m in menu:
        if m.title == menu_name:
            return m


@register.inclusion_tag('app_menu/menus.html', takes_context=True)
def draw_menu(context, menu_name):
    menu = list(Category.objects.all())
    menu_item = get_current_menu_item(menu, menu_name)

    local_context = {'menu_item': menu_item}
    named_url = context['request'].path
    list_of_children = get_next_level_children(menu, menu_item)
    requested_menu_item = get_requested_menu_item(menu, named_url[1:])
    if requested_menu_item == 0:
        raise Http404

    unfolded_menu_item_ids = get_parents_ids(menu, requested_menu_item) + [
        requested_menu_item.id]

    local_context['unfolded_menu_item_ids'] = unfolded_menu_item_ids
    local_context['list_of_children'] = list_of_children
    local_context['menu'] = menu
    local_context['menu_item'] = menu_item
    local_context['nodes'] = []
    local_context['has_children'] = False if menu_item.right == \
                                             menu_item.left + 1 else True
    return local_context


@register.inclusion_tag('app_menu/menus.html', takes_context=True)
def draw_children(context, menu_item):
    local_context = {'menu_item': menu_item}
    list_of_children = get_next_level_children(context['menu'], menu_item)
    local_context['list_of_children'] = list_of_children
    if menu_item.right == menu_item.left + 1:
        local_context['has_children'] = False
        if context['nodes']:
            local_context['nodes'].append(menu_item)
        else:
            local_context['nodes'] = [menu_item]
    else:
        local_context['has_children'] = True
        local_context['nodes'] = context['nodes']
    local_context['menu'] = context['menu']

    if 'unfolded_menu_item_ids' in context:
        local_context['unfolded_menu_item_ids'] = context[
            'unfolded_menu_item_ids']
    return local_context
