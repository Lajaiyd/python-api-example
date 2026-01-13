from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

import book_review  # Ensure book_review.py is in the same directory or properly installed

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

br = book_review.BookReview()

class PostReview(Resource):

    def post(self):
        """
        Creates a new book review record in the database.
        Inputs MUST be provided in the POST request body as JSON.
        ---
        tags:
          - Book Reviews
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: BookReview
              type: object
              required:
                - book
                - rating
              properties:
                book:
                  type: string
                  description: The name of the book
                rating:
                  type: number
                  format: float
                  description: Rating of the book (1–10)
                notes:
                  type: string
                  description: Optional notes about the book
        responses:
          201:
            description: Review created successfully
          400:
            description: Invalid or missing input
        """

        if not request.is_json:
            return {"error": "Request body must be JSON"}, 400

        data = request.get_json() or {}

        book = data.get("book")
        rating = data.get("rating")
        notes = data.get("notes")

        if not isinstance(book, str) or not book.strip():
            return {"error": "'book' is required and must be a string"}, 400

        if not isinstance(rating, (int, float)) or not (1 <= float(rating) <= 10):
            return {"error": "'rating' must be a number between 1 and 10"}, 400

        if notes is not None and not isinstance(notes, str):
            return {"error": "'notes' must be a string if provided"}, 400

        fields = {
            "Book": book.strip(),
            "Rating": float(rating),
        }

        if isinstance(notes, str) and notes.strip():
            fields["Notes"] = notes.strip()

        try:
            record = br.table.create(fields)
        except Exception as e:
            return {"error": "Failed to create review", "details": str(e)}, 500

        return {"created": True, "record": record}, 201


api.add_resource(PostReview, "/post-review")


class AllReviews(Resource):

    def get(self):
        """
        Retrieves a list of book review dictionaries.
        Optional query params:
        - sort: 'asc' or 'desc' (sorts by Rating)
        - max_records: int (limits number of records returned)
        ---
        tags:
        - Book Reviews
        parameters:
            - name: sort
              in: query
              type: string
              required: false
              enum: [asc, desc]
              description: Sort by Rating ascending or descending

            - name: max_records
              in: query
              type: integer
              required: false
              description: Maximum number of records to return

        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            book_title:
                                type: string
                                description: The book title
                            book_rating:
                                type: number
                                description: The book rating
                            book_notes:
                                type: string
                                description: The book review
        """
        sort = request.args.get("sort")  # asc | desc | None
        max_records = request.args.get("max_records", type=int)

        # Build pyairtable "sort" as list[str]
        sort_fields = None
        if sort == "asc":
            sort_fields = ["Rating"]
        elif sort == "desc":
            sort_fields = ["-Rating"]
        elif sort is not None:
            return jsonify({"error": "sort must be 'asc', 'desc', or omitted"}), 400

        kwargs = {}
        if sort_fields is not None:
            kwargs["sort"] = sort_fields
        if max_records is not None:
            if max_records <= 0:
                return jsonify({"error": "max_records must be a positive integer"}), 400
            kwargs["max_records"] = max_records

        records = br.table.all(**kwargs) if kwargs else br.table.all()
        return jsonify({"reviews": records})

api.add_resource(AllReviews, "/all-reviews")


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
    