from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from components.uploader import render_uploader

class DocumentLoaderService:
    def __init__(self):
        """
        Document loading service class is defined for to load documents
        """
    
    def docx_loader(self, resume):
        loader = Docx2txtLoader(resume)
        content = loader.load()

        return content
    
    def pdf_loader(self, resume):
        loader = PyPDFLoader(resume)
        content = loader.load()

        return content


def get_file_loader(resume:str):
    """
    Get file loader based on file extension
    """
    if resume.endswith(".docx"):
        return DocumentLoaderService().docx_loader(resume)
    elif resume.endswith(".pdf"):
        return DocumentLoaderService().pdf_loader(resume)
    else:
        raise ValueError("Unsupported file type")