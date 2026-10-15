#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse
import base64

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


def json_response(data, status=200):
    """Convert a Python dictionary into a JSON HTTP response."""
    return Response(
        response=jsonpickle.encode(data),
        status=status,
        mimetype="application/json"
    )

def image_dimensions(image_bytes):
    """Read an image from bytes and return its dimensions."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        return {
            'width': img.size[0],
            'height': img.size[1]
        }

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )



@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    # Read the JSON payload sent by the client.
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return json_response(
            {'error': 'Expected a JSON object containing a and b'},
            status=400
        )

    # Extract the two vectors before validating
    a = data.get('a')
    b = data.get('b')

    # Check that both vectors are lists.
    if not isinstance(a, list) or not isinstance(b, list):
        return json_response(
            {'error': 'a and b must be lists'},
            status=400
        )

    # Check that the vectors have equal lengths.
    if len(a) != len(b):
        return json_response(
            {'error': 'Vectors must have the same length'},
            status=400
        )

    # Check that all elements are numbers.
    for value in a + b:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return json_response(
                {'error': 'Vector elements must be numbers'},
                status=400
            )

    # Calculate the dot product.
    result = sum(x * y for x, y in zip(a, b))

    # Return the result as JSON.
    return json_response({'dotproduct': result})



@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return json_response(
            {'error': 'Expected a JSON object containing image'}, status=400
        )

    image_string = data.get('image')

    if not isinstance(image_string, str):
        return json_response(
            {'error': 'image must be a Base64 string'},
            status=400
        )

    try:
        # Convert Base64 string back into binary image data
        image_bytes = base64.b64decode(
            image_string,
            validate=True
        )

        # Use same image processing logic as rawimage
        response = image_dimensions(image_bytes)
        return json_response(response)

    except Exception:
        return json_response(
            {'width': 0, 'height': 0},
             status=400
             )


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
