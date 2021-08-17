import os
from flask import Response, json, send_file, request

from kenzie.utils import get_extension


def list_files(app, type):
    """
    Função responsável por retornar todos os arquivos ou arquivos em especifico no diretório upload.

    :param Flask app: Instância do flask
    :param str type: Tipo do arquivo
    :return: Response
    """

    try:
        files = os.listdir(app.config['FILE_DIRECTORY'])
    except OSError:
        return Response(status=500, response=json.dumps({"message": 'Erro ao carregar a pasta'}), mimetype='application/json')

    if type is None:
        return Response(status=200, response=json.dumps({"files": selected_files}), mimetype='application/json')

    selected_files = []

    for file in files:
        extension = get_extension(file)

        if extension == type:
            selected_files.append(file)

    return Response(status=200, response=json.dumps({"files": selected_files}), mimetype='application/json')


def download(app, filename):

    """
    Função responsável por fazer download lado do cliente de algum arquivo específico.

    :param app: Instância do Flask
    :param filename: Nome do arquivo
    :return: Response
    """

    try:
        get_file = os.path.join(app.config['FILE_DIRECTORY'], filename)

        return send_file(get_file)
    except FileNotFoundError:
        return Response(status=404, response=json.dumps({"message": "O arquivo ainda não existe."}), mimetype='application/json')


def download_dir_as_zip(app):

    """
    Função responsável por fazer download de arquivos em especifico comprimidos

    :param app: Instancia do Flask
    :return: Response
    """

    try:
        file_type = request.args['file_type']
        compression_rate = request.args['compression_rate']

        files = os.listdir(app.config['FILE_DIRECTORY'])

        selected_files = []

        for file in files:
            extension = get_extension(file)

            if extension == file_type:
                selected_files.append(app.config['FILE_DIRECTORY'] + file)

        files_formatted = ' '.join(selected_files)
        os.system('zip -{} -r /tmp/download.zip {}'.format(compression_rate, files_formatted))

        return send_file('/tmp/download.zip')
    except:
        return Response(status=404, response=json.dumps({"message": 'Não existe imagens desse tipo no diretório'}), mimetype='application/json')