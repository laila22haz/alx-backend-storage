-- Optimize search and score

CREATE INDEX idx_name_first ON names (name(1), score(1));
