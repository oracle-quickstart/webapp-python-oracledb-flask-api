FROM ghcr.io/oracle/oraclelinux:8

RUN dnf -y module disable python36 && \
    dnf -y module enable python39 && \
    dnf -y install python39 python39-pip python39-setuptools python39-wheel && \
    rm -rf /var/cache/dnf

WORKDIR /myapp
COPY requirements.txt main.py key.pem cert.pem add_employee.html get_employees.html update_employee.html confirm_delete_employee.html crud_options.html search_employee.html employee_not_found.html /myapp
RUN pip3 install -r requirements.txt


CMD ["python3", "./main.py"]
