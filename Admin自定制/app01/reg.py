from app01 import models
from MyAdmin.service import v1
from django.utils.safestring import mark_safe

class AdminUserInfo(v1.BaseAdmin):

    def func(self,obj):
        """
        反向生成url，使每一条数据可以跳转到详细页执行change视图
        :param obj: 数据表行数据
        :return: 编辑按钮跳转url
        """
        from django.urls import reverse
        #反向生成url,需要namespace,app跟类名称在注册时传入
        name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
        #obj为查询出的数据表每一行数据
        url = reverse(name, args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self,obj):
        """
        生成checkbox标签
        :param obj: 行数据
        :return: 带有数据行id的checkbox标签
        """
        tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)

    list_display = [checkbox,'id','username',func]

"""
这里注册后,self._registry[model_class] = xxx(model_class,self)
原来的字典就变为{UserInfo:AdminUserInfo(UserInfo,site)},
因此传过去的context字典中的admin_obj不再是BaseAdmin对象，而是这里的AdminUserInfo对象，它除了能继承
BaseAdmin类的各种方法，还有自己定制的func 以及checkbox方法.
"""
v1.site.register(models.UserInfo,AdminUserInfo)

class AdminRole(v1.BaseAdmin):
    list_display = ['id', 'name']

v1.site.register(models.Role,AdminRole)

