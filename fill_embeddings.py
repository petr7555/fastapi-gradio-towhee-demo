import towhee
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

connections.connect(host='127.0.0.1', port='19530')


def create_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, description='ids', is_primary=True, auto_id=False),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='embedding vectors', dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description='reverse image search')
    col = Collection(name=collection_name, schema=schema)

    # create IVF_FLAT index for collection.
    index_params = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }
    col.create_index(field_name="embedding", index_params=index_params)
    return col

collection = create_milvus_collection('reverse_image_search_norm', 2048)

dc = (
    towhee.read_csv('reverse_image_search.csv')
    .runas_op['id', 'id'](func=lambda x: int(x))
    .image_decode['path', 'img']()
    .image_embedding.timm['img', 'vec'](model_name='resnet50')
    .tensor_normalize['vec', 'vec']()
    .to_milvus['id', 'vec'](collection=collection, batch=100)
)
