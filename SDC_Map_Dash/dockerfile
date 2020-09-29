FROM python:3

RUN if ! which wget; then if which apt-get; then apt-get update && apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/* ; fi ; fi

# Add the DOIRootCA to enable sourcing remote packages on the USGS network.
RUN wget -nv -O /etc/ssl/certs/DOIRootaCA.crt \
      https://repo.snafu.cr.usgs.gov/ssl/DOIRootCA.crt \
      && cat /etc/ssl/certs/DOIRootaCA.crt >> /etc/ssl/certs/ca-certificates.crt

RUN echo "[global]\ncert = /etc/ssl/certs/ca-certificates.crt" > /etc/pip.conf
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt


RUN pip install dash gunicorn requests pandas numpy plotly_express sciencebasepy dash-bootstrap-components

COPY . /src
WORKDIR /src/app/
EXPOSE 5555

CMD exec gunicorn app:server -b 0.0.0.0:5555
