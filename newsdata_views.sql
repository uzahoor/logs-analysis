-- DROP VIEW top_articles;
CREATE OR REPLACE view top_articles AS 
	SELECT articles.title, articles.author, COUNT(*) AS views 
	FROM articles JOIN log 
	ON log.path = '/article/' || articles.slug
	GROUP BY articles.title, articles.author
	ORDER BY views DESC;

-- DROP VIEW top_authors;
CREATE OR REPLACE view top_authors AS 
	SELECT authors.name, sum(top_articles.views) AS views 
	FROM top_articles JOIN authors 
	ON authors.id = top_articles.author
	GROUP BY authors.name
	ORDER BY views DESC;

-- DROP VIEW errors;
CREATE OR REPLACE view errors AS 
	SELECT date(time) AS date, COUNT(*) AS requests
	FROM log
	WHERE status LIKE '%404%'
	GROUP BY date;

-- DROP VIEW successes;
CREATE OR REPLACE view total AS 
	SELECT date(time) AS date, COUNT(*) AS requests
	FROM log
	GROUP BY date;

-- DROP VIEW error_days;
CREATE OR REPLACE view error_days AS 
	SELECT total.date, ROUND(((errors.requests * 1.0) / total.requests) * 100, 2) AS errors_percent
	FROM errors JOIN total
	ON total.date = errors.date
	WHERE ROUND(((errors.requests * 1.0) / total.requests) * 100, 2) > 1
	ORDER BY errors DESC;