-- Safe divide

DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;
    IF b = 0 THEN
        result = 0;
    ELSE
        SET result = a / b;
    END IF;
    RETURN result
END $$
DELIMITER ;
