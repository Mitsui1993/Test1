from django.http import HttpResponse
from django.shortcuts import render

class BaseAdmin(object):
    list_display = "__all__"

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None

    @property
    def urls(self):
        from django.conf.urls import url
        """
        这里的self.model_class为之前传入的model类，所以一样可以取得app和model类名,由此设置别名，
        方便后续反向生成url.
        """
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$',self.changelist_view,name='%s_%s_changelist' % info),
            url(r'^add/$',self.add_view,name='%s_%s_add' % info),
            url(r'^(.+)/delete/$',self.delete_view,name='%s_%s_delete' % info),
            url(r'^(.+)/change/$',self.change_view,name='%s_%s_change' % info),
        ]
        return urlpatterns

    def add_view(self,request):
        """
        新增数据
        :param request:
        :return:
        """
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        data = "%s_%s_add" % info
        return HttpResponse(data)

    def delete_view(self,request,pk):
        """
        删除数据
        :param request:
        :return:
        """
        # self.model_class.objects.filter(id=pk).delete()
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_del" % info
        return HttpResponse(data)

    def change_view(self,request,pk):
        """
        修改数据
        :param request:
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_change" % info
        return HttpResponse(data)

    def changelist_view(self,request):
        """
        查看列表
        :param request:
        :return:
        """
        self.request = request
        result_list = self.model_class.objects.all()
        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'admin_obj':self  #此处self为自定制的Admin-models类对象
        }
        return render(request,'md/change_list.html',context)


class MySite(object):
    def __init__(self):
        self._registry = {}
        self.namespace = 'MyAdmin'
        self.app_name = 'MyAdmin'

    def register(self,model_class,xxx = BaseAdmin):
        self._registry[model_class] = xxx(model_class,self)
        """{
        modle类:BaseAdmin(model类， MySite()即site )
        }
        """

    def get_urls(self):
        from django.conf.urls import url,include
        ret = [
            url(r'^login/',self.login,name='login'),
            url(r'^logout/',self.login,name='logout'),
        ]
        #通过循环items获得每一个model类所在的app名，以及小写的类名
        for model_cls,admin_obj in self._registry.items():
            """
            model_cls为models类，admin_obj为BaseAdmin(model类， MySite()即site )，即传入2个参数的BaseAdmin对象，
            admin_obj.urls则执行BaseAdmin的urls方法
            """
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            # print(app_label,model_name)
            #拼接生成url，如/md/app01/userinfo/,再次分发拿到最终的/md/app01/userinfo/change_list等url
            ret.append(url(r'^%s/%s' % (app_label,model_name),include(admin_obj.urls)))

        return ret

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse('login')

site = MySite()