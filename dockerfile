FROM ubuntu:18.04

LABEL "author"="kissofjudase23@gmail.com" \
      "type"="library"

RUN apt-get -y update && \
    apt-get -y install python3.6 python3-pip && \
    pip3 install --upgrade pip


COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

ARG work_dir
WORKDIR ${work_dir}

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/bin/bash"]
