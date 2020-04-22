from django.shortcuts import render, get_object_or_404
from users.models import User
from groups.models import Group, UserGroup
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET


@csrf_exempt
@require_POST
def create_group(request):
    if request.POST.get('username') and request.POST.get('group_name'):
        username = request.POST.get('username')
        group_name = request.POST.get('group_name')
        user = get_object_or_404(User.objects.all(), username=username)

        user_group_names = [query.group.name for query in UserGroup.objects.filter(user=user)]
        if group_name not in user_group_names:
            group = Group(name=group_name)
            user_group = UserGroup(user=user, group=group)
            group.save()
            user_group.save()
            return HttpResponse('', status=200)
    return HttpResponse('', status=400)


@csrf_exempt
@require_POST
def join_group(request):
    if request.POST.get('username') and request.POST.get('group_id'):
        username = request.POST.get('username')
        group_id = request.POST.get('group_id')
        user = get_object_or_404(User.objects.all(), username=username)
        group = get_object_or_404(Group.objects.all(), id=group_id)

        group_name = group.name
        user_group_names = [query.group.name for query in UserGroup.objects.filter(user=user)]
        if group_name not in user_group_names:
            user_group = UserGroup(user=user, group=group)
            user_group.save()
            return HttpResponse('', status=200)
    return HttpResponse('', status=400)


@csrf_exempt
@require_POST
def leave_group(request):
    if request.POST.get('username') and request.POST.get('group_id'):
        username = request.POST.get('username')
        group_id = request.POST.get('group_id')
        user = get_object_or_404(User.objects.all(), username=username)
        group = get_object_or_404(Group.objects.all(), id=group_id)

        UserGroup.objects.filter(user=user, group=group).delete()
        return HttpResponse('', status=200)
    return HttpResponse('', status=400)


@csrf_exempt
@require_GET
def group_list(request):
    if request.POST.get('username') and request.POST.get('group_id'):
        username = request.POST.get('username')
        group_id = request.POST.get('group_id')
        user = get_object_or_404(User.objects.all(), username=username)
        group = get_object_or_404(Group.objects.all(), id=group_id)

        return JsonResponse([query.group.name for query in UserGroup.objects.filter(user=user)], safe=False)
    return HttpResponse('', status=400)
