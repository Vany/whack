FROM python
RUN git clone http://github.com/fetchai/ledger-api-py.git
# -b release/v0.4.x
WORKDIR /ledger-api-py
RUN python3 setup.py install
RUN pip3 install -v -v -v --no-cache-dir oef
