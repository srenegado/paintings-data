FROM python

RUN mkdir -p /home/paintings-data

WORKDIR /home/paintings-data

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /pipelines .
COPY /data .
COPY makefile .

CMD ["make", "staging"]