from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
import markdown
from toptran import models
from django.shortcuts import render,get_object_or_404

from .models import News,Knowledge,Case,Index,Category,Product



def index(request):
	index_list = Index.objects.all()
	return render(request, 'toptran/index.html', context={'index_list': index_list})




#以下被NewsView类代替：
#def news(request):
	#news_list = News.objects.all()
	#return render(request, 'toptran/news.html', context={'news_list': news_list})
class NewsView(ListView):
	model = News
	template_name = 'toptran/news.html'
	context_object_name = 'news_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章

	paginate_by = 10
	def get_context_data(self, **kwargs):


  
        #在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        #例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        #这里传递了一个 {'post_list': post_list} 字典给模板。
        #在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        #所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
     

        # 首先获得父类生成的传递给模板的字典。

		context = super().get_context_data(**kwargs)


        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
		context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:

            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
			return {}

        # 当前页左边连续的页码号，初始值为空
		left = []

        # 当前页右边连续的页码号，初始值为空
		right = []

        # 标示第 1 页页码后是否需要显示省略号
		left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
		right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
		first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
		last = False

        # 获得用户当前请求的页码号
		page_number = page.number

        # 获得分页后的总页数
		total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:


            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
			if right[-1] < total_pages - 1:

				right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
			if left[0] > 2:
				left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
			if left[0] > 1:
				first = True
		else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:

				right_has_more = True
			if right[-1] < total_pages:
				last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:

				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

		return data


def newsdetail(request,pk):

	news = get_object_or_404(News,pk=pk)
	news.increase_views()
	news.body = markdown.markdown(news.body,
		                          extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
	return render(request,'toptran/newsdetail.html',context={'news':news})






class KnowledgeView(ListView):
	model = Knowledge
	template_name = 'toptran/knowledge.html'
	context_object_name = 'knowledge_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章

	paginate_by = 10
	def get_context_data(self, **kwargs):

  
        #在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        #例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        #这里传递了一个 {'post_list': post_list} 字典给模板。
        #在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        #所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
     

        # 首先获得父类生成的传递给模板的字典。

		context = super().get_context_data(**kwargs)


        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
		context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:

            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
			return {}

        # 当前页左边连续的页码号，初始值为空
		left = []

        # 当前页右边连续的页码号，初始值为空
		right = []

        # 标示第 1 页页码后是否需要显示省略号
		left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
		right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
		first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
		last = False

        # 获得用户当前请求的页码号
		page_number = page.number

        # 获得分页后的总页数
		total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:


            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
			if right[-1] < total_pages - 1:

				right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
			if left[0] > 2:
				left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
			if left[0] > 1:
				first = True
		else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:

				right_has_more = True
			if right[-1] < total_pages:
				last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:

				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

		return data


def knowledgedetail(request,pk):

	knowledge = get_object_or_404(Knowledge,pk=pk)
	knowledge.increase_views()
	knowledge.body = markdown.markdown(knowledge.body,
		                          extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
	return render(request,'toptran/knowledgedetail.html',context={'knowledge':knowledge})


























def contact(request):
	return render(request, 'toptran/contact.html')



def about(request):
	return render(request, 'toptran/about.html')





class CaseView(ListView):
	model = Case
	template_name = 'toptran/case.html'
	context_object_name = 'case_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章

	paginate_by = 15
	def get_context_data(self, **kwargs):

  
        #在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        #例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        #这里传递了一个 {'post_list': post_list} 字典给模板。
        #在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        #所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
     

        # 首先获得父类生成的传递给模板的字典。

		context = super().get_context_data(**kwargs)


        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
		context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:

            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
			return {}

        # 当前页左边连续的页码号，初始值为空
		left = []

        # 当前页右边连续的页码号，初始值为空
		right = []

        # 标示第 1 页页码后是否需要显示省略号
		left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
		right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
		first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
		last = False

        # 获得用户当前请求的页码号
		page_number = page.number

        # 获得分页后的总页数
		total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:


            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
			if right[-1] < total_pages - 1:

				right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
			if left[0] > 2:
				left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
			if left[0] > 1:
				first = True
		else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:

				right_has_more = True
			if right[-1] < total_pages:
				last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:

				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

		return data



def product_list(request,category_slug=None):
	
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter()
	if category_slug:
		category = get_object_or_404(Category,slug=category_slug)
		products = products.filter(category=category)



	#all_products = Product.objects.all()
	#paginator = Paginator(all_products, 1) # 每页显示 25 个联系人

	#page = request.GET.get('page')
	#try:

		#contacts = paginator.page(page)
	#except PageNotAnInteger:

        # 如果用户请求的页码号不是整数，显示第一页
 		#contacts = paginator.page(1)
	#except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
		#contacts = paginator.page(paginator.num_pages)

	return render(request,'toptran/product_list.html',
		        {'category':category,
		          'categories':categories,
		          'products':products})









  
def product_detail(request,id,slug):
	product = get_object_or_404(Product,id=id,slug=slug)
	
	return render(request,'toptran/product_detail.html',{'product':product})
