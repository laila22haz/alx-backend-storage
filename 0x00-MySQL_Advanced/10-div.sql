-- Safe divide

DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS
FLOAT
BEGIN
    DECLARE total;
    IF b = 0 THEN
        total = 0;
    ELSE
        SET total = a / b;
    END IF;
END $$
DELIMITER ;
