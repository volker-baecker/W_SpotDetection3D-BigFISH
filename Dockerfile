FROM python:3.6.9-stretch


# ---------------------------------------------------------------------------------------------------------------------
# Install Cytomine python client
RUN pip install --upgrade pip setuptools wheel
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd /Cytomine-python-client && git checkout tags/v2.3.0.poc.1 && pip install . && \
    rm -r /Cytomine-python-client

# ---------------------------------------------------------------------------------------------------------------------
# BigFISH installation
# 
RUN pip install big-fish==0.6.2

# ---------------------------------------------------------------------------------------------------------------------
# Install Neubias-W5-Utilities (annotation exporter, compute metrics, helpers,...)
RUN git clone https://github.com/Neubias-WG5/neubiaswg5-utilities.git
RUN cd /neubiaswg5-utilities/ && git checkout tags/v0.8.8 && pip install .

# install utilities binaries
RUN chmod +x /neubiaswg5-utilities/bin/*
RUN cp /neubiaswg5-utilities/bin/* /usr/bin/

# cleaning
RUN rm -r /neubiaswg5-utilities

# ---------------------------------------------------------------------------------------------------------------------
# Add script
ADD detect_spots.py /app/script.py
ADD wrapper.py /app/wrapper.py

# for running the wrapper locally
ADD descriptor.json /app/descriptor.json

ENTRYPOINT ["python", "/app/wrapper.py"]


