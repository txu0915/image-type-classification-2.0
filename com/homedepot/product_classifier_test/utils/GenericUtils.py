from datetime import datetime, timedelta

from pytz import timezone


class GenericUtils:

    @staticmethod
    def get_date(days_to_subtract):
        time_zone = timezone('US/Eastern')
        date_format = '%Y-%m-%d'
        date_in_utc = (datetime.now(time_zone) - timedelta(days=days_to_subtract)).strftime(date_format)
        return date_in_utc

    @staticmethod
    def bucket_path_details(outputpath):
        details = outputpath.split('/', 3)
        return details

    @staticmethod
    def generate_image_classification_json(oms_id, label, category_id, image_available, image_url, predictions):
        json_data = {'oms_id': oms_id, 'label': label, 'category': category_id, 'image_available': image_available,
                     'image_url': image_url, 'predictions': predictions}
        return json_data
