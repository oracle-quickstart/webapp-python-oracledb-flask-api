-- Employees Table
CREATE TABLE employees (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    email VARCHAR2(255) NOT NULL,
    department VARCHAR2(255) NOT NULL
);

-- Insert 50 records in 'employees' table
INSERT INTO employees (name, email, department) VALUES ('John Doe', 'john.doe@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Jane Smith', 'jane.smith@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Bob Johnson', 'bob.johnson@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Mary Brown', 'mary.brown@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('David Lee', 'david.lee@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Sarah Green', 'sarah.green@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Mike Davis', 'mike.davis@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Karen Wilson', 'karen.wilson@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Tom Johnson', 'tom.johnson@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Lisa Chen', 'lisa.chen@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('David Davis', 'david.davis@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Michelle Rodriguez', 'michelle.rodriguez@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Christopher Smith', 'christopher.smith@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Samantha Brown', 'samantha.brown@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Charles Kim', 'charles.kim@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Alexandra Taylor', 'alexandra.taylor@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Richard Wilson', 'richard.wilson@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Jennifer Lee', 'jennifer.lee@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Matthew Jones', 'matthew.jones@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Ava Chen', 'ava.chen@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('William Davis', 'william.davis@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Natalie Nguyen', 'natalie.nguyen@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Joseph Garcia', 'joseph.garcia@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Rachel Martin', 'rachel.martin@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Christian Kim', 'christian.kim@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Hannah Rodriguez', 'hannah.rodriguez@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Anthony Johnson', 'anthony.johnson@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Sophia Wilson', 'sophia.wilson@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Ethan Chen', 'ethan.chen@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Madison Smith', 'madison.smith@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Oliver Davis', 'oliver.davis@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Grace Nguyen', 'grace.nguyen@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Daniel Garcia', 'daniel.garcia@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Isabella Martin', 'isabella.martin@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Mia Kim', 'mia.kim@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Lucas Rodriguez', 'lucas.rodriguez@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Victoria Johnson', 'victoria.johnson@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('David Wilson', 'david.wilson@example.com','Engineering');
INSERT INTO employees (name, email, department) VALUES ('Steven Nguyen', 'steven.nguyen@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Amy Kim', 'amy.kim@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Anna Martinez', 'anna.martinez@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Kevin Kim', 'kevin.kim@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Catherine Davis', 'catherine.davis@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Robert Nguyen', 'robert.nguyen@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Karen Clark', 'karen.clark@example.com', 'Engineering');
INSERT INTO employees (name, email, department) VALUES ('Mike Wilson', 'mike.wilson@example.com', 'Sales');
INSERT INTO employees (name, email, department) VALUES ('Rachel Lee', 'rachel.lee@example.com', 'Marketing');
INSERT INTO employees (name, email, department) VALUES ('Thomas Johnson', 'thomas.johnson@example.com', 'Finance');
INSERT INTO employees (name, email, department) VALUES ('Emily White', 'emily.white@example.com', 'Human Resources');
INSERT INTO employees (name, email, department) VALUES ('Brian Brown', 'brian.brown@example.com', 'Engineering');
commit;

-- Procedure to Generate Sample Data
CREATE OR REPLACE PROCEDURE add_employees (
    n IN NUMBER
)
AS
    departments employees.department%TYPE := 'Sales,Marketing,Finance,Human Resources,Engineering';
BEGIN
    FOR i IN 1..n LOOP
        INSERT INTO employees (name, email, department)
        VALUES ('Employee ' || i, 'employee' || i || '@example.com', REGEXP_SUBSTR(departments,'[^,]+',1,ROUND(DBMS_RANDOM.VALUE(1,5))));
    END LOOP;
    COMMIT;
END;
/

-- Generate Sample Employee Data
BEGIN
    add_employees(50);
END;
/

-- Employees Salary Table
CREATE TABLE employees_salary (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id NUMBER NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    bonus FLOAT NOT NULL
    );

-- Procedure to Generate Sample Data
CREATE OR REPLACE PROCEDURE generate_employees_salary(n IN NUMBER) AS
BEGIN
  FOR i IN 1..n LOOP
    INSERT INTO employees_salary (employee_id, salary, start_date, end_date, bonus)
    VALUES (FLOOR(DBMS_RANDOM.VALUE(1, 10)), -- generate random employee_id between 1 and 10
            ROUND(DBMS_RANDOM.VALUE(50000, 100000), 2), -- generate random salary between 50000 and 100000 with 2 decimal places
            TRUNC(SYSDATE - DBMS_RANDOM.VALUE(1, 365)), -- generate random start_date between 1 and 365 days ago
            TRUNC(SYSDATE + DBMS_RANDOM.VALUE(1, 365)), -- generate random end_date between today and 365 days from now
            ROUND(DBMS_RANDOM.VALUE(5000, 15000), 2)); -- generate random bonus between 5000 and 15000 with 2 decimal places
  END LOOP;
  COMMIT;
END;
/

-- Generate Sample Employee Salary Data
BEGIN
  generate_employees_salary(50); -- generate 50 random records
END;
/

-- Cleanup
-- drop table employees;
-- drop table employees_salary;
-- drop procedure generate_employees_salary;
-- drop procedure add_employees;
