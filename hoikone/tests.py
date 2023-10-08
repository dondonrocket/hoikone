from django.test import TestCase

# Create your tests here.
    if query:
        keywords = query.split()  # キーワードをスペースで分割
        q_objects = Q()  # 空のQオブジェクトを作成

        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(feature__icontains=keyword)

        queryset = self.queryset.filter(q_objects)

        request.session['search_query'] = query

    else:
        query = request.session.get('search_query')
        if query:
            keywords = query.split()
            q_objects = Q()

            for keyword in keywords:
                q_objects |= Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(feature__icontains=keyword)

            queryset = self.queryset.filter(q_objects)
        else:
            queryset = self.queryset
            request.session.pop('search_query', None)












                    query = request.GET.get('query')
        if query:
            queryset = self.queryset.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(feature__icontains=query))
            # 検索条件がクエリパラメータとして提供された場合、セッションに保存する
            request.session['search_query'] = query

        else:
            # クエリパラメータが提供されていない場合、セッションから検索条件を取得する
            query = request.session.get('search_query')
            if query:
                queryset = self.queryset.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(feature__icontains=query))
            else:
                queryset = self.queryset
                # 検索条件が提供されなかった場合、セッションから検索条件を削除する
                request.session.pop('search_query', None)
        if not queryset.exists():  # クエリセットにデータが存在しない場合の処理
            context = {
                'count': '0'
            }
            return render(request, 'nursery-list.html', context)
#        pagination_class = PageNumberPagination()
        paginator = Paginator(queryset, 6)
        page_number = request.GET.get('page')
        NurseryDatafinal = paginator.get_page(page_number)
        totalpage=NurseryDatafinal.paginator.num_pages

        paginated_queryset = self.paginate_queryset(queryset.order_by('name'))



        serializer = NurserySerializer(paginated_queryset, many=True)

        # シリアライザーのデータとページネーションの情報をテンプレートに渡す
        context = {
            'search': serializer.data,
            'result_count': len(queryset),
            'pagination': NurseryDatafinal,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'current_page_number':page_number,
        }

        return render(request, 'nursery-list.html', context)
