FROM python:2.7-alpine

# Install Python dependencies
RUN apk add --no-cache --virtual=build_dependencies musl-dev gcc python-dev make cmake g++ gfortran && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip install numpy && \
    pip install pandas==0.22.0 && \
    pip install openrefine-client && \
    apk del build_dependencies && \
    apk add --no-cache libstdc++ bash vim curl && \
    rm -rf /var/cache/apk/*

# Change docker WORKDIR (shall be mounted by user)
WORKDIR /app

# Make openrefine-client executable
RUN chmod +x /usr/local/lib/python2.7/site-packages/google/refine/__main__.py
RUN cp /usr/local/lib/python2.7/site-packages/google/refine/__main__.py /usr/local/lib/python2.7/site-packages/google/refine/openrefine
ENV PATH="${PATH}:/usr/local/lib/python2.7/site-packages/google/refine"