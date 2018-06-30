from yabe import yabe


@yabe.route('/', methods=['GET'])
def router_index():
    return 'Hello World.'
