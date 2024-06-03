from flask import Flask, request, jsonify
from app.document_processor import DocumentProcessor
from app.clustering_model import ClusteringModel
from app.query_handler import QueryHandler
from app.translation_service import TranslationService
import os
from flask_cors import CORS

# Initialize models and processor
antique_base_path = "./antique"
wikir_base_path = "./wikir"

antique_processor = DocumentProcessor(antique_base_path)
wikir_processor = DocumentProcessor(wikir_base_path)

antique_loaded_vectorizer, antique_loaded_tfidf_matrix, antique_loaded_document_names, antique_kmeans, antique_processed_docs_dict, antique_preprocessed_corpus, antique_document_texts, antique_Word2VecModel, antique_document_vectors = antique_processor.process_documents("collection.tsv",False)
wikir_loaded_vectorizer, wikir_loaded_tfidf_matrix, wikir_loaded_document_names, wikir_kmeans, wikir_processed_docs_dict, wikir_preprocessed_corpus, wikir_document_texts, wikir_Word2VecModel, wikir_document_vectors = wikir_processor.process_documents("collection.csv",False)

# Ensure processor.documents is not None
antique_processor.documents = antique_processor.load_documents(os.path.join(antique_base_path,  "collection.tsv"))
wikir_processor.documents = wikir_processor.load_documents(os.path.join(wikir_base_path, "collection.csv"))

antique_clustering_model = ClusteringModel(antique_loaded_vectorizer, antique_kmeans)
wikir_clustering_model = ClusteringModel(wikir_loaded_vectorizer, wikir_kmeans)

antique_query_handler = QueryHandler(antique_processor, antique_loaded_vectorizer, antique_loaded_tfidf_matrix, antique_loaded_document_names, antique_processor.documents, antique_Word2VecModel, antique_document_vectors)
wikir_query_handler = QueryHandler(wikir_processor, wikir_loaded_vectorizer, wikir_loaded_tfidf_matrix, wikir_loaded_document_names, wikir_processor.documents, wikir_Word2VecModel, wikir_document_vectors)

translator = TranslationService()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# API endpoints
@app.route("/cluster-plot", methods=["POST"])
def plot_cluster():
    data_name = request.args.get('data', default='antique')
    clustering_model.plot_clusters(loaded_tfidf_matrix, kmeans.labels_.tolist(), method='pca')
    return jsonify({'message': 'plotted'}), 200

@app.route('/query_without_clustering', methods=['POST'])
def query_without_clustering():
    data_name = request.args.get('data', default='antique')
    query_text = request.json.get('query')
    query_text = translator.detect_and_translate(query_text)
    top_n = request.json.get('top_n', 10)
    
    if(data_name=='antique'):
        top_matching_documents, top_matches_scores = antique_query_handler.match_query_with_ranking(query_text, top_n)
    if(data_name=='wikir'):
        top_matching_documents, top_matches_scores = wikir_query_handler.match_query_with_ranking(query_text, top_n)
    return jsonify({'top_matching_documents': top_matching_documents, 'top_matches_scores': top_matches_scores}), 200

@app.route('/query_with_clustering', methods=['POST'])
def query_with_clustering():
    data_name = request.args.get('data', default='antique')
    query_text = request.json.get('query')
    query_text = translator.detect_and_translate(query_text)
    top_n = request.json.get('top_n', 10)
    if(data_name=='antique'):
        top_matching_documents, top_matches_scores = antique_query_handler.match_query_with_ranking_and_clustering(query_text, antique_clustering_model, top_n)
    if(data_name=='wikir'):
        top_matching_documents, top_matches_scores = wikir_query_handler.match_query_with_ranking_and_clustering(query_text, wikir_clustering_model, top_n)
    return jsonify({'top_matching_documents': top_matching_documents, 'top_matches_scores': top_matches_scores}), 200

@app.route('/suggest', methods=['POST'])
def suggest():
    data_name = request.args.get('data', default='antique')

    query_text = request.json.get('query')
    query_text = translator.detect_and_translate(query_text)
    if(data_name=='antique'):
        suggestions = antique_query_handler.generate_query_suggestions(query_text, antique_clustering_model, antique_preprocessed_corpus)
    if(data_name=='wikir'):
        suggestions = wikir_query_handler.generate_query_suggestions(query_text, wikir_clustering_model, wikir_preprocessed_corpus)
    return jsonify({'suggestions': suggestions}), 200

if __name__ == '__main__':
    app.run(debug=True)
