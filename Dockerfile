FROM sagemath/sagemath
USER root
RUN apt-get update && apt-get install -y python3-pip
USER sage
RUN pip3 install --user pycryptodome
