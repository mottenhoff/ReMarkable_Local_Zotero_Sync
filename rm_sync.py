from pathlib import Path

from rmapy.api import Client as RMClient
from rmapy.folder import Folder
from rmapy.document import Document
from rmapy.document import ZipDocument

from config import config

CONFIG = config()

def check_remarkable_api_connection(Client):
    if not Client.is_auth():
        Client.register_device(CONFIG["Remarkable_auth_code"])
    return Client

def get_files_from_remarkable(rmc):
    try:
        all_items = rmc.get_meta_items()
    except Exception:
        print('Response 401: Renewing token')
        rmc.renew_token()
        all_items = rmc.meta_items()

    folders = [f for f in all_items if isinstance(f, Folder)]
    documents = [f for f in all_items if isinstance(f, Document)]
    return folders, documents


def get_files_from_zotero_storage(path: str):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError('Path does not exists!')

    return [pdf_path for pdf_path in Path(path).rglob('*.pdf')]

def get_folder_object(name: str, folders):
    try:
        return [folder for folder in folders if folder.VissibleName == name][0]
    except Exception:
        print('Folder does not exist.')
        raise

def upload_new_files_to_remarkable(rmc, zotero_pdfs, rm_folders, rm_documents, to_rm_folder):
    documents_in_paper_folder = [document for document in rm_documents if document.Parent == to_rm_folder.ID]
    document_names_in_paper_folder = [document.VissibleName for document in documents_in_paper_folder]
    
    missing_documents = [document for document in zotero_pdfs if document.stem not in document_names_in_paper_folder]
    n_docs = len(missing_documents)
    print('Uploading {} files{:s}'.format(n_docs, '.' if n_docs==0 else ':'))
    for document in missing_documents:
        print('  {}'.format(document.name), end='', flush=True)
        document = ZipDocument(doc=document.absolute().as_posix())
        rmc.upload(document, to=to_rm_folder)
        print('\tDONE')

def remove_files_from_remarkable(rmc, zotero_pdfs, rm_folders, rm_documents, from_rm_folder):
    rm_docs = [docs for docs in rm_documents if docs.Parent == from_rm_folder.ID]
    pdf_names = [pdf.stem for pdf in zotero_pdfs]
    files_to_remove = [file for file in rm_docs if file.VissibleName not in pdf_names]
    
    n_files = len(files_to_remove)
    print('Removing {:d} files{:s}'.format(n_files, '.' if n_files==0 else ':'))
    for file in files_to_remove:
        print('  {}'.format(file.VissibleName), end='')
        rmc.delete(file)
        print('\tDONE')

def sync():
    zotero_path = CONFIG['path_to_local_zotero_storage'] # Local storage
    remarkable_folder_name = CONFIG["reMarkable_folder_name"]
    try:
        rmc = RMClient()
        rmc = check_remarkable_api_connection(rmc)

        zotero_pdfs = get_files_from_zotero_storage(zotero_path)
        rm_folders, rm_documents = get_files_from_remarkable(rmc)
        
        # Mirror Zotero local storage with ReMarkable 2 
        upload_new_files_to_remarkable(rmc, zotero_pdfs, rm_folders, rm_documents, 
                                      to_rm_folder=get_folder_object(remarkable_folder_name, rm_folders))
        remove_files_from_remarkable(rmc, zotero_pdfs, rm_folders, rm_documents,
                                     from_rm_folder=get_folder_object(remarkable_folder_name, rm_folders))
    except Exception:
        return

if __name__ == '__main__':
    sync()


