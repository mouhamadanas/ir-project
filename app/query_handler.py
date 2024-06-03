import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from app.document_processor import DocumentProcessor

nlp = spacy.load("en_core_web_sm")

class QueryHandler:
    def __init__(self, document_processor, vectorizer, tfidf_matrix, document_names, document_contents, word2vec_model, document_vectors):
        self.document_processor = document_processor
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.document_names = document_names
        self.document_contents = document_contents
        self.word2vec_model = word2vec_model
        self.document_vectors = document_vectors

    def match_query_with_ranking(self, query_text, top_n=100):
        preprocessed_query = self.document_processor.preprocess_text(query_text)
        query_vector = self.document_processor.get_embedding_vector(self.word2vec_model, preprocessed_query)
        similarities = cosine_similarity([query_vector], self.document_vectors)[0]
        ranked_indices = np.argsort(similarities.flatten())[::-1]
        top_matches_indices = ranked_indices[:top_n]
        top_matches_scores = similarities.flatten()[top_matches_indices]
        top_matching_documents = [self.document_contents[self.document_names[i]] for i in top_matches_indices]
        return top_matching_documents, top_matches_scores.tolist()

    def match_query_with_ranking_and_clustering(self, query_text, clustering_model, top_n=100):
        preprocessed_query = self.document_processor.preprocess_text(query_text)
        query_vector = self.vectorizer.transform([' '.join(preprocessed_query)])
        cluster = clustering_model.predict_cluster(' '.join(preprocessed_query))
        cluster_indices = np.where(clustering_model.kmeans.labels_ == cluster[0])[0]
        cluster_documents = self.tfidf_matrix[cluster_indices]
        cluster_document_names = [self.document_names[i] for i in cluster_indices]

        

        similarities = cosine_similarity(query_vector, cluster_documents)[0]
        ranked_indices = np.argsort(similarities)[::-1]
        top_matches_indices = ranked_indices[:top_n]

        

        top_matches_indices = [i for i in top_matches_indices if i < len(cluster_document_names)]

        

    # Further debugging for index and names
        for i in top_matches_indices:
            if i >= len(cluster_document_names):
                print(f"Invalid index found: {i}")

        top_matches_scores = similarities[top_matches_indices]

    # Handle case where document name is not found in document_contents
        top_matching_documents = []
        for i in top_matches_indices:
            doc_name = cluster_document_names[i]
            if doc_name in self.document_contents:
                top_matching_documents.append(self.document_contents[doc_name])
            else:
                print(f"Document not found for name: {doc_name}")
                # top_matching_documents.append("Document not found")

        return top_matching_documents, top_matches_scores.tolist()

   
    def generate_query_suggestions(self, query_text, clustering_model, preprocessed_corpus, top_n=5):
        preprocessed_query = self.document_processor.preprocess_text(query_text)
        query_vector = self.vectorizer.transform([' '.join(preprocessed_query)])
        query_cluster = clustering_model.kmeans.predict(query_vector)[0]
        cluster_indices = [i for i, cluster in enumerate(clustering_model.kmeans.labels_) if cluster == query_cluster]
        cluster_docs = [preprocessed_corpus[i] for i in cluster_indices]
        sentences = []
        for doc in cluster_docs:
            processed_doc = nlp(' '.join(doc))
            for sent in processed_doc.sents:
                if len(sent.text.strip()) < 40:
                    sentences.append(sent.text.strip())

        if not sentences:
            return []

        sentence_vectors = self.vectorizer.transform(sentences)
        similarities = cosine_similarity(query_vector, sentence_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_n]
        suggestions = [sentences[i] for i in top_indices]
        return suggestions
