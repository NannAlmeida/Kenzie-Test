import os
from flask import request, Response, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from kenzie.utils import allowed_files


def upload(app):

    """
    Função responsável por fazer upload de imagens.

    :param app: Instância do Flask
    :return: Response
    """

    try:
        if 'file' not in request.files:
            return Response(status=417, response=json.dumps({"message": 'Não há nenhum arquivo carregado!'}), mimetype='application/json')

        file = request.files['file']

        filename = secure_filename(file.filename)

        if not allowed_files(filename):
            return Response(status=415, response=json.dumps({"message": 'Formato de imagem inválido.'}), mimetype='application/json')

        exists = os.path.isfile(app.config['FILE_DIRECTORY'] + filename)

        if exists:
            return Response(status=409, response=json.dumps({"message": "A imagem {} já existe no servidor.".format(filename)}), mimetype='application/json')

        file.save(os.path.join(app.config['FILE_DIRECTORY'], filename))

        return Response(status=201, response=json.dumps({"message": 'A imagem {} foi salvo com sucesso!'.format(filename)}), mimetype='application/json')
    except RequestEntityTooLarge:
        return Response(status=413, response=json.dumps({"message": 'Imagem superior a 1mb, tente uma imagem mais leve'}), mimetype='application/json')
