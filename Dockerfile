FROM ghcr.io/oracle/oraclelinux:8

RUN yum install -y oracle-release-el8 \
    && yum-config-manager --enable ol8_oracle_instantclient \
    && yum install -y oracle-instantclient19.10-basic


RUN dnf -y module disable python36 && \
    dnf -y module enable python39 && \
    dnf -y install python39 python39-pip python39-setuptools python39-wheel && \
    rm -rf /var/cache/dnf

RUN yum install -y postgresql-devel

RUN yum install -y gcc \
    && yum install -y libaio-devel

ADD requirements.txt .
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt


# Set the environment variable for LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH /usr/lib/oracle/19.10/client64/lib/

ADD main.py .

ADD key.pem .

ADD cert.pem .

ADD add_employee.html .

ADD get_employees.html .

ADD update_employee.html .

ADD confirm_delete_employee.html .

ADD crud_options.html .

ADD search_employee.html .

ADD employee_not_found.html .

CMD ["python3", "./main.py"]
