class ProbeTesterExceptionSerializer:
    @staticmethod
    def serialize(exception):
        return {
            'error': {
                'source': exception.source,
                'code': exception.code,
                'message': str(exception)
            }
        }
