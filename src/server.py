import tempfile
import os
import traceback
from flask import Flask, request
from werkzeug.utils import secure_filename
from PredictDrawingCategory import CategoryPrediction
from PredictDesignPattern import PatternPrediction

app = Flask(__name__)


@app.route('/<string:classifierType>', methods=['GET', 'POST'])
def upload(classifierType=None):
    if not classifierType in ['category', 'pattern']:
        return '', 404
    if request.method == 'POST':
        if 'images' not in request.files:
            return 'no images uploaded', 403
        images = request.files.getlist('images')
        format = request.form['format']
        if not format in ['csv', 'json']:
            format = 'json'
        if format == 'csv':
            responseType = 'text/csv; charset=utf-8'
        elif format == 'json':
            responseType = 'application/json; charset=utf-8'

        tempDir = tempfile.TemporaryDirectory()
        filenames = []
        for image in images:
            filename = secure_filename(image.filename)
            if len(filename) > 0:
                filePath = os.path.join(tempDir.name, filename)
                image.save(filePath)
                filenames.append(filePath)
        if len(filenames) == 0:
            return 'no images uploaded', 403
        
        try:
            if classifierType == 'category':
                return CategoryPrediction(tempDir.name, format), 200, {'Content-Type': responseType}
            else:
                return PatternPrediction(tempDir.name, format), 200, {'Content-Type': responseType}
        except:
            return traceback.format_exc(), 403

    return '''
    <h1>Upload image(s) to classify {}</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="images" multiple>
        <div>
            Output format:
            <select name="format">
                <option selected>json</option>
                <option>csv</option>
            </select>
        </div>
        <input type="submit">
    </form>
    '''.format(classifierType)


if __name__ == '__main__':
    port = 8080
    print('Listening on port', port, '...', flush=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)