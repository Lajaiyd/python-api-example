from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return {"text": text.upper()}, 200
    

class ProcessText(Resource):

    def get(self):
        """
        This method responds to the GET request for this endpoint and processes text
        based on duplication and capitalization rules.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be processed

            - name: duplication_factor
              in: query
              type: integer
              required: false
              default: 1
              description: Number of times to repeat the text on new lines

            - name: capitalization
              in: query
              type: string
              required: false
              enum: [UPPER, LOWER, None]
              default: None
              description: Capitalization rule to apply to the text
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            result:
                                type: string
                                description: The processed text
        """
        text = request.args.get("text")
        duplication_factor = request.args.get("duplication_factor", default=1, type=int)
        capitalization = request.args.get("capitalization", default=None)

        # Apply capitalization
        if capitalization == "UPPER":
            text = text.upper()
        elif capitalization == "LOWER":
            text = text.lower()

        # Duplicate text on new lines
        result = "\n".join([text] * max(duplication_factor, 1))

        return jsonify({"result": result})

api.add_resource(ProcessText, "/process-text")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)
    