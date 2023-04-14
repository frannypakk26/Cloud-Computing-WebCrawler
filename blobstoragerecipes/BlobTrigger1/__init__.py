import logging

import azure.functions as func

import io
from wordcloud import WerdCloud


def main(myblob: func.InputStream, inputBlob: bytes, outputBlob: func.Out[bytes]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    
    #reading the input blob
    logging.info("Getting input file as a list")
    recipes_list = inputBlob.replace("\n", " ") #changes the new lines to a space
    
    #carriage return
    #logging.info("Getting input file as a single string")
    #recipes_text = recipes_list.replace('\r', '')
    #logging.info(recipes_text)
    
    logging.info("Generating wordcloud of text from input file")
    word_cloud_text = WordCloud().generate(recipes_list)
    
    wordcloud_image = word_cloud_text.to_image()
    
    #converting image to bytes
    image_byte_array = io.Bytes()
    wordcloud_image.save(image_byte_array, format = 'png')
    logging.info(type(image_byte_array))
    
    #saving wordcloud in output file
    logging.info("Saving wordcloud image into the output folder")
    outputBlob.set(image_byte_array.getvalue())
    logging.info("Wordcloud image is saved in output folder")
    