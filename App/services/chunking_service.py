from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:


    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )


    def split_document(self, text):

        chunks = self.text_splitter.split_text(
            text
        )

        return chunks