import uuid

def gen_face_id():
    return (str(uuid.uuid1())).replace("-", "")