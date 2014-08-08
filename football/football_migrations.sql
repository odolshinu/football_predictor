ALTER TABLE `football_match` ADD COLUMN `stage` varchar(5);

ALTER TABLE `football_match` ADD COLUMN `gameweek` integer;

ALTER TABLE `football_league` ADD COLUMN `code` varchar(8);
ALTER TABLE `football_league` ADD COLUMN `championship_id` integer;

ALTER TABLE `football_league` ADD CONSTRAINT `championship_id_refs_id_01efb5ec` FOREIGN KEY (`championship_id`) REFERENCES `football_championship` (`id`);

ALTER TABLE `football_team` ADD COLUMN `logo` varchar(100);

ALTER TABLE `football_league` ADD COLUMN `admin_id` integer;
ALTER TABLE `football_league` ADD CONSTRAINT `admin_id_refs_id_c8b2fbfa` FOREIGN KEY (`admin_id`) REFERENCES `auth_user` (`id`);