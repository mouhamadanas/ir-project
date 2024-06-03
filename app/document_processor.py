import os
import re
import string
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
class DocumentProcessor:
    def __init__(self, base_path, vector_size=500, epochs=35, workers=4):
        self.base_path = base_path
        self.vector_size = vector_size
        self.epochs = epochs
        self.workers = workers
        self.documents = None

    def load_documents(self, file_path, limit=1000):
        documents = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i >= limit:
                    break
                if "antique" in file_path:
                    doc_id, content = line.strip().split('\t')
                elif "wikir" in file_path:
                    doc_id, content = line.strip().split(',')

                documents[doc_id] = content
        self.documents = documents
        return documents

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens]
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [re.sub(r'http\S+', '', word) for word in tokens]
        tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens]
        tokens = [word for word in tokens if word]
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]
        pos_tags = pos_tag(tokens)
        pos_tags = [(word, self.nltk_to_wordnet_pos(pos_tag)) for word, pos_tag in pos_tags]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word, pos=pos) if pos else word for word, pos in pos_tags]
        abbreviations = {"abbr": "abbreviation", "exp": "expansion"}
        tokens = [abbreviations.get(word, word) for word in tokens]
        return tokens

    def nltk_to_wordnet_pos(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def tokenize_text(self, text):
        return word_tokenize(text)

    def process_documents(self,fileName,save_new=True):
        tsv_file_path = os.path.join(self.base_path, fileName)
        vectorizer_path = os.path.join(self.base_path, "clustering", "clustering_vectorizer.pkl")
        kmeans_path = os.path.join(self.base_path, "clustering", "kmeans.pkl")
        tfidf_matrix_path = os.path.join(self.base_path, "tf_idf_matrix", "tfidf_matrix1.pkl")
        document_names_path = os.path.join(self.base_path, "docs_names", "document_names1.pkl")
        processed_docs_path = os.path.join(self.base_path, "processed_docs", "processed_docs.pkl")
        corpus_path = os.path.join(self.base_path, "corpus", "corpus.pkl")
        texts_path = os.path.join(self.base_path, "texts", "texts.pkl")
        Word2Vec_path = os.path.join(self.base_path, "Word2Vec", "Word2Vec.pkl")
        document_vectors_path = os.path.join(self.base_path, "document_vectors", "document_vectors.pkl")

        need_processing = save_new or not all(self.file_exists(path) for path in [
            vectorizer_path, kmeans_path, tfidf_matrix_path, document_names_path, processed_docs_path, corpus_path, texts_path, Word2Vec_path
        ])

        if need_processing:
            document_contents = self.load_documents(tsv_file_path)
            processed_docs_dict = {doc_id: self.preprocess_text(content) for doc_id, content in document_contents.items()}
            preprocessed_corpus = list(processed_docs_dict.values())
            document_texts = [' '.join(tokens) for tokens in preprocessed_corpus]

            tokenized_documents = [self.tokenize_text(d) for d in document_texts]
            Word2VecModel = Word2Vec(tokenized_documents, vector_size=self.vector_size, sg=1, workers=self.workers, epochs=self.epochs)
            self.save_object(Word2VecModel, Word2Vec_path)

            document_vectors = [self.get_embedding_vector(Word2VecModel, doc_tokens) for doc_tokens in tokenized_documents]
            self.save_object(document_vectors, document_vectors_path)

            self.save_object(processed_docs_dict, processed_docs_path)
            self.save_object(preprocessed_corpus, corpus_path)
            self.save_object(document_texts, texts_path)

            kmeans, loaded_vectorizer = self.cluster_documents(document_texts, 4)
            self.save_object(loaded_vectorizer, vectorizer_path)
            self.save_object(kmeans, kmeans_path)

            loaded_tfidf_matrix = loaded_vectorizer.fit_transform(document_texts)
            self.save_object(loaded_tfidf_matrix, tfidf_matrix_path)
            loaded_document_names = list(document_contents.keys())
            self.save_object(loaded_document_names, document_names_path)
        else:
            loaded_vectorizer = self.load_object(vectorizer_path)
            document_vectors = self.load_object(document_vectors_path)
            Word2VecModel = self.load_object(Word2Vec_path)
            loaded_tfidf_matrix = self.load_object(tfidf_matrix_path)
            loaded_document_names = self.load_object(document_names_path)
            kmeans = self.load_object(kmeans_path)
            processed_docs_dict = self.load_object(processed_docs_path)
            preprocessed_corpus = self.load_object(corpus_path)
            document_texts = self.load_object(texts_path)

        return loaded_vectorizer, loaded_tfidf_matrix, loaded_document_names, kmeans, processed_docs_dict, preprocessed_corpus, document_texts, Word2VecModel, document_vectors

    def get_embedding_vector(self, model, doc_tokens):
        embeddings = []
        size = 500
        if len(doc_tokens) < 1:
            return np.zeros(size)
        else:
            for tok in doc_tokens:
                if tok in model.wv:
                    embeddings.append(model.wv[tok])
                else:
                    embeddings.append(np.random.rand(size))
            if embeddings:
                embeddings = np.asarray(embeddings)
                vector = embeddings.mean(axis=0)
            else:
                return np.zeros(size)
        return vector

    def cluster_documents(self, documents, num_clusters=300):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)
        return kmeans, vectorizer

    def save_object(self, obj, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(obj, file)

    def load_object(self, filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def file_exists(self, filename):
        return os.path.exists(filename) and os.path.getsize(filename) > 0
