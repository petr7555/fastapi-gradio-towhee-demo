import gradio
import pandas as pd
import towhee
from gradio.components import Image
from pymilvus import connections
from towhee.types.image_utils import from_pil

connections.connect(host='127.0.0.1', port='19530')
df = pd.read_csv('reverse_image_search.csv')
id_img = df.set_index('id')['path'].to_dict()

with towhee.api() as api:
    milvus_search_function = (
        api.runas_op(func=lambda img: from_pil(img))
        .image_embedding.timm(model_name='resnet50')
        .tensor_normalize()
        .milvus_search(collection='reverse_image_search_norm', limit=5)
        .runas_op(func=lambda res: [id_img[x.id] for x in res])
        .as_function()
    )

interface = gradio.Interface(
    milvus_search_function,
    Image(type="pil", source='upload'),
    [Image(type="filepath") for _ in range(5)]
)

interface.launch()
