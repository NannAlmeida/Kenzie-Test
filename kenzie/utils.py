def get_extension(filename):
    extension = filename.split('.')

    return extension[1]

def allowed_files(filename):
    types_allowed = {'png', 'jpg', 'gif'}
    extension = get_extension(filename)

    return extension.lower() in types_allowed