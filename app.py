from flask import Flask, jsonify, request
from pydantic import BaseModel, Field, ValidationError
from flask_pydantic import validate
from models import MongoDB
from config import Config
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db = MongoDB(app.config['MONGO_URI'])

class FAQModel(BaseModel):
    question: str = Field(..., max_length=255)
    answer: str = Field(..., max_length=1000)

@app.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = db.get_all_faqs()
    return jsonify(faqs), 200

@app.route('/faqs/<string:faq_id>', methods=['GET'])
def get_faq(faq_id):
    faq = db.get_faq_by_id(faq_id)
    if faq:
        return jsonify(faq), 200
    return jsonify({"error": "FAQ not found"}), 404

@app.route('/faqs', methods=['POST'])
@validate()
def create_faq(body: FAQModel):
    faq = {"question": body.question, "answer": body.answer}
    db.create_faq(faq)
    return jsonify({"message": "FAQ created successfully"}), 201

@app.route('/faqs/<string:faq_id>', methods=['PUT'])
@validate()
def update_faq(faq_id, body: FAQModel):
    updated_data = {"question": body.question, "answer": body.answer}
    result = db.update_faq(faq_id, updated_data)
    if result.matched_count == 0:
        return jsonify({"error": "FAQ not found"}), 404
    return jsonify({"message": "FAQ updated successfully"}), 200

@app.route('/faqs/<string:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    result = db.delete_faq(faq_id)
    if result.deleted_count == 0:
        return jsonify({"error": "FAQ not found"}), 404
    return jsonify({"message": "FAQ deleted successfully"}), 200

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": e.errors()}), 400

if __name__ == '__main__':
    app.run(debug=True)
