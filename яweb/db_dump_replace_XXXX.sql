SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


DELIMITER $$
DROP PROCEDURE IF EXISTS `PutPlus`$$
$$
DELIMITER ;


/* host1000218_XXXX — пользователь базы  DEFINER=`host1000218_XXXX`@`localhost` */
DELIMITER $$
CREATE PROCEDURE `PutPlus`(IN `ListNumber` VARCHAR(15) CHARSET utf8, IN `ProblemName` VARCHAR(10) CHARSET utf8, IN `PupilXlsdID` CHAR(7) CHARSET utf8)
    MODIFIES SQL DATA
    COMMENT 'Внести плюс данному школьнику за данную задачу в данном листке'
BEGIN
DECLARE useListID, useProblemID, usePupilID int(6);
SELECT ID into useListID    FROM `PList`    where replace(Number, 'a', 'а') = replace(ListNumber, 'a', 'а');
SELECT ID into useProblemID FROM `PProblem` where Name = ProblemName and ListID = useListID;
SELECT ID into usePupilID   FROM `PPupil`   where xlsID  = PupilXlsdID;
insert into `PResult` (`PupilID`, `ProblemID`, `Mark`, `User`, `TS`) VALUES (usePupilID, useProblemID, '+', 'admin', CURRENT_TIMESTAMP)  ON DUPLICATE KEY UPDATE Mark = '+';
COMMIT;
END$$
DELIMITER ;




DROP TABLE IF EXISTS `PClass`;
CREATE TABLE `PClass` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `Name` varchar(15) NOT NULL COMMENT 'Название',
  `Description` varchar(100) NOT NULL COMMENT 'Описание'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Классы';

TRUNCATE TABLE `PClass`;
INSERT INTO `PClass` (`ID`, `Name`, `Description`) VALUES
(1, 'VMSH', 'ВМШ, 6 класс');

DROP TABLE IF EXISTS `PList`;
CREATE TABLE `PList` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `ListTypeID` int(6) NOT NULL DEFAULT '1' COMMENT 'Тип',
  `ClassID` int(6) DEFAULT NULL COMMENT 'Класс',
  `Number` varchar(15) NOT NULL COMMENT 'Номер',
  `Description` varchar(100) NOT NULL COMMENT 'Описание',
  `Date` varchar(50) NOT NULL COMMENT 'Дата листка'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Листки';

DROP TABLE IF EXISTS `PListType`;
CREATE TABLE `PListType` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `Description` varchar(100) NOT NULL COMMENT 'Описание'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Типы листков';

TRUNCATE TABLE `PListType`;
INSERT INTO `PListType` (`ID`, `Description`) VALUES
(1, 'Обязательный листок'),
(2, 'Дополнительный листок');

DROP TABLE IF EXISTS `PProblem`;
CREATE TABLE `PProblem` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `ProblemTypeID` int(6) NOT NULL DEFAULT '0' COMMENT 'Тип задачи',
  `ListID` int(6) NOT NULL COMMENT 'Листок',
  `Number` int(5) NOT NULL COMMENT 'Порядковый номер в листке',
  `Group` int(5) NOT NULL COMMENT 'Номер группы',
  `Name` varchar(10) NOT NULL COMMENT 'Название'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Задачи';

DROP TABLE IF EXISTS `PProblemType`;
CREATE TABLE `PProblemType` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `Sign` char(3) NOT NULL COMMENT 'Обозначение',
  `Description` varchar(100) NOT NULL COMMENT 'Описание'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Типы задач';

TRUNCATE TABLE `PProblemType`;
INSERT INTO `PProblemType` (`ID`, `Sign`, `Description`) VALUES
(0, '', 'Обычная задача'),
(1, '*', 'Сложная задача'),
(2, '**', 'Очень сложная задача'),
(3, '°', 'Важная задача');

DROP TABLE IF EXISTS `PPupil`;
CREATE TABLE `PPupil` (
  `ID` int(6) NOT NULL COMMENT 'Уникальный ID',
  `ClassID` int(6) NOT NULL COMMENT 'Класс',
  `Name1` varchar(20) NOT NULL COMMENT 'Фамилия',
  `Name2` varchar(20) NOT NULL COMMENT 'Имя',
  `Name3` varchar(20) NOT NULL COMMENT 'Отчество',
  `Nick` varchar(15) NOT NULL COMMENT 'Короткое имя',
  `xlsID` char(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `PResult`;
CREATE TABLE `PResult` (
  `PupilID` int(6) NOT NULL COMMENT 'Школьник',
  `ProblemID` int(6) NOT NULL COMMENT 'Задача',
  `Mark` varchar(50) NOT NULL COMMENT 'Отметка',
  `TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Время внесения в базу',
  `User` varchar(50) NOT NULL COMMENT 'Кто внёс?'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Кондуит';

DROP TABLE IF EXISTS `PResultHistory`;
CREATE TABLE `PResultHistory` (
  `PupilID` int(6) NOT NULL COMMENT 'Школьник',
  `ProblemID` int(6) NOT NULL COMMENT 'Задача',
  `Mark` varchar(50) NOT NULL COMMENT 'Отметка',
  `TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Время внесения в базу',
  `User` varchar(50) NOT NULL COMMENT 'Кто внёс?'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Кондуит (история)';

DROP TABLE IF EXISTS `PUser`;
CREATE TABLE `PUser` (
  `User` varchar(50) NOT NULL COMMENT 'Имя пользователя',
  `DisplayName` varchar(50) NOT NULL COMMENT 'Отображаемое имя',
  `Group` varchar(50) NOT NULL COMMENT 'Группа',
  `Disabled` char(1) NOT NULL DEFAULT 'N' COMMENT 'Отключён'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Пользовательские группы';

TRUNCATE TABLE `PUser`;
INSERT INTO `PUser` (`User`, `DisplayName`, `Group`, `Disabled`) VALUES
('admin', 'Сергей Андреевич', 'Admin', 'N'),
('shashkov', 'Сергей Андреевич', 'Teacher', 'N'),
('vmsh', 'Просмотр', 'Pupil', 'N');

DROP TABLE IF EXISTS `PUserClass`;
CREATE TABLE `PUserClass` (
  `User` varchar(50) NOT NULL COMMENT 'Пользователь',
  `ClassID` int(6) NOT NULL COMMENT 'Класс'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Настройки доступа пользователей к классам';


ALTER TABLE `PClass`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `PList`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ListType` (`ListTypeID`);

ALTER TABLE `PListType`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `PProblem`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ProblemType` (`ProblemTypeID`),
  ADD KEY `List` (`ListID`);

ALTER TABLE `PProblemType`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `PPupil`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `PPupil_xlsID_idx` (`xlsID`) COMMENT 'Уникальный индекс по ID школшьника',
  ADD KEY `Class` (`ClassID`);

ALTER TABLE `PResult`
  ADD UNIQUE KEY `Result` (`PupilID`,`ProblemID`),
  ADD KEY `Pupil` (`PupilID`),
  ADD KEY `Problem` (`ProblemID`);

ALTER TABLE `PResultHistory`
  ADD KEY `PupilID` (`PupilID`,`ProblemID`,`TS`);

ALTER TABLE `PUser`
  ADD PRIMARY KEY (`User`);

ALTER TABLE `PUserClass`
  ADD KEY `User` (`User`),
  ADD KEY `ClassID` (`ClassID`);


ALTER TABLE `PClass`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID', AUTO_INCREMENT=2;

ALTER TABLE `PList`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID';

ALTER TABLE `PListType`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID', AUTO_INCREMENT=3;

ALTER TABLE `PProblem`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID';

ALTER TABLE `PProblemType`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID', AUTO_INCREMENT=4;

ALTER TABLE `PPupil`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID';


ALTER TABLE `PList`
  ADD CONSTRAINT `PList_ibfk_1` FOREIGN KEY (`ListTypeID`) REFERENCES `PListType` (`ID`) ON UPDATE CASCADE;

ALTER TABLE `PProblem`
  ADD CONSTRAINT `PProblem_ibfk_1` FOREIGN KEY (`ProblemTypeID`) REFERENCES `PProblemType` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `PProblem_ibfk_2` FOREIGN KEY (`ListID`) REFERENCES `PList` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `PPupil`
  ADD CONSTRAINT `PPupil_ibfk_1` FOREIGN KEY (`ClassID`) REFERENCES `PClass` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `PResult`
  ADD CONSTRAINT `PResult_ibfk_1` FOREIGN KEY (`PupilID`) REFERENCES `PPupil` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `PResult_ibfk_2` FOREIGN KEY (`ProblemID`) REFERENCES `PProblem` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `PUserClass`
  ADD CONSTRAINT `PUserClass_ibfk_1` FOREIGN KEY (`User`) REFERENCES `PUser` (`User`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `PUserClass_ibfk_2` FOREIGN KEY (`ClassID`) REFERENCES `PClass` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
