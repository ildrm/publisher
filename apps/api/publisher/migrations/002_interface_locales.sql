-- Interface locale is independent from manuscript language and direction.
-- NULL preserves a legacy account's browser language until the user selects a preference.
ALTER TABLE users ADD COLUMN locale TEXT CHECK(locale IS NULL OR locale IN('en','zh','hi','es','ar','fr','bn','pt','id','ur','ru','de','ja','pcm','fa'));
