CREATE TRIGGER check_phone_format
BEFORE INSERT ON students
FOR EACH ROW
WHEN (NEW.phone NOT GLOB '+7([0-9][0-9][0-9])-[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
BEGIN
    SELECT CASE
        WHEN NEW.phone GLOB '+7([0-9][0-9][0-9])-[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' THEN
            NULL
        ELSE
            RAISE(ABORT, 'Invalid phone number format')
    END;
END;
