import os
import re
import sys
import base64
import shutil
import time
import threading

#os.environ['OPENAI_API_KEY'] = "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"
os.environ['OPENAI_API_KEY'] = "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"


from langchain.llms import OpenAI
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext
from llama_index.readers.file.base import (
    DEFAULT_FILE_EXTRACTOR, 
    ImageParser,
)
from llama_index.indices.query.query_transform.base import (
    ImageOutputQueryTransform,
)
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
image_parser = ImageParser(keep_image=True, parse_text=True)
file_extractor = DEFAULT_FILE_EXTRACTOR
file_extractor.update(
{
    ".jpg": image_parser,
    ".png": image_parser,
    ".jpeg": image_parser,
})
source_folder = 'images'
indexed_folder = 'NUS_ISS_chatbot/data/indexed'
index_filepath = './text_token_llama.json'
# add filename as metadata for all documents
filename_fn = lambda filename: {'file_name': filename}
image_reader = SimpleDirectoryReader(
    input_dir=source_folder,
    file_extractor=file_extractor, 
    file_metadata=filename_fn,
    required_exts=['.jpg']
)
def move_indexed_files():
    # fetch all files
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".jpg") :
            # construct full file path
            source = source_folder + '/' + file_name
            destination = indexed_folder + '/' + file_name
            # move only files
            if os.path.isfile(source):
                shutil.move(source, destination)
                #print('Moved:', file_name)

def print_dots(stop_event):
    while not stop_event.is_set():
        print(".", end="", flush=True)
        time.sleep(1)

def tagImages_llama():
    import time
    start_time = time.time()
    print ("\nStep 3: Tagging of images according to LlamaIndex")
    stop_event = threading.Event()
    dot_printer = threading.Thread(target=print_dots, args=(stop_event,))
    dot_printer.start()
    image_documents = image_reader.load_data()
    image_index = GPTSimpleVectorIndex.load_from_disk(image_documents)
    for document in image_documents:
        image_index.insert(document) 
    image_index.save_to_disk(index_filepath)
    elapsed_time = time.time() - start_time
    stop_event.set()
    dot_printer.join()
    print (f"Complete Tagging of images according to LlamaIndex, Elapsed time: {elapsed_time:.4f} seconds")

def findSuitableImage_llama(search_string, image_index):
    response = image_index.query(
        search_string,
        query_transform=ImageOutputQueryTransform(width=600)
    )

    x = None
    if response.response:
        x = re.search('<img src="(.+)".+"\d+"', response.response)
    if x:
        image_path = x.group(1).replace("\\","/").replace(source_folder, indexed_folder)
        return image_path
    else:
        return ""
    
def clearAndLoadTextTokensFromFile_llama():
    return GPTSimpleVectorIndex.load_from_disk(index_filepath)
