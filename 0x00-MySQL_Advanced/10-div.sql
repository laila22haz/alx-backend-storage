-- Safe divide

DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS
DECIMAL(10,2)
BEGIN
    DECLARE total DECIMAL(10,2);
    SET total = a / b;
    IF b = 0 THEN
        RETURNS 0;
    END IF;
END $$
DELIMITER ;
