-- Best band ever!
-- ranks country origins of bands

SELECT origin, SUM(fans) as total_fans
FROM metal_bands
GROUP By origin
ORDER By total_fans DESC;
