RELEASE_VERSION="0.0.1"

project=`gcloud config get-value project`

sudo apt-get update
sudo apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
tar -xf Python-3.7.4.tar.xz
cd ./Python-3.7.4
./configure --enable-optimizations
make install
DEBIAN_FRONTEND=noninteractive apt-get upgrade -q -y -u  -o Dpkg::Options::="--force-confdef" --allow-downgrades --allow-remove-essential --allow-change-held-packages --allow-change-held-packages --allow-unauthenticated
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install -y libhdf5-dev
sudo python3.7 /usr/local/bin/pip3 install --upgrade setuptools
sudo python3.7 /usr/local/bin/pip3 install apache-beam[gcp]==2.15.0
sudo python3.7 /usr/local/bin/pip3 install avro==1.9.0
sudo python3.7 /usr/local/bin/pip3 install gcsfs==0.2.3
sudo python3.7 /usr/local/bin/pip3 install google-cloud-storage==1.16.1
sudo python3.7 /usr/local/bin/pip3 install h5py==2.9.0
sudo python3.7 /usr/local/bin/pip3 install imutils==0.5.3
sudo python3.7 /usr/local/bin/pip3 install joblib==0.13.2
sudo python3.7 /usr/local/bin/pip3 install keras==2.2.4
sudo python3.7 /usr/local/bin/pip3 install opencv-contrib-python-headless==4.1.1.26
sudo python3.7 /usr/local/bin/pip3 install pandas==0.25.1
sudo python3.7 /usr/local/bin/pip3 install Pillow==6.1.0
sudo python3.7 /usr/local/bin/pip3 install scikit-image==0.14.5
sudo python3.7 /usr/local/bin/pip3 install scikit-learn==0.20.4
sudo python3.7 /usr/local/bin/pip3 install scipy==1.2.2
sudo python3.7 /usr/local/bin/pip3 install xgboost==0.82

echo "export PYSPARK_PYTHON=python3.7" | tee -a  /etc/profile.d/spark_config.sh  /etc/*bashrc /usr/lib/spark/conf/spark-env.sh
echo "export PYTHONHASHSEED=0" | tee -a /etc/profile.d/spark_config.sh /etc/*bashrc /usr/lib/spark/conf/spark-env.sh
echo "spark.executorEnv.PYTHONHASHSEED=0" >> /etc/spark/conf/spark-defaults.conf


gsutil -m cp gs://$project-artifacts/releases/tensorflow/tensorflow-1.14.0-cp37-cp37m-manylinux1_x86_64.whl /tmp/

sudo python3.7 /usr/local/bin/pip3 install /tmp/tensorflow-1.14.0-cp37-cp37m-manylinux1_x86_64.whl

gsutil cp gs://$project-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/setup-scripts/$RELEASE_VERSION/setup.py /tmp/setup.py

gsutil -m cp -r gs://$project-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/python-scripts/$RELEASE_VERSION/product_image_classifier_2.0-0.0.1.egg /tmp/product_image_classifier_2.0-0.0.1.egg

sudo easy_install-3.7 /tmp/product_image_classifier_2.0-0.0.1.egg

mkdir /tmp/com

cp -r /usr/local/lib/python3.7/site-packages/product_image_classifier_2.0-0.0.1.egg/com/* /tmp/com/