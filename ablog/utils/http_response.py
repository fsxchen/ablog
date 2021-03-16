from flask import jsonify


def make_response(data, code=200):
    """

    :type code: object
    """
    if code > 199 and code < 300:
        return jsonify({
            "code": 20000,
            "data": data
        })

    return jsonify({
        "code": "40000",
        "data": data
    })
