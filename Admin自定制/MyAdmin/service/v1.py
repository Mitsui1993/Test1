from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http.request import QueryDict
from django.urls import reverse

class BaseAdmin(object):
    list_display = "__all__"
    add_or_edit_model_form = None

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def get_add_or_edit_model_form(self):
        """
        根据请求的model创建ModelForm
        :return:
        """
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):
                # class Meta:
                #     model = self.model_class
                #     fields = "__all__"
            #类的本质由type创建
            _m = type("Meta",(object,),{"model":self.model_class,"fields":"__all__"})
            MyModelForm = type("MyModelForm",(ModelForm,),{"Meta":_m})
            return MyModelForm

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
        if request.method == "GET":
            model_form_obj = self.get_add_or_edit_model_form()()
            # print(request.build_absolute_uri()) #url绝对路径
            # print(request.get_full_path()) #url相对路径

        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            if model_form_obj.is_valid():
                model_form_obj.save()
            #添加成功，跳转回之前页面：
                base_add_url = reverse("{0}:{1}_{2}_changelist".format(self.site.namespace, self.app_label, self.model_name))
                changelist_url = "{0}?{1}".format(base_add_url, request.GET.get("_changelistfilter"))
                return redirect(changelist_url)

        context = {
            'form': model_form_obj
        }
        return render(request,"md/add.html",context)

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
        obj = self.model_class.objects.filter(id=pk).first()
        if not obj:
            return HttpResponse("ID不存在！")
        if request.method == "GET":
            #instance将数据初始化获取默认值
            edit_model_form = self.get_add_or_edit_model_form()(instance=obj)
        else:
            #对于ModelForm，在修改数据时候，除了要将request.POST传入，还要讲修改的对象传入instance，
            #否则他将作为添加新数据处理。
            edit_model_form = self.get_add_or_edit_model_form()(data=request.POST,instance=obj)
            if edit_model_form.is_valid():
                edit_model_form.save()
                #修改成功，跳转回之前页面
                base_add_url = reverse(
                    "{0}:{1}_{2}_changelist".format(self.site.namespace, self.app_label, self.model_name))
                changelist_url = "{0}?{1}".format(base_add_url, request.GET.get("_changelistfilter"))
                return redirect(changelist_url)

        context = {"form":edit_model_form}
        return render(request,"md/change.html",context)

    def changelist_view(self,request):
        """
        查看列表
        :param request:
        :return:
        """
        #生成页面上，添加按钮
        #为了使添加后能跳转回原来的页面，这里生成一个QueryDict保存此时GET的url
        param_dict = QueryDict(mutable=True)
        if request.GET:
            #urlencode()可以把{"id":1,"name":"xx"}格式化为"id=1&name=xx"的字符串
            param_dict['_changelistfilter'] = request.GET.urlencode()

        #反向生成url，使每个models类跳转到不同的add url
        base_add_url = reverse("{0}:{1}_{2}_add".format(self.site.namespace,self.app_label,self.model_name))
        #根据当前url值拼接生成add url，使得添加数据后能找到跳转之前的页面
        add_url = "{0}?{1}".format(base_add_url,param_dict.urlencode())

        self.request = request
        result_list = self.model_class.objects.all()
        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'admin_obj':self,  #此处self为自定制的Admin-models类对象
            'add_url':add_url
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
            ret.append(url(r'^%s/%s/' % (app_label,model_name),include(admin_obj.urls)))

        return ret

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse('login')

site = MySite()