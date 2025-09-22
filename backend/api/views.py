from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from .models import Ciclovia
from .serializers import CicloviaSerializer
from silk.profiling.profiler import silk_profile

class BuscaPorLogradouro(APIView):
    """
    Endpoint para buscar registros pelo nome do logradouro.
    Exemplo de uso: GET /api/busca-logradouro/?logradouro_nome=R MARIANTE
    """
    @silk_profile(name='view_get_busca_logradouro_orm')
    def get(self, request):
        logradouro = request.GET.get('logradouro_nome')
        if not logradouro:
            return Response(
                {'error': 'Parâmetro logradouro_nome é obrigatório.'}, 
                status=400
            )

        # Usando ORM para a busca
        queryset = Ciclovia.objects.filter(
            logradouro_nome__icontains=logradouro.strip().upper()
        )

        # Ordenação
        ordering = request.GET.get('ordering', 'asc').lower()
        if ordering == 'desc':
            queryset = queryset.order_by('-implantacao')
        else:
            queryset = queryset.order_by('implantacao')

        # Paginação com Paginator do Django
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('pagesize', 10)
        paginator = Paginator(queryset, page_size)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return Response({
                'page': page_number,
                'pagesize': page_size,
                'total': paginator.count,
                'results': []
            })

        serializer = CicloviaSerializer(page_obj.object_list, many=True)

        return Response({
            'page': page_obj.number,
            'pagesize': int(page_size),
            'total': paginator.count,
            'results': serializer.data
        })

class BuscaPorImplantacao(APIView):
    """
    Endpoint para buscar registros pela data de implantação.
    Exemplo de uso: GET /api/busca-implantacao/?implantacao=2018-06-21
    """
    @silk_profile(name='view_get_busca_implantacao_orm')
    def get(self, request):
        implantacao = request.GET.get('implantacao')
        if not implantacao:
            return Response({'error': 'Parâmetro implantacao é obrigatório.'}, status=400)

        # Usando ORM para a busca
        queryset = Ciclovia.objects.filter(implantacao=implantacao.strip())

        # Paginação
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('pagesize', 10)
        paginator = Paginator(queryset, page_size)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return Response({
                'page': page_number,
                'pagesize': page_size,
                'total': paginator.count,
                'results': []
            })

        serializer = CicloviaSerializer(page_obj.object_list, many=True)

        return Response({
            'page': page_obj.number,
            'pagesize': int(page_size),
            'total': paginator.count,
            'results': serializer.data
        })