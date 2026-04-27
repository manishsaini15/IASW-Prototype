import os
import shutil
from datetime import datetime
from config import ARCHIVE_FOLDER

def archive_document(file_path):
    """
    Mock FileNet archival: copy uploaded file into archived_docs folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.basename(file_path)

    filenet_ref_id = f"FN-{timestamp}"
    archived_filename = f"{filenet_ref_id}-{filename}"

    destination = os.path.join(ARCHIVE_FOLDER, archived_filename)

    shutil.copy(file_path, destination)

    return filenet_ref_id, destination