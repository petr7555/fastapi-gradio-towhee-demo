import towhee
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

with towhee.api() as api:
    app1 = (
        api.map(lambda x: x + ' -> 1')
        .map(lambda x: x + ' => 1')
        .serve('/app1', app)
    )

with towhee.api['x']() as api:
    app2 = (
        api.runas_op['x', 'x_plus_1'](func=lambda x: x + ' -> 2')
        .runas_op['x_plus_1', 'y'](func=lambda x: x + ' => 2')
        .select['y']()
        .serve('/app2', app)
    )

with towhee.api() as api:
    app3 = (
        api.parse_json()
        .runas_op['x', 'x_plus_1'](func=lambda x: x + ' -> 3')
        .runas_op['x_plus_1', 'y'](func=lambda x: x + ' => 3')
        .select['y']()
        .serve('/app3', app)
    )

client = TestClient(app)
print(client.post('/app1', content='1').text)
print(client.post('/app2', content='2').text)
print(client.post('/app3', content='{"x": "3"}').text)
