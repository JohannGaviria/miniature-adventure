from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Paginación personalizada que permite al cliente especificar el tamaño de la página
    mediante el parámetro de consulta `page_size`. El tamaño máximo de la página es 100.
    """
    page_size_query_param = 'page_size'
    max_page_size = 100


    def get_paginated_response(self, data):
        """
        Retorna una respuesta paginada con los enlaces de la siguiente y anterior página,
        el número total de elementos, el tamaño de la página y los resultados.

        Args:
            data (list): Lista de datos paginados.

        Returns:
            dict: Diccionario con la respuesta paginada.
        """
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        }
