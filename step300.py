import sys

import configs
from core import pipeline

if __name__ == '__main__':
    configs.setting_logger()
    argv = sys.argv[1:]

    directory_name = argv[0]

    steps = list()
    tokens_path = configs.get_step02_desc_tokens_path(directory_name)
    tokens_header_path = configs.get_step02_desc_tokens_header_path(directory_name)
    caption_quality = configs.get_step03_caption_quality_score_path(directory_name)
    steps.append(['Calculate caption', 'python', 'step300_caption_quality.py',
                  tokens_path, tokens_header_path, caption_quality])

    image_quality = configs.get_step03_image_quality_score_path(directory_name)
    steps.append(['Calculate caption', 'python', 'step301_image_quality.py',
                  tokens_path, tokens_header_path, image_quality])

    collection_path = configs.get_step02_append_collection_path(directory_name)
    collection_header_path = configs.get_step02_append_collection_header_path(directory_name)
    caption_quality_collection = configs.appended_get_step03_caption_quality_collection_path(directory_name)
    caption_quality_collection_header = configs.get_step03_caption_quality_collection_header_path(directory_name)
    steps.append(['Calculate caption', 'python', 'step302_append_caption_quality.py',
                  collection_path, collection_header_path, caption_quality, image_quality, caption_quality_collection,
                  caption_quality_collection_header])

    step03_output_path = configs.get_step03_output_directory_path(directory_name)
    step03_bucket_output_path = configs.get_bucket_step03_output_directory_path(directory_name)
    steps.append(
        ['Update base collection to bucket', 'python', 'step101_upload_base_collection.py',
         step03_output_path, step03_bucket_output_path])

    pipeline.run(steps)
