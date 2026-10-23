# Study Notes: Grounding and RAG Applications

These are student study notes written in our own words, based on Chapter 4 "Grounding and RAG Applications" of the Development of AI Applications course (https://mazarbaloch.github.io/dev-ai-course/docs/chapters/04-grounding-and-rag). They are used as the fixed reference document for the StudyBuddy AI evaluation.

## 1. The information gap

A language model only knows what was in its training data and what is sent in the current request. General facts may be covered by training, but private, recent or course-specific details usually are not. For example, if a student asks which dataset a workshop uses and the answer is only written in the course guide, the model cannot know it unless the relevant passage is supplied. Using a bigger or better model does not solve this, because the missing information is in a document, not in the model.

Grounding means tying an answer to evidence that is supplied to the model, so that the answer can be checked against that evidence.

## 2. Simpler options before RAG

RAG is not always necessary. If the document is short, the simplest approach is direct context: put the whole document text into the request. If the question asks for a known field, such as the room number for a course code, a normal database lookup is enough.

Retrieval becomes worthwhile when the collection of documents is too large to fit in one request, when different questions need different documents, or when the information changes independently of the model. Retrieval also has costs: the sources must be prepared, an index must be maintained, and the team must check that search actually finds the right evidence.

## 3. What RAG is

RAG stands for retrieval-augmented generation. It works in two stages. First the application retrieves candidate passages that are related to the question. Then it sends those passages to the model together with the question and instructions for answering. The idea was introduced by Lewis et al. in the original RAG paper.

Adding documents to a RAG system is different from training a model. Adding documents changes the searchable collection, while training changes the learned parameters of the model. This means new course material can be used immediately without retraining anything.

## 4. Semantic search and embeddings

An embedding is a numeric vector that represents a piece of text. Texts with related meaning are placed near each other. For example, the question "What should I bring?" should match the passage "Bring a laptop with Python installed to the workshop", even though the two sentences share few words. A passage about the history of the workshop has the same topic but does not help answer the question.

The course example uses the all-MiniLM-L6-v2 model from Sentence Transformers. It produces embeddings with 384 dimensions and is designed for sentences and short paragraphs. Its default input limit is 256 word pieces, so longer text is cut off.

## 5. Similarity and ranking

Cosine similarity compares the direction of two vectors. The Chroma vector store reports cosine distance instead, which is defined as one minus cosine similarity. A smaller distance therefore means a closer match.

Similarity is only a ranking signal. It does not prove that a passage is true or that it contains the answer. If a student asks about the cafeteria menu using workshop notes, the search still returns the nearest passages, even though none of them is relevant. During development the retrieved passages and their distances should stay visible, and any cut-off value should be chosen later using both answerable and unanswerable test questions.

## 6. Ingestion: preparing the documents

Ingestion is the preparation pipeline that runs before questions arrive. Its steps are: extract the text, identify the source of each piece, divide the text into chunks, create embeddings, and store the records. Later runs of ingestion handle updated documents.

Extracted text is not the same as the original file. PDF files can contain columns, tables, repeated headers or images, and extraction can change the reading order or drop content. Scanned documents need OCR before any text can be extracted. If a table is broken during extraction, retrieval may succeed while the answer is built on damaged evidence, so extracted passages should be compared with the original before blaming the model.

## 7. Choosing chunk boundaries

A chunk is a piece of text that can be retrieved on its own. Short chunks isolate single facts, but they can lose the heading or a condition that gives the fact its meaning. Long chunks keep more context, but they add noise both to search and to the generated answer.

A fixed window groups a set number of words or tokens. Overlap means that neighbouring windows share some text, for example 80-word windows with 15 shared words; overlap protects context at the borders but duplicates text. Structure-aware chunking splits on paragraphs, headings, sentences or sections instead. A typical risk: the sentence "Submit by Friday" may end up in a different chunk from "This applies only to the project resubmission", and the condition is lost. Chunking methods should be compared by retrieval and answer quality, not by the number of chunks.

## 8. Keeping source information

Every chunk needs a unique identifier and a way back to its source. Useful metadata includes the document identity, title, course, revision, and page or section. A page number alone is not unique, because two different documents can both have a page 1. One option is to combine the source location with a content hash, which also shows when the text has changed.

## 9. Evaluating a RAG application

A RAG application can fail in two different places. Retrieval can fail to find the right passage, or the model can receive the right passage but use it incorrectly. These two parts should be assessed separately. A good test set contains answerable questions, whose answers are in the documents, and unanswerable questions, where the correct behaviour is to say that the documents do not contain the answer.
