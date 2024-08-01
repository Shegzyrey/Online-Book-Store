from flask import Blueprint, request, jsonify
from services.openai_service import get_book_summary
from config import Config

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
def summarize_book():
    book_data = request.json
    book_text = book_data['text']
    summary = get_book_summary(book_text, Config.OPENAI_API_KEY)
    return jsonify({'summary': summary})
