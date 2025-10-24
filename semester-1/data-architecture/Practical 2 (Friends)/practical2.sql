-- Practical 2 - Friends Database Queries

-- 1. Lucy Murphy's details
SELECT * FROM friend WHERE name = "Lucy Murphy";

-- 2. Friends who have surname Jones

SELECT * FROM friend WHERE name LIKE "%Jones";

-- 3. Friends who live on Chapel St

SELECT * FROM friend WHERE address LIKE "%Chapel St";

-- 4. Friends who live in the 042 area

SELECT * FROM friend WHERE telephone LIKE "042%";

-- 5. Bill Daly's address and phone no

SELECT address, telephone FROM friend WHERE name = "Bill Daly";
-- 6. Friends with surname Bloggs and live in the 042 area
SELECT * FROM friend WHERE name LIKE "%Bloggs" AND telephone LIKE "042%";

-- 7. Friends with surname Smith (Smyth)
SELECT * FROM friend WHERE name like "%Smith" OR name like "%smyth";

-- 8. Friends with surname King or live on Chapel St
Select  * FROM friend WHERE name like "%king" OR address LIKE "%Chapel St";

-- 9. Friends who play squash
SELECT friend.* FROM friend JOIN Hobbies USING (friend_id) WHERE hobby = 'squash';

-- 10. Friends who live in the 042 area and play football
SELECT friend.* FROM friend JOIN Hobbies USING (friend_id) WHERE telephone LIKE "042%" AND Hobbies.hobby = "football";

-- 11. Friends with surname Clarke who swim
-- Nothing shows up because Clarke last name none of them swim Clarke 5 and Clarke 7 platy football and running
SELECT friend.* FROM friend JOIN Hobbies USING (friend_id) WHERE name LIKE "%Clarke" AND Hobbies.hobby = "swimming";

-- 12. Friends who play tennis or golf
SELECT friend.* FROM friend JOIN Hobbies USING (Friend_id) WHERE Hobbies.hobby = "tennis" OR Hobbies.hobby = "golf";

-- 13. Friends who live on Chapel Street who play tennis or swim
Select friend.* FROM friend JOIN Hobbies USING (friend_id) WHERE address LIKE "%Chapel St" AND (Hobbies.hobby = "tennis" OR Hobbies.hobby = "swimming");


-- 14. Name and address of friends who like to run or play pool
SELECT name, address FROM friend JOIN Hobbies USING (friend_id) WHERE Hobbies.hobby = "running" OR Hobbies.hobby = "pool";