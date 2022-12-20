--
-- Datenbank: `redmine_api`
-- Tabellenstruktur für Tabelle `ts_interface`
--

CREATE TABLE `ts_interface` (
  `id` int(11) NOT NULL,
  `ticketida` bigint(20) NOT NULL,
  `ticketidb` bigint(20) NOT NULL,
  `statusa` int(1) NOT NULL,
  `mailida` int(11) NOT NULL,
  `transferb` int(1) NOT NULL,
  `updateon` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `ts_interface` ADD PRIMARY KEY (`id`);
ALTER TABLE `ts_interface` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
