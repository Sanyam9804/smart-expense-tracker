import traceback
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def app(scope, receive, send):
    try:
        from backend.main import app as real_app
        await real_app(scope, receive, send)
    except Exception as e:
        err = traceback.format_exc().encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': err,
        })
