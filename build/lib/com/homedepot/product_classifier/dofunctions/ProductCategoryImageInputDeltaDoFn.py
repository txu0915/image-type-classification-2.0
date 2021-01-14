import apache_beam as beam


class ProductCategoryImageInputDeltaDoFn(beam.DoFn):

    def process(self, element):
        (oms_id, dtls) = element
        current_product_dtls_iter = dtls['current_product_dtls_tag']
        previous_product_dtls_iter = dtls['previous_product_dtls_tag']

        if current_product_dtls_iter and previous_product_dtls_iter:
            current_product_dtls_tuple = current_product_dtls_iter[0]
            previous_product_dtls_tuple = previous_product_dtls_iter[0]
            i = 0
            j = 0
            current_image_url_list = []
            current_category_id_list = []
            previous_image_url_list = []
            previous_category_id_list = []
            for currentProductCategoryImageDtlsVO in current_product_dtls_tuple:
                current_category_id = currentProductCategoryImageDtlsVO.category_id
                current_image_dtls_list = currentProductCategoryImageDtlsVO.image_dtls_list
                current_category_id_list.append(current_category_id)
                if i == 0:
                    for current_image_details_dict in current_image_dtls_list:
                        image_url = current_image_details_dict['image_url']
                        current_image_url_list.append(image_url)
                i = i + 1

            for previousProductCategoryImageDtlsVO in previous_product_dtls_tuple:
                previous_category_id = previousProductCategoryImageDtlsVO.category_id
                previous_image_dtls_list = previousProductCategoryImageDtlsVO.image_dtls_list
                previous_category_id_list.append(previous_category_id)
                if j == 0:
                    for previous_image_details_dict in previous_image_dtls_list:
                        image_url = previous_image_details_dict['image_url']
                        previous_image_url_list.append(image_url)
                    j = j + 1

            if not sorted(current_image_url_list) == sorted(previous_image_url_list):
                return [(oms_id, current_product_dtls_tuple)]

            elif not sorted(current_category_id_list) == sorted(previous_category_id_list):
                return [(oms_id, current_product_dtls_tuple)]

        elif current_product_dtls_iter and not previous_product_dtls_iter:
            current_product_dtls_tuple = current_product_dtls_iter[0]
            return [(oms_id, current_product_dtls_tuple)]
        else:
            pass
