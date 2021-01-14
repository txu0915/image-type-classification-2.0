import apache_beam as beam

from com.homedepot.product_classifier.pojo.ProductCategoryImageDtlsVO import ProductCategoryImageDtlsVO


class ProductCategoryImageTransformDoFn(beam.DoFn):
    ## Merging [(OMSID,filtered_image_list)] info with [(oms_id, category_id)] info
    def process(self, element):
        (oms_id, details) = element
        product_category_dtls_iter = details['product_category_dtls_tag']
        product_image_dtls_iter = details['product_image_dtls_tag']
        category_image_dtls_list = []
        if product_category_dtls_iter and product_image_dtls_iter:
            for category_id in product_category_dtls_iter:
                if category_id:
                    for product_image_list in product_image_dtls_iter:
                        if product_image_list:
                            category_image_dtls_list.append(ProductCategoryImageDtlsVO(category_id, product_image_list));
        if category_image_dtls_list:
            return [(oms_id, category_image_dtls_list)]

        ## returning a info that contains OMSID and all its relavent categories and all images it has...
