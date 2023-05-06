FROM python:3.6.9-stretch

# ---------------------------------------------------------------------------------------------------------------------
# BigFISH installation
# 
RUN python3 -m venv /opt/bigfish_env
RUN /opt/venv/bin/activate && pip install big-fish==0.6.2


# ---------------------------------------------------------------------------------------------------------------------
# Install Cytomine python client (annotation exporter, compute metrics, helpers,...)
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd /Cytomine-python-client && git checkout v2.7.3 && pip install . && \
    rm -r /Cytomine-python-client
    
# ---------------------------------------------------------------------------------------------------------------------
# Install Neubias-W5-Utilities (annotation exporter, compute metrics, helpers,...)    
# It will get DiademMetric.jar and JSAP-2.1.jar files to compute DIADEM metric

RUN git clone https://github.com/Neubias-WG5/biaflows-utilities.git && \
    cd /biaflows-utilities/ && git checkout tags/v0.9.1 && pip install .

# install utilities binaries
RUN chmod +x /biaflows-utilities/bin/*
RUN cp /biaflows-utilities/bin/* /usr/bin/

# cleaning
RUN rm -r /biaflows-utilities   


# ---------------------------------------------------------------------------------------------------------------------
# Add script
ADD detect_spots.py /app/script.py
ADD wrapper.py /app/wrapper.py

# for running the wrapper locally
ADD descriptor.json /app/descriptor.json

ENTRYPOINT ["python", "/app/wrapper.py"]


